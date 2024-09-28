import random
import numpy as np


# 0: walkable path 
# 1: wall
# 2: starting point
# 3: goal
class MazeGenerator():
    W = 10
    H = 10
    # down, up, right, left
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    grid = np.empty((H, W), dtype=int)

    def __init__(self):
        self.grid.fill(1)

    def check_neigbhours(self, x, y):
        walls = 0
        for dx, dy in self.DIRECTIONS:
            if self.grid[x + dx][y + dy] == 1:
                walls += 1

        return walls >= 3

    def is_valid_move(self, x, y):
        if 0 < x < self.H - 1 and 0 < y < self.H - 1:
            if self.grid[x][y] == 1: 
                return self.check_neigbhours(x, y)
        return False

    def dfs(self, x, y):
        self.grid[x][y] = 0 

        random.shuffle(self.DIRECTIONS)

        for dx, dy in self.DIRECTIONS:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny):                
                self.grid[nx][ny] = 0                
                self.grid[x + dx//2][y + dy//2] = 0
                self.dfs(nx, ny)

    def print_maze(self):
        for row in self.grid:
            print(''.join(' '+str(row)))

    def generate_maze(self):
        self.dfs(1,1)
        # self.grid[1][1] = 2 #starting point
        # self.grid[8][8] = 3 #starting point
        return self.grid


