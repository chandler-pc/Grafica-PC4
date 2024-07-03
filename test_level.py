import time
from text_canvas import TextCanvas
import pygame

class TestLevel:
    def __init__(self,screen):
        self.text_canvas = TextCanvas(screen)
        self.screen = screen

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.text_canvas.add_line()

    def draw(self):
        self.screen.fill((153, 204, 255))
        self.text_canvas.draw()
    
    def update(self, dt):
        self.handle_events()
        self.text_canvas.update(dt)
            