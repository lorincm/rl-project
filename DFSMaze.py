import random
import numpy as np


# 0: walkable path 
# 1: wall
# 2: starting point
# 3: goal
class MazeGenerator():
    WIDTH = 10
    HEIGHT = 10
    # down, up, right, left
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    grid = np.empty((HEIGHT, WIDTH), dtype=int)

    def __init__(self):
        self.grid.fill(1)

    def check_neigbours(self, x, y):
        walls = 0
        for dirx, diry in self.DIRECTIONS:
            if self.grid[x + dirx][y + diry] == 1:
                walls += 1

        return walls >= 3

    def valid_move(self, x, y):
        if 0 < x < self.HEIGHT - 1 and 0 < y < self.HEIGHT - 1:
            if self.grid[x][y] == 1: 
                return self.check_neigbours(x, y)
        return False

    def dfs(self, x, y):
        self.grid[x][y] = 0 

        random.shuffle(self.DIRECTIONS)

        for dirx, diry in self.DIRECTIONS:
            nextx, nexty = x + dirx, y + diry
            if self.valid_move(nextx, nexty):                
                self.grid[nextx][nexty] = 0                
                self.grid[x + dirx//2][y + diry//2] = 0
                self.dfs(nextx, nexty)

    def print_maze(self):
        for row in self.grid:
            print(''.join(' '+str(row)))

    def generate_maze(self):
        # us to generate maze
        # self.dfs(1,1)

        # static maze from the assignment 
        self.grid = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 3, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 4, 1],
            [1, 0, 0, 0, 0, 0, 1, 5, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ])

        return self.grid


