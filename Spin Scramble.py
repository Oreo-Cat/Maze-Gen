#A simple, aglorithmic test for the Spin Scramble algorithm (not infinite, only finite)
#BLACK IS WALLS, WHITE IS PATHS

import numpy as np
from PIL import Image


def fract(x):
    return x - np.floor(x)

def rand3(x, y, z):
    vec = np.array([x, y, z], dtype=float)
    vec = fract(vec * 0.1031)
    vec += np.dot(vec, vec[::-1] + 31.32)
    return fract((vec[0] + vec[1]) * vec[2])

def rand2(x, y):
    return rand3(rand3(x, 0.0, y), 0.0, y)
    
def get_wall_dir(VonN):
    if VonN[1] == 1 and VonN[2] == 1 and VonN[3] == 1: #Then VonN[0] == 0
        wall_dir = 0
    elif VonN[0] == 1 and VonN[2] == 1 and VonN[3] == 1: #Then VonN[1] == 0
        wall_dir = 1
    elif VonN[0] == 1 and VonN[1] == 1 and VonN[3] == 1: #Then VonN[2] == 0
        wall_dir = 2
    elif VonN[0] == 1 and VonN[1] == 1 and VonN[2] == 1: #Then VonN[3] == 0
        wall_dir = 3
    else:
        wall_dir = 4
    return wall_dir


maze = Image.open("maze.png")
width = maze.width
height = maze.height

walls_width = int((width-3)/2)
walls_height = int((height-3)/2)

visited = [False] * (walls_width*walls_height) #So cell spins aren't repeated

seed = 42
passes = 100

for iteration in range(passes):
    wall_dir_arr = []
    old_wall_dir_arr = []

    for y in range(walls_height):
        for x in range(walls_width):
            VonN = [0, 0, 0, 0]
            if maze.getpixel([x*2+2, y*2+1])[0] >= 128:
                VonN[0] = 1
            if maze.getpixel([x*2+3, y*2+2])[0] >= 128:
                VonN[1] = 1
            if maze.getpixel([x*2+2, y*2+3])[0] >= 128:
                VonN[2] = 1
            if maze.getpixel([x*2+1, y*2+2])[0] >= 128:
                VonN[3] = 1
                
            wall_dir = get_wall_dir(VonN)
            old_wall_dir_arr.append(wall_dir)

            if wall_dir != 4 and visited[y*walls_width+x] == False: #Then there is only one wall connection / able to be scrambled
                random = rand3(x, y, seed)
                if random < 1.0/3.0:
                    wall_dir += 1
                elif random < 2.0/3.0:
                    wall_dir += 2
                else:
                    wall_dir += 3

                wall_dir = wall_dir % 4

            wall_dir_arr.append(wall_dir)

            #print([x*2+2, y*2+2])
            #print(VonN)

    for i in range(len(wall_dir_arr)):
        if wall_dir_arr[i] != 4:
            if wall_dir_arr[i] == 0 and i >= walls_width and wall_dir_arr[i-walls_width] != 4 and rand2(i-walls_width, seed) >= rand2(i, seed):
                #print("up battle")
                wall_dir_arr[i] = 4
                old_wall_dir_arr[i] = 4
                visited[i] = True
            elif wall_dir_arr[i] == 1 and (i+1) % walls_width != 0 and wall_dir_arr[i+1] != 4 and rand2(i+1, seed) >= rand2(i, seed):
                #print("right battle")
                wall_dir_arr[i] = 4
                old_wall_dir_arr[i] = 4
                visited[i] = True
            elif wall_dir_arr[i] == 2 and i < walls_width * (walls_height-1) and wall_dir_arr[i+walls_width] != 4 and rand2(i+walls_width, seed) >= rand2(i, seed):
                #print("down battle")
                wall_dir_arr[i] = 4
                old_wall_dir_arr[i] = 4
                visited[i] = True
            elif wall_dir_arr[i] == 3 and i % walls_width != 0 and wall_dir_arr[i-1] != 4 and rand2(i-1, seed) >= rand2(i, seed):
                #print("left battle")
                wall_dir_arr[i] = 4
                old_wall_dir_arr[i] = 4
                visited[i] = True
                
            if i >= walls_width and wall_dir_arr[i-walls_width] == 2 and rand2(i-walls_width, seed) >= rand2(i, seed):
                #print("up battle")
                wall_dir_arr[i] = 4
                old_wall_dir_arr[i] = 4
                visited[i] = True
            elif (i+1) % walls_width != 0 and wall_dir_arr[i+1] == 3 and rand2(i+1, seed) >= rand2(i, seed):
                #print("right battle")
                wall_dir_arr[i] = 4
                old_wall_dir_arr[i] = 4
                visited[i] = True
            elif i < walls_width * (walls_height-1) and wall_dir_arr[i+walls_width] == 0 and rand2(i+walls_width, seed) >= rand2(i, seed):
                #print("down battle")
                wall_dir_arr[i] = 4
                old_wall_dir_arr[i] = 4
                visited[i] = True
            elif i % walls_width != 0 and wall_dir_arr[i-1] == 1 and rand2(i-1, seed) >= rand2(i, seed):
                #print("left battle")
                wall_dir_arr[i] = 4
                old_wall_dir_arr[i] = 4
                visited[i] = True

    for i in range(len(old_wall_dir_arr)):
        x = int(i % walls_width)*2+2
        y = int(i // walls_width)*2+2
        
        if old_wall_dir_arr[i] == 0:
            maze.putpixel((x,y-1),(255,255,255))
        elif old_wall_dir_arr[i] == 1:
            maze.putpixel((x+1,y),(255,255,255))
        elif old_wall_dir_arr[i] == 2:
            maze.putpixel((x,y+1),(255,255,255))
        elif old_wall_dir_arr[i] == 3:
            maze.putpixel((x-1,y),(255,255,255))

        if wall_dir_arr[i] == 0:
            maze.putpixel((x,y-1),(0,0,0))
        elif wall_dir_arr[i] == 1:
            maze.putpixel((x+1,y),(0,0,0))
        elif wall_dir_arr[i] == 2:
            maze.putpixel((x,y+1),(0,0,0))
        elif wall_dir_arr[i] == 3:
            maze.putpixel((x-1,y),(0,0,0))
    seed += 1
    
    if round(iteration%(passes/100),10) == 0:
        print(round(iteration/passes*100))
    
maze.show()
maze.save("SS_maze.png")
