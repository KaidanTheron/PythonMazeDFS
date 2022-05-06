"""
READ ME:
- If you want to edit properties of maze generation you can change "widthMaze" property on line 35. 
- If you want to change generation/search speed you can change ppf: pause per frame on line 36.

Run this baby in the terminal and watch it go. Btw, there are some cases with the generation algorithm where it reaches
its max recursion depth, and this tends to happen with "widthMaze" > 75. The recursion can also get to max depth on the
search with "widthMaze" > 50, but don't worry about it.

Once you run the script it will generate the maze. After the maze is generated you can press enter and it will solve the
maze.
"""


import math
import pygame
import sys
import time
from random import randint

# - >
# Initialize pygame
pygame.init()

# - >
# Initialize pygame window
fps = 60
HEIGHT = 600
WIDTH = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

################################################################### - > 
################################################################### - > 
# Controlling values:
widthMaze = 59 # length of one side of maze
ppf = 0.1 # time in seconds between each frame

# branchDepth = 0 # implement branch depth property to make recursive algorithm more branchy? 
################################################################### - >
################################################################### - >

# - >
# Selection of Maze generation algorithm's must be available
# - Randomized depth-first search
# - Randomized Kruskal's algorithm
# - Randomized Prim's algorithm
# - Aldous-Broder algorithm
# - Recursive division method
#
# Walls are identified by black cells, passages are identified by white cells, solution cells are marked as red

class Maze(object):

    width = 0
    grid = []
    entrance = []
    exit = []
    solution = []

    def __init__(self, width):
        if self.width % 2 == 0:
            self.width += 1
        self.grid = [[[1, False] for _ in range(width)] for _ in range(width)] # each cell is a list 
        # [status, visited] status being 0 for open, 1 for wall and 2 for current cell during gen, 3 for solution
        self.width = width
        # [row, column]:
        # entrance top left corner
        self.entrance = [0, 1] 
        # set entrance cell as visited
        self.grid[self.entrance[0]][self.entrance[1]][1] = True
        self.grid[self.entrance[0]][self.entrance[1]][0] = 0
        # exit bottom left corner
        self.exit = [width-1, width-2]
        # set exit cell as visited
        self.grid[self.exit[0]][self.exit[1]][1] = True
        self.grid[self.exit[0]][self.exit[1]][0] = 0

    def generate(self, algo):
        if algo == "DepthFirst":
            self.df()
            self.resetVisited()
        elif algo == "RecursiveDivision":
            self.recursiveDiv()
        elif algo == "Kruskal":
            self.kruskal()
        elif algo == "Prim":
            self.prim()
        elif algo == "AldousBroder":
            self.ab()

    def resetVisited(self):
        for row in range(self.width):
            for column in range(self.width):
                self.grid[row][column][1] = False

        render(self)

    def createSolution(self):
        for cell in self.solution:
            self.grid[cell[0]][cell[1]][0] = 3

    # - >
    # These are all the available maze solving algorthims:
    # All return a grid with a set of solution cells
    def depthFirstSearch(self, currentCell = [1,1]):
        time.sleep(ppf)
        self.solution.append(currentCell)
        self.grid[currentCell[0]][currentCell[1]][1] = True
        self.grid[currentCell[0]][currentCell[1]][0] = 2
        self.createSolution()
        render(self)
        self.grid[currentCell[0]][currentCell[1]][0] = 0
        cells = self.findUnvisitedCellsSearch(currentCell, num=1)
        while len(cells) != 0:
            # search every unvisited cell adjacent to this cell
            for cell in cells:         
                if self.depthFirstSearch(cell):
                    return True
            cells = self.findUnvisitedCellsSearch(currentCell, num=1)
        
        if currentCell != self.exit:
            self.solution.pop()
        else:
            return True

        self.createSolution()
        render(self)
        self.grid[currentCell[0]][currentCell[1]][0] = 0
        

    # - >
    # for a given cell, find adjacent unvisited cells, the num argument dictates what counts as an adjacent cell 
    def findUnvisitedCells(self, currentCell, num = 2):
        cells = []

        if (currentCell[1]+num < self.width):
            if (self.grid[currentCell[0]][currentCell[1]+num][1] == False):
                cells.append([currentCell[0], currentCell[1]+num])
        if (currentCell[0]+num < self.width): 
            if (self.grid[currentCell[0]+num][currentCell[1]][1] == False):
                cells.append([currentCell[0]+num, currentCell[1]])
        if (currentCell[0]-num >= 0): 
            if (self.grid[currentCell[0]-num][currentCell[1]][1] == False):
                cells.append([currentCell[0]-num, currentCell[1]])
        if (currentCell[1]-num >= 0): 
            if (self.grid[currentCell[0]][currentCell[1]-num][1] == False):
                cells.append([currentCell[0], currentCell[1]-num])

        return cells

    def findUnvisitedCellsSearch(self, currentCell, num = 1):
        cells = []

        if (currentCell[1]+num < self.width):
            if (self.grid[currentCell[0]][currentCell[1]+num][0] == 0) & (self.grid[currentCell[0]][currentCell[1]+num][1] == False):
                    cells.append([currentCell[0], currentCell[1]+num])
        if (currentCell[0]+num < self.width):  
            if (self.grid[currentCell[0]+num][currentCell[1]][0] == 0) & (self.grid[currentCell[0]+num][currentCell[1]][1] == False):
                    cells.append([currentCell[0]+num, currentCell[1]])
        if (currentCell[0]-num >= 0):
            if (self.grid[currentCell[0]-num][currentCell[1]][0] == 0) & (self.grid[currentCell[0]-num][currentCell[1]][1] == False):
                    cells.append([currentCell[0]-num, currentCell[1]])
        if (currentCell[1]-num >= 0): 
            if (self.grid[currentCell[0]][currentCell[1]-num][0] == 0) & (self.grid[currentCell[0]][currentCell[1]-num][1] == False):
                    cells.append([currentCell[0], currentCell[1]-num])

        return cells
    
    # - >
    # Each algorithm updates the maze grid creating a maze, also defining the entrance and exit of the maze
    # so that the solving algo knows where to enter and when it has found a solution
    def df(self, currentCell = [1,1]):
        time.sleep(ppf)
        self.grid[currentCell[0]][currentCell[1]][1] = True
        self.grid[currentCell[0]][currentCell[1]][0] = 2
        render(self)
        self.grid[currentCell[0]][currentCell[1]][0] = 0
        cells = self.findUnvisitedCells(currentCell)
        while len(cells) != 0:
            # newCell is the random adjacent cell that df is searching
            newCell = cells[randint(0, len(cells)-1)]
            # remove wall between newCell and current cell
            self.grid[currentCell[0]+math.floor((newCell[0]-currentCell[0])*0.5)][currentCell[1]+math.floor((newCell[1]-currentCell[1])*0.5)][0] = 0
            self.grid[currentCell[0]+math.floor((newCell[0]-currentCell[0])*0.5)][currentCell[1]+math.floor((newCell[1]-currentCell[1])*0.5)][1] = True
            self.df(newCell)
            cells = self.findUnvisitedCells(currentCell)  
        
        self.grid[currentCell[0]][currentCell[1]][0] = 0
        render(self)

    def recursiveDiv(self):
        pass

    def kruskal(self):
        pass

    def prim(self):
        pass

    def ab(self):
        pass

# - >
# This is where the grid is received and rendered
def render(maze):
    window.fill([0, 0, 0])
    for row in range(maze.width):
        for column in range(maze.width):
            if maze.grid[row][column][0] == 0:
                pygame.draw.rect(window, (255, 255, 255), pygame.Rect(math.floor(WIDTH/maze.width)*column, math.floor(WIDTH/maze.width)*row, math.floor(WIDTH/maze.width), math.floor(WIDTH/maze.width)))
            elif maze.grid[row][column][0] == 3:
                pygame.draw.rect(window, (0, 255, 255), pygame.Rect(math.floor(WIDTH/maze.width)*column, math.floor(WIDTH/maze.width)*row, math.floor(WIDTH/maze.width), math.floor(WIDTH/maze.width)))
            elif maze.grid[row][column][0] == 2:
                pygame.draw.rect(window, (0, 0, 255), pygame.Rect(math.floor(WIDTH/maze.width)*column, math.floor(WIDTH/maze.width)*row, math.floor(WIDTH/maze.width), math.floor(WIDTH/maze.width)))

    pygame.display.flip()
    
def main():

    maze = Maze(widthMaze)
    maze.generate("DepthFirst")

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    maze.depthFirstSearch()

main()