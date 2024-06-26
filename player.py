from enum import Enum
import pymunk
from pymunk.vec2d import Vec2d
from animator import Animator

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3

    def __str__(self) -> str:
        return self.name.lower()

class Player:
    def __init__(self, position, interface) -> None:
        self.player_interface = interface
        self.position = [*position]
        self.velocity = 150
        self.direction = Direction.DOWN
        self.is_moving = False
        self.is_air = True
        self.animator = Animator("player", (48, 48),0.2)

        self.body = pymunk.Body(10,float("inf"), body_type=pymunk.Body.DYNAMIC)
        self.body.position = Vec2d(self.position[0], self.position[1])
        self.shape = pymunk.Poly.create_box(self.body, size=(30, 48))
        self.shape.collision_type = 1 
        self.shape.elasticity = 0.1
        self.shape.friction = 1.

        self.sensor = pymunk.Poly.create_box(self.body, size=(30, 5))
        self.sensor.sensor = True
        self.sensor.collision_type = 2

        self.invincible = False
        self.invincible_timer = 0
        self.invincible_blink_timer = 0
        self.attacking = False
        self.attack_timer = 0
        self.attack_blink_timer = 0

        self.life = 10

    def move(self):
        if not self.is_moving or self.attacking:
            return
        if self.direction == Direction.LEFT:
            self.body.apply_impulse_at_local_point((-self.velocity, 0))
        elif self.direction == Direction.RIGHT:
            self.body.apply_impulse_at_local_point((self.velocity, 0))
        if self.body.velocity.x > self.velocity:
            self.body.velocity = (self.velocity, self.body.velocity.y)
        elif self.body.velocity.x < -self.velocity:
            self.body.velocity = (-self.velocity, self.body.velocity.y)

    def set_direction(self, direction):
        self.direction = direction
        self.is_moving = True
        self.animator.update_animation(str(direction))
    
    def set_stop(self):
        self.is_moving = False
        self.direction = Direction.DOWN
        self.body.velocity = (0, self.body.velocity.y)
        self.animator.update_animation("idle")

    def jump(self):
        if self.is_air or self.attacking:
            return
        self.body.apply_impulse_at_local_point((0, -5500))
        self.is_air = True
    
    def update(self, dt):
        self.move()
        self.animator.update(dt)
        if self.invincible:
            self.invincible_timer -= dt
            self.invincible_blink_timer -= dt
            if self.invincible_blink_timer <= 0:
                self.invincible_blink_timer = 0.1
            if self.invincible_timer <= 0:
                self.invincible = False
        if self.attacking:
            self.attack_timer -= dt
            self.attack_blink_timer -= dt
            if self.attack_blink_timer <= 0:
                self.attack_blink_timer = 0.1
            if self.attack_timer <= 0:
                self.attacking = False

    def draw(self, screen):
        x, y = self.body.position
        if self.invincible and int(self.invincible_timer * 10) % 2 == 0:
            self.animator.animate(x, y, screen, color=(0,0,0))
        elif self.attacking and int(self.attack_timer * 10) % 2 == 0:
            self.animator.animate(x, y, screen, color=(0, 255, 0))
        else:
            self.animator.animate(x, y, screen)

    def take_damage(self):
        if not self.invincible:
            self.life -= 1
            self.invincible = True
            self.invincible_timer = 1.0
            self.invincible_blink_timer = 0.1
            if self.life <= 0:
                self.life = 0
                self.player_interface.set_life_text(f"DEAD")
            else:
                self.player_interface.set_life_text(f"Life {self.life}")

    def attack(self, enemy):
        if not self.attacking and not self.is_air:
            self.attacking = True
            self.attack_timer = 0.5
            enemy.take_damage()