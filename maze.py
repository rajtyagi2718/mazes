import numpy as np
import random

class Maze:

    # walls[i][j] = [top, bottom, left, right, visits]
    shared_wall = {0:1, 1:0, 2:3, 3:2}

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.data = np.ones((height, width, 5), int)
        self.source = (height // 2, width // 2)
        self.target = None
        self.init_target()
        self.dfs()
        self.total_cells = height * width

    def init_target(self):
        edge = random.randrange(4)
        if edge < 2:
            i = random.randrange(self.height)
            j = 0 if not edge else self.width-1
        else:
            i = 0 if edge == 2 else self.height-1
            j = random.randrange(self.width)
        self.target = (i, j)

    ## walls ##

    def top_wall(self, c):
        return self.data[c[0]][c[1]][0]

    def bottom_wall(self, c):
        return self.data[c[0]][c[1]][1]

    def left_wall(self, c):
        return self.data[c[0]][c[1]][2]

    def right_wall(self, c):
        return self.data[c[0]][c[1]][3]

    def remove_wall(self, c, w):
        self.data[c[0]][c[1]][w] = 0

    def get_shared_wall(self, w):
        return self.shared_wall[w]

    ## cells ##

    def top_cell(self, c):
        return (c[0]-1, c[1])

    def bottom_cell(self, c):
        return (c[0]+1, c[1])

    def left_cell(self, c):
        return (c[0], c[1]-1)

    def right_cell(self, c):
        return (c[0], c[1]+1)

    def adjacent_cells(self, c):
        ret = []
        if not self.top_wall(c):
            ret.append(self.top_cell(c))
        if not self.bottom_wall(c):
            ret.append(self.bottom_cell(c))
        if not self.left_wall(c):
            ret.append(self.left_cell(c))
        if not self.right_wall(c):
            ret.append(self.right_cell(c))
        return ret

    def adjacent_cell_walls(self, c):
        ret = []
        if c[0]:
            ret.append((self.top_cell(c), 0))
        if c[0] < self.height-1:
            ret.append((self.bottom_cell(c), 1))
        if c[1]:
            ret.append((self.left_cell(c), 2))
        if c[1] < self.width-1:
            ret.append((self.right_cell(c), 3))
        return ret

    ## visits ##

    def visits(self, c):
        return self.data[c[0]][c[1]][4]

    def add_visit(self, c):
        self.data[c[0]][c[1]][4] += 1

    def remove_visit(self, c):
        self.data[c[0]][c[1]][4] -= 1

    def clear_visits(self):
        self.data[:,:,4] = 0

    def total_visits(self):
        return np.sum(self.data[:,:,4])

    ## search ##

    def dfs(self):
        self.search(self.source)
        cells = [(i,j) for i in range(self.height) for j in range(self.width)]
        random.shuffle(cells)
        for c in cells:
            if self.visits(c):
                self.search(c)

    def search(self, c):
        self.remove_visit(c)
        adj = self.adjacent_cell_walls(c)
        random.shuffle(adj)
        for d,w in adj:
            if self.visits(d):
                self.remove_wall(c, w)
                self.remove_wall(d, self.get_shared_wall(w))
                self.search(d)
