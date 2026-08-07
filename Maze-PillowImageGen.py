import random
import turtle
import math
import time
import bitarray
from PIL import Image

size = 50
completed = 0
choices: list[int] = []
horizontal = bitarray.bitarray(size*(size-1)) #Using bitarray as it is less intensive on memory than regular "byte" array.
horizontal.setall(1)
vertical = bitarray.bitarray(size*(size-1))
vertical.setall(1)
VNC: list[int] = []
visitedset = set()
percent = 0

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
