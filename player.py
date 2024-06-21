from enum import Enum
import pymunk
from asset_loader import AssetLoader
from pymunk.vec2d import Vec2d

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3

    def __str__(self) -> str:
        return self.name.lower()

class Player:
    def __init__(self) -> None:
        self.position = [0,0]
        self.velocity = 100
        self.direction = Direction.DOWN
        self.is_moving = False
        self.sprites = AssetLoader.load_sprite_sheet("player_walk", size=(48,48))
        self.animation_name = "idle_down_"
        self.sprite = self.sprites['idle_down_0']
        self.animation_delta = .5
        self.actual_animation_time = self.animation_delta
        self.is_air = False


        self.body = pymunk.Body(10,float("inf"), body_type=pymunk.Body.DYNAMIC)
        self.body.position = Vec2d(self.position[0], self.position[1])
        self.shape = pymunk.Poly.create_box(self.body, size=(48, 48))
        self.shape.elasticity = 0.1
        self.shape.friction = 1.

    def move(self):
        if not self.is_moving:
            return
        if self.direction == Direction.LEFT:
            self.body.velocity = (-self.velocity, self.body.velocity.y)
        elif self.direction == Direction.RIGHT:
            self.body.velocity = (self.velocity, self.body.velocity.y)

    def set_direction(self, direction):
        self.direction = direction
        self.is_moving = True
        self.update_animation("walk")
    
    def set_stop(self):
        self.is_moving = False
        self.direction = Direction.DOWN
        self.body.velocity = (0, self.body.velocity.y)

    def jump(self):
        if self.is_air:
            return
        self.body.apply_impulse_at_local_point((0, -5000))
        self.is_air = True
        print("Jump")
    
    def update(self, dt):
        self.move()
        self.actual_animation_time -= dt
        if self.actual_animation_time <= 0:
            self.actual_animation_time = self.animation_delta

    def update_animation(self, animation_name):
        self.animation_name = animation_name + "_" + str(self.direction) + "_"
        self.actual_animation_time = self.animation_delta

    def draw(self, screen):
        x, y = self.body.position
        self.animate()
        screen.blit(self.sprite, (x-24, y-24))

    def animate(self):
        animation_name = self.animation_name + str(int((self.actual_animation_time / self.animation_delta) * 2) % 2)
        self.sprite = self.sprites[animation_name]