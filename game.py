import pygame
from menu import Menu
import asyncio
class Game:
    def __init__(self) -> None:
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.actual_level = Menu(self.screen)
        self.fps = 60

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.actual_level.draw()

    async def run(self):
        while True:
            dt = self.clock.tick(self.fps) / 1000
            self.actual_level.update(dt)
            self.draw()
            pygame.display.flip()