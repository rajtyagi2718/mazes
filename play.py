from maze import Maze
from search import GlobalDFS, GlobalBFS, ShortestPath, GlobalAStar
from gui import GUI

maze = Maze(30, 30)
cell_size = 20

agents = [GlobalAStar, ShortestPath, GlobalBFS, GlobalDFS]

for agent in agents:
    gui = GUI(maze, 20, agent(maze))
    gui.start()
    maze.clear_visits()
