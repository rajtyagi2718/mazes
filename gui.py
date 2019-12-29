import pygame
from pygame import Color

class GUI:

    def __init__(self, maze, cell_size, agent):
        self.maze = maze
        self.agent = agent

        pygame.init()
        pygame.display.set_caption('Maze')
        self.cell_size = cell_size
        self.wall_size = cell_size // 5
        self.surface = pygame.display.set_mode((self.maze.width * cell_size,
                                                self.maze.height * cell_size))
        self.clock = pygame.time.Clock()

    def start(self):
        self.main_loop()

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if self.agent.is_terminal():
                break

            self.update()
            self.clock.tick(60)
        self.end_loop()

    def end_loop(self):
        if self.agent.target_found:
            print('maze solved!')
        print('%s: %d visits' % (self.agent.name, self.maze.total_visits()))
        self.pause_loop(3)
        pygame.quit()

    def pause_loop(self, sec):
        for _ in range(int(sec*60)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.clock.tick(60)

    def update(self):
        self.agent.search()
        self.surface.fill(Color('white'))
        self.draw_objects()
        pygame.display.flip()

    def draw_objects(self):
        self.draw_cells()
        self.draw_walls()

    def visit_color(self, n):
        return (255-70*n, 255-70*n, 255)

    def draw_cells(self):
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.maze.visits((i,j)):
                    color = self.visit_color(self.maze.visits((i,j)))
                    y, x = i*self.cell_size, j*self.cell_size
                    rect = (x, y, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.surface, color, rect)

        # source
        y,x = (k*self.cell_size for k in self.maze.source)
        rect = (x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.surface, Color('yellow'), rect)

        # target
        y,x = (k*self.cell_size for k in self.maze.target)
        rect = (x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.surface, Color('red'), rect)

    def draw_walls(self):
        # draw left and top walls
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                y, x = i*self.cell_size, j*self.cell_size
                if self.maze.left_wall((i,j)):
                    pygame.draw.line(self.surface, Color('black'),
                                   (x,y), (x,y+self.cell_size), self.wall_size)
                if self.maze.top_wall((i,j)):
                    pygame.draw.line(self.surface, Color('black'),
                                   (x,y), (x+self.cell_size,y), self.wall_size)

        # draw right and bottom border walls
        y = self.maze.height * self.cell_size
        x = self.maze.width * self.cell_size
        pygame.draw.line(self.surface, Color('black'), (x,0), (x,y), self.wall_size)
        pygame.draw.line(self.surface, Color('black'), (0,y), (x,y), self.wall_size)
