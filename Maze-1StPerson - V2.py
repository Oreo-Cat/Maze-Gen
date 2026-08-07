#Need to:
#colour code start and end points
#Make turning smoother
#Add minimap
import random
import turtle
import math
import time
import bitarray
from PIL import Image



#Main maze generation
size = 20 #Size of maze
render_dist = 10 #Render distance of maze
scale = 2 #Scale of maze viewer window
width = 600 #Width of viewer window
height = 400 #Height of viewer window
FOV = 1 #FOV of viewer window. Defult = 1, higher numbers = compressed view, lower numbers = stretched view - NOT IMPLEMENTED FULLY

completed = 0
choices: list[int] = []
horizontal = bitarray.bitarray(size*(size-1)) #Using bitarray as it is less intensive on memory than regular "byte" array.
horizontal.setall(1)
vertical = bitarray.bitarray(size*(size-1))
vertical.setall(1)
VNC: list[int] = []
visitedset = set()
percent = 0
screen = turtle.Screen()

current = random.randint(0, int(math.pow(size, 2)))
visitedset.add(current)
VNC.append(current)

starttotal = time.perf_counter()

while completed < math.pow(size, 2):
    percent += 1
    if percent % (size*size/100)==0:
        print(int(completed/math.pow(size, 2)*100), "percentage complete")
    loop = random.randint(3, 5)
    for i in range(loop):
        choices.clear()
        #Left
        if not current-1 in visitedset and not current % size == 0: #Swapped from arrays to sets here - led to a 30x speed improvement!
            choices.append(current-1)
        #Right
        if not current+1 in visitedset and not (current+1) % size == 0:
            choices.append(current+1)
        #Above
        if not current-size in visitedset and not current-size > math.pow(size, 2)-1 and not current-size < 0:
            choices.append(current-size)
        #Below
        if not current+size in visitedset and not current+size > math.pow(size, 2)-1 and not current+size < 0:
            choices.append(current+size)

        if choices == []:
            completed += 1
            VNC.remove(current) #This is the bottleneck!
            break
        chosen = random.choice(choices)
        VNC.append(chosen)
        visitedset.add(chosen)
        #Left
        if current - chosen == 1:
            wall = chosen//size*(size-1)+chosen%size #wall = math.floor(chosen/size)*(size-1)+remainder(chosen, size)   Swapped from math. to integer math
            if not wall > len(horizontal)-1:
                horizontal[wall] = 0
        #Right
        elif chosen - current == 1:
            wall = current//size*(size-1)+current%size #wall = math.floor(current/size)*(size-1)+remainder(current, size)
            if not wall > len(horizontal)-1:
                horizontal[wall] = 0
        #Above
        elif current - chosen == size:
            if not chosen > len(vertical)-1:
                vertical[chosen] = 0
        #Below
        else:
            if not current > len(vertical)-1:
                vertical[current] = 0

        current = chosen
    if not VNC == []:
        index = random.randint(0, len(VNC)-1) #Swapped to using indexing for random choices, slight speed improvement.
        current = VNC[index]

endtotal = time.perf_counter()
print(endtotal-starttotal, "Total time") # Timer to count how long it took to calculate



#Image generation
x = 1
y = 1
it = 0

maze = Image.new(mode="RGB", size=(size*2+1, size*2+1))
for a in range(size):
    for b in range(size-1):
        maze.putpixel((x, y), (255,255,255))
        x += 1
        if horizontal[it] == 0:
            maze.putpixel((x, y), (255,255,255))
        x += 1
        it += 1
    maze.putpixel((x, y), (255,255,255))
    y += 2
    x = 1
    
y = 2
x = 1
it = 0

for a in range(size-1):
    for b in range(size):
        if vertical[it] == 0:
            maze.putpixel((x, y), (255,255,255))
        x += 2
        it += 1
    y += 2
    x = 1

maze.putpixel((1, 0), (100,255,100))
maze.putpixel((size*2-1, size*2), (255,100,100))
maze.save("maze.png")
print("Done!")



#Full maze array constructor
h = 0
v = 0
maze = []
for i in range(size*2+1): #Adding walls to the top of the maze
    maze.append(1)
for a in range(size-1):
    maze.append(1)#Adding walls to the left of the maze
    for b in range(size-1): #Horizontal rows
        maze.append(0) #0 = path, 1 = wall
        if horizontal[h] == 0:
            maze.append(0)
        else:
            maze.append(1)
        h += 1
    maze.append(0)
    maze.append(1)#Adding walls to the right of the maze

    maze.append(1) #Adding walls to the left of the maze
    if vertical[v] == 0:#Vertical rows
        maze.append(0)
    else:
        maze.append(1)
    v += 1
    for b in range(size-1):
        maze.append(1)
        if vertical[v] == 0:
            maze.append(0)
        else:
            maze.append(1)
        v += 1
    maze.append(1)#Adding walls to the right of the maze

maze.append(1) #Adding walls to the left of the maze
for b in range(size-1): #Last horizontal row
    maze.append(0)
    if horizontal[h] == 0:
        maze.append(0)
    else:
        maze.append(1)
    h += 1
maze.append(0)
maze.append(1)#Adding walls to the right of the maze
for i in range(size*2+1): #Adding walls to the bottom of the maze
    maze.append(1)

#Turtle wall 1st person functions
L = turtle.Turtle()
R = turtle.Turtle()
L.pensize(3)
R.pensize(3)
L.hideturtle()
R.hideturtle()
def draw_left_wall(draw_size, scale): #L = turtle, draw_size, scale = scale
    turtle.tracer(0)
    global L
    L.pendown()
    old_x = L.xcor() #Need to swap this bit out for maths
    old_y = L.ycor()
    L.goto(width*-1*scale/4*draw_size,height*scale/4*draw_size)
    L.goto(width*-1*scale/4*draw_size,height*-1*scale/4*draw_size)
    L.goto(old_x, old_y*-1)
    L.teleport(width*-1*scale/4*draw_size,height*scale/4*draw_size)
    turtle.update()

def draw_left_path(draw_size, scale):
    turtle.tracer(0)
    global L
    L.penup()
    L.sety(height*scale/4*draw_size)
    L.pendown()
    old_x = L.xcor()
    old_y = L.ycor()
    L.goto(width*-1*scale/4*draw_size,height*scale/4*draw_size)
    L.goto(width*-1*scale/4*draw_size,height*-1*scale/4*draw_size)
    L.goto(old_x, old_y*-1)
    L.teleport(width*-1*scale/4*draw_size,height*scale/4*draw_size)
    turtle.update()

def draw_right_wall(draw_size, scale):
    turtle.tracer(0)
    global R
    R.pendown()
    old_x = R.xcor()
    old_y = R.ycor()
    R.goto(width*scale/4*draw_size,height*scale/4*draw_size)
    R.goto(width*scale/4*draw_size,height*-1*scale/4*draw_size)
    R.goto(old_x, old_y*-1)
    R.teleport(width*scale/4*draw_size,height*scale/4*draw_size)
    turtle.update()

def draw_right_path(draw_size, scale):
    turtle.tracer(0)
    global R
    R.penup()
    R.sety(400*scale/4*draw_size)
    R.pendown()
    old_x = R.xcor()
    old_y = R.ycor()
    R.goto(width*scale/4*draw_size,height*scale/4*draw_size)
    R.goto(width*scale/4*draw_size,height*-1*scale/4*draw_size)
    R.goto(old_x, old_y*-1)
    R.teleport(width*scale/4*draw_size,height*scale/4*draw_size)
    turtle.update()

def draw_forward_wall(draw_size, scale):
    turtle.tracer(0)
    global L
    L.pendown()
    L.teleport(width*scale/4*draw_size,height*scale/4*draw_size)
    L.goto(width*-1*scale/4*draw_size,height*scale/4*draw_size)
    L.teleport(width*scale/4*draw_size,height*-1*scale/4*draw_size)
    L.goto(width*-1*scale/4*draw_size,height*-1*scale/4*draw_size)
    turtle.update()

def draw_end(draw_size, scale, forward_walls):
    turtle.tracer(0)
    global R
    R.fillcolor("Red")
    R.pendown()
    R.teleport(width*scale/4*draw_size,height*-1*scale/4*draw_size)
    R.begin_fill()
    R.goto(width*-1*scale/4*draw_size,height*-1*scale/4*draw_size)
    R.goto(width*-1*scale/4*(1/(forward_walls+FOV-2)),height*-1*scale/4*draw_size)
    R.goto(width*scale/4*(1/(forward_walls+FOV-2)),height*-1*scale/4*draw_size)
    R.goto(width*-1*scale/4*draw_size,height*-1*scale/4*draw_size)
    R.end_fill()
    turtle.update()

def draw_maze(forward_walls, left_walls, right_walls):
    global screen #I only need to write global variables if I edit the variables not read them

    L.clear() #Not clearscreen() because it clears onkeypress aswell
    R.clear()

    L.teleport(width*-1/2*scale,height/2*scale)
    R.teleport(width/2*scale, height/2*scale)

    for i in range(forward_walls):
        if left_walls[i] == 1:
            draw_left_wall(1/(i+FOV), scale)
        else:
            draw_left_path(1/(i+FOV), scale)
        if right_walls[i] == 1:
            draw_right_wall(1/(i+FOV), scale)
        else:
            draw_right_path(1/(i+FOV), scale)
    if ending:
        draw_end(1/(forward_walls+FOV-1), scale, forward_walls)
    draw_forward_wall(1/(forward_walls+FOV-1), scale)



#Wall drawer code
while True:
    current = random.randint(0, len(maze)-1)
    if maze[current] == 0: #To make sure player doesn't spawn in a wall
        break
#current = size*2+2 #For testing: Spawns player at maze start

direction = 1

ending = False #Initialise ending variable
def main(direction): #0 = left, 1 = up, 2 = right, 3 = down
    global ending
    left_walls = []
    right_walls = []
    forward_walls = render_dist
    
    #Left
    if direction == 0:
        for i in range(render_dist):
            if current-i-1 < 0 or maze[current-i] == 1:
                forward_walls = i
                if current-i == 2:  ##########Not fully implemented
                    ending = True
                break
        for i in range(forward_walls):
            left_walls.append(maze[current-i+(size*2+1)])
            right_walls.append(maze[current-i-(size*2+1)])
        draw_maze(forward_walls, left_walls, right_walls)
    #Right
    elif direction == 2:
        for i in range(render_dist):
            if current+i+1 >= (size*2+1)**2 or maze[current+i] == 1:
                forward_walls = i
                break
        for i in range(forward_walls):
            left_walls.append(maze[current+i-(size*2+1)])
            right_walls.append(maze[current+i+(size*2+1)])
        draw_maze(forward_walls, left_walls, right_walls)
    #Up
    elif direction == 1:
        for i in range(render_dist):
            if (current-(size*2+1)*i)-1 < 0 or maze[current-((size*2+1)*i)] == 1:
                forward_walls = i
                if current-((size*2+1)*i) == 2:  ##########Not fully implemented
                    ending = True
                break
        for i in range(forward_walls):
            left_walls.append(maze[current-((size*2+1)*i)-1])
            right_walls.append(maze[current-((size*2+1)*i)+1])
        draw_maze(forward_walls, left_walls, right_walls)
    #Down    
    else:
        for i in range(render_dist):
            if current+((size*2+1)*i)+1 >= (size*2+1)**2 or maze[current+((size*2+1)*i)] == 1:
                forward_walls = i
                break
        for i in range(forward_walls):
            left_walls.append(maze[current+((size*2+1)*i)+1])
            right_walls.append(maze[current+((size*2+1)*i)-1])
        draw_maze(forward_walls, left_walls, right_walls)
    print(current, forward_walls, left_walls, right_walls)


def forward():
    global current
    if direction == 0:
        current -= 1
        if maze[current] == 1:
            current += 1
    elif direction == 1:
        current -= size*2+1
        if maze[current] == 1:
            current += size*2+1
    elif direction == 2:
        current += 1
        if maze[current] == 1:
            current -= 1
    else:
        current += size*2+1
        if maze[current] == 1:
            current -= size*2+1
    main(direction)

def backward():
    global current
    if direction == 0:
        current += 1
        if maze[current] == 1:
            current -= 1
    elif direction == 1:
        current += size*2+1
        if maze[current] == 1:
            current -= size*2+1
    elif direction == 2:
        current -= 1
        if maze[current] == 1:
            current += 1
    else:
        current -= size*2+1
        if maze[current] == 1:
            current += size*2+1
    main(direction)
   
def left():
    global direction
    direction -= 1
    if direction > 3:
        direction = 0
    elif direction < 0:
        direction = 3
    main(direction)

def right():
    global direction
    direction += 1
    if direction > 3:
        direction = 0
    elif direction < 0:
        direction = 3
    main(direction)

screen.setup(width*scale, height*scale)  
forward() #This just makes sure the screen begins displaying
screen.onkeypress(forward, "w")
screen.onkeypress(left, "a")
screen.onkeypress(backward, "s")
screen.onkeypress(right, "d")
screen.listen()
screen.mainloop()
