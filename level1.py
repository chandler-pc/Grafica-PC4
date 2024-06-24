import pygame
import pymunk
import pymunk.pygame_util
from player import Player, Direction
from player_interface import PlayerInterface

keys = {
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT
}

class Level1:
    def __init__(self, screen):
        level_name = "ANGRY"
        pygame.display.set_caption(level_name)
        self.screen = screen
        self.player = Player((100,100))
        self.running = True
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space.add(self.player.body, self.player.shape)
        self.first_part_time = 30
        self.is_first_part = True
        self.load_map()
        self.player_interface = PlayerInterface(screen)
        self.player_interface.set_text(level_name)
        self.player_interface.set_timer(str(self.first_part_time))

    def generate_logs(self):
        for i in range(10):
            log = FallenLogObstacle((100 + i * 100, 0))
            self.space.add(log.body, log.shape)

    def change_level_state(self, dt):
        if self.first_part_time <= 0:
            self.is_first_part = False
            return
        self.first_part_time -= dt
        self.player_interface.set_timer(str(int(self.first_part_time)))

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
        self.handle_events()
        self.player.update(dt)
        self.space.step(dt)
        self.change_level_state(dt)

    def draw(self):
        self.player.draw(self.screen)
        self.player_interface.draw()
        self.space.debug_draw(self.draw_options)

class FallenLogObstacle:
    def __init__(self,position):
        self.position = [*position]
        self.body = pymunk.Body(10,float("inf"), body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(self.position[0], self.position[1])
        self.shape = pymunk.Poly.create_box(self.body, size=(20, 5))
        self.shape.elasticity = 0.1
        self.shape.friction = 1.