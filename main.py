import pygame
from level1 import Level1

pygame.init()

class World:
    def __init__(self) -> None:
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.actual_level = Level1(self.screen)
        self.fps = 60

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.actual_level.draw()

    def run(self):
        while True:
            dt = self.clock.tick(self.fps) / 1000
            self.actual_level.handle_events()
            self.actual_level.update(dt)
            self.draw()
            pygame.display.flip()

game = World()
game.run()