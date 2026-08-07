# Maze-Gen
This repo serves as a final collection of all my projects maze related. I have worked on this project for multiple years, and I have decided to finally stop. I will leave all my data for someone else to push ahead further. The repo includes TeraMaze (world's biggest maze) and my best algorithms and ideas for infinite maze generation. Enjoy!

# TerraMaze
The final TeraMaze attempt can be found here: on Gigapan as one of the largest images the website hosts. It is the world's largest computer generated perfect maze. On the page you can find some more details on it as well as the issues I left it with. I will recap the issue here. The maze is generated in chunks, to avoid VRAM and allow the project to run without terabytes of RAM. The first chunk generates like a normal growing tree maze. The chunk stitching should be simple - the chunks themselves are generated connected like a mini maze (via more growing tree), any new chunk checks if any chunks around it have been generated yet (of which it must be touching at least one old chunk) and any edges of the chunk that were touching old chunks can have new maze generated from. This would create a seamless final maze. The issue was that the code wasn't recognising some of the available walls to grow from, creating giant seams stretching across the maze, this could definitely have been due to the maze prioritising growing from new maze rather than the walls.

Other optimisations:
. Swapping the random library to std::pcg64 with thread local storage for parallelisation and uint64_t to prevent integer overflow when selecting next maze cell
. Further utilisation of queues and stacks
. Turn off PNG compression for temp files when there is space on device

By fixing these issues, adding the optimisations and generating a final maze, you would easily be able to hold the record for world's biggest maze!
I believe I have included the final code in c++ (called Maze_Optimised_300000_Uniform.cpp) in a zip folder also containing the rest of the files I used for testing. The vips-dev-8.17 folder has been left empty as vips is not mine, you will need to download dependencies and reroute file paths if you want to use this direct code. For this reason, the code has not been included as a working prototype but mainly as a learning experience, for iteration and improvement.

#InfiniMaze
Despite there being a lot of test code and working prototypes, I will only include the algorithms and core ideas for the project, as to provide a clean slate for anyone wanting to begin.

FNC:
Flow Noise Construction is a very simple algorithm, it is built as a local, deterministic improvement of binary tree algorithm. Think of it as a ternary tree algorithm. It is an improved version of binary tree that allows you to travel in three directions, whilst still being perfect, very simple, and local.
It works like this: 
    First we initialise a grid with floats, each cell then goes through this process: 
        1) If this cell is the highest of it, the left cell and the right cell, connect up.
        2) Else, connect to the lowest higher cell (left or right).
        
A python demonstration is included.

SS:
Spin scramble is simply this:
Every rotation of cells in a small C shape (4 cells, 3 connections), can be rotated around its centre as long as it doesn't rotate cells already being rotated in another viable C shape.
This can be done with wall Cs or path Cs.
It MAINTAINS MAZE PERFECTNESS - no new loops or islands are created.

A python program is included that fits with FNC to scramble mazes.
