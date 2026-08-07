#A simple, algorithmic test for the FNC algorithm (not infinite, nor finite, generates test samples for Spin scramble)
#BLACK IS WALLS, WHITE IS PATHS
#DO NOT COPY ANY OF THIS FOR FINAL VERSION - IT IS VERY WRONG

import random
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


width = 1000 #In cells
height = 1000 #In cells
seed = 42

noise = []
for y in range(height):
    row = []
    for x in range(width):
        row.append(rand3(x, y, seed))
    noise.append(row)
#print(noise)

maze = Image.new(mode="RGB", size=(width*2+1, height*2+1))
for y in range(height):
    for x in range(width):
        maze.putpixel((x*2+1, y*2+1), (255, 255, 255))
        if x % width == 0: #If it is the left most point
            L = 0.0
        else:
            L = noise[y][x-1]
        if (x+1) % width == 0: #If it is the right most point
            R = 0.0
        else:
            R = noise[y][x+1]
        M = noise[y][x]

        #M R L or L M R - the letter after M in ascending order is the correct dir - the lowest greater
        if M == min(L, M, R):
            if L < R:
                maze.putpixel((x*2, y*2+1), (255, 255, 255)) #LEFT
            else: # R == max(L, R)
                maze.putpixel((x*2+2, y*2+1), (255, 255, 255)) #RIGHT
        elif M == max(L, M, R):
            maze.putpixel((x*2+1, y*2), (255, 255, 255)) #UP
        else: #L M R or R M L
            if L > M:
                maze.putpixel((x*2, y*2+1), (255, 255, 255)) #LEFT
            else:
                maze.putpixel((x*2+2, y*2+1), (255, 255, 255)) #RIGHT
maze.save("maze.png")  
print("Done!")
