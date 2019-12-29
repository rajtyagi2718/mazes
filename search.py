from collections import deque

class Agent:

    def __init__(self, maze, name):
        self.name = name
        self.maze = maze
        self.curr = self.maze.source
        self.data = None
        self.target_found = False

    def is_terminal(self):
        return self.target_found or not self.data

    def search(self):
        """Explore maze by visiting cells adjacent to current until target is reached."""

class GlobalAgent(Agent):

    def search(self):
        """Explore maze from global pov. Agent can jump between previously visited cells. Target coordinates are known."""


class GlobalDFS(GlobalAgent):

    def __init__(self, maze):
        super().__init__(maze, 'global_dfs')
        self.data = [self.curr]
        self.search()

    def search(self):
        if self.is_terminal():
            return
        self.curr = self.data.pop()
        self.maze.add_visit(self.curr)
        self.target_found = self.curr == self.maze.target
        if self.maze.visits(self.curr) == 1:
            self.data.extend(c for c in self.maze.adjacent_cells(self.curr)
                               if not self.maze.visits(c))
        else:
            self.search()

class GlobalBFS(GlobalAgent):

    def __init__(self, maze):
        super().__init__(maze, 'global_bfs')
        self.data = deque([self.curr])
        self.search()

    def search(self):
        if self.is_terminal():
            return
        self.curr = self.data.popleft()
        self.maze.add_visit(self.curr)
        self.target_found = self.curr == self.maze.target
        if self.maze.visits(self.curr) == 1:
            self.data.extend(c for c in self.maze.adjacent_cells(self.curr)
                               if not self.maze.visits(c))
        else:
            self.search()

from heapq import heappush, heappop, heapify

class GlobalAStar(GlobalAgent):

    def __init__(self, maze):
        super().__init__(maze, 'global_astar')
        self.data = [(0, self.curr)]
        self.data_set = set((self.curr,))
        self.search()

    def heuristic(self, cell):
        target = self.maze.target
        return abs(cell[0]-target[0]) + abs(cell[1]-target[1])

    def search(self):
        if self.is_terminal():
            return

        dist, self.curr = heappop(self.data)
        self.data_set.remove(self.curr)
        self.maze.add_visit(self.curr)
        self.target_found = self.curr == self.maze.target

        for adj in self.maze.adjacent_cells(self.curr):
            if not self.maze.visits(adj):
                adj_dist = dist + self.heuristic(adj)
                if adj in self.data_set:
                    i = self.data.index(adj)
                    if self.data[i][0] > adj_dist:
                        self.data[i][0] = adj_dist
                        heapify(self.data)
                else:
                    heappush(self.data, (adj_dist, adj))
                    self.data_set.add(adj)


class ShortestPath(GlobalAgent):

    def __init__(self, maze):
        super().__init__(maze, 'global_shortest_path')
        self.data = deque([self.curr])
        self.prev = {self.curr:None}
        self.pos = -1
        self.explore()
        self.backtrack_path()

    def search(self):
        if self.is_terminal():
            return
        self.pos += 1
        if self.pos == len(self.data):
            self.target_found = True
        else:
            self.curr = self.data[self.pos]
            self.maze.add_visit(self.curr)

    def explore(self):
        while self.data:
            self.curr = self.data.popleft()
            if self.curr == self.maze.target:
                break
            if not self.maze.visits(self.curr):
                adj = [c for c in self.maze.adjacent_cells(self.curr)
                         if not self.maze.visits(c)]
                self.prev.update((c, self.curr) for c in adj)
                self.data.extend(adj)
            self.maze.add_visit(self.curr)

    def backtrack_path(self):
        self.data = []
        while self.curr:
            self.data.append(self.curr)
            self.curr = self.prev[self.curr]
        self.data.reverse()
        self.curr = self.maze.source
        self.maze.clear_visits()
