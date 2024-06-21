import pygame
import pymunk
import pymunk.pygame_util
from player import *

keys = {
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT
}

class Level1:
    def __init__(self, screen) -> None:
        pygame.display.set_caption("Level 1 - IRA")
        self.screen = screen
        self.player = Player()
        self.running = True
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space.add(self.player.body, self.player.shape)
        self.load_map()

    def load_map(self, segments=None):
        if segments is None:
            segments = [
                ((0, 500), (800, 500), 5, 0.5, 0.5)
            ]
        for segment in segments:
            start, end, thickness, elasticity, friction = segment
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            shape = pymunk.Segment(body, start, end, thickness)
            shape.elasticity = elasticity
            shape.friction = friction
            self.space.add(body, shape)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in keys.keys():
                    self.player.set_direction(keys[event.key])
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key in keys.keys():
                    if self.player.direction == keys[event.key]:
                        self.player.set_stop()
                        self.player.update_animation("idle")

    def update(self, dt):
        self.player.update(dt)
        self.space.step(dt)

    def draw(self):
        self.player.draw(self.screen)
        #self.space.debug_draw(self.draw_options)