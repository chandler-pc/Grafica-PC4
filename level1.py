from enum import Enum
import random
import pygame
import pymunk
import pymunk.pygame_util
from animator import Animator
from player import Player, Direction
from player_interface import PlayerInterface
from utils import LevelState

keys = {
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT
}


class Level1:
    def __init__(self, screen):
        level_name = "ANGRY"
        pygame.display.set_caption(level_name)
        self.screen = screen
        self.running = True
        self.player_interface = PlayerInterface(screen)
        self.player_interface.set_level_name(level_name)
        self.player = Player((100, 100), self.player_interface)
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space.add(self.player.body, self.player.shape)
        self.platforms = []
        self.load_map()
        self.manager = ManagerLevel1(
            self.space, self.player, self.player_interface)

        handler = self.space.add_collision_handler(1, 2)
        handler.begin = self.on_ground_begin
        handler.separate = self.on_ground_end
        handler_platform = self.space.add_collision_handler(1, 3)
        handler_platform.pre_solve = self.on_platform
        handler_platform.begin = self.on_ground_begin
        handler_platform.separate = self.on_ground_end

        handler_dragon_platform = self.space.add_collision_handler(4, 3)
        handler_dragon_platform.begin = self.ignore_collision

        handler_dragon_log = self.space.add_collision_handler(4, 5)
        handler_dragon_log.begin = self.ignore_collision

        handler_platform_log = self.space.add_collision_handler(3, 5)
        handler_platform_log.begin = self.ignore_collision

        handler_ground_log = self.space.add_collision_handler(2, 5)
        handler_ground_log.begin = self.ignore_collision

        handler_wall = self.space.add_collision_handler(1, 6)
        handler_wall.begin = self.only_collision

        handler_dragon_wall = self.space.add_collision_handler(4, 6)
        handler_dragon_wall.begin = self.ignore_collision

        handler_log_player = self.space.add_collision_handler(1, 5)
        handler_log_player.begin = self.on_log_hit_player

        handler_player_dragon = self.space.add_collision_handler(1, 4)
        handler_player_dragon.begin = self.on_player_hit_dragon
        handler_player_dragon.pre_solve = self.ignore_collision

        handler_fireball_platform = self.space.add_collision_handler(7, 3)
        handler_fireball_platform.begin = self.ignore_collision

        handler_fireball_wall = self.space.add_collision_handler(7, 6)
        handler_fireball_wall.begin = self.ignore_collision

        handler_fireball_player = self.space.add_collision_handler(1, 7)
        handler_fireball_player.begin = self.on_fireball_hit_player

    def on_player_hit_dragon(self, arbiter, space, data):
        self.player.take_damage()
        return True

    def on_log_hit_player(self, arbiter, space, data):
        self.player.take_damage()
        log_shape = arbiter.shapes[1]
        for log in self.manager.logs:
            if log.shape == log_shape:
                log.destroy()
                break
        return True
    
    def on_fireball_hit_player(self, arbiter, space, data):
        self.player.take_damage()
        fireball_shape = arbiter.shapes[1]
        for fireball in self.manager.fireballs:
            if fireball.shape == fireball_shape:
                self.manager.remove_fireball(fireball)
                break
        return True

    def on_ground_begin(self, arbiter, space, data):
        self.player.is_air = False
        return True

    def on_ground_end(self, arbiter, space, data):
        self.player.is_air = True
        return True

    def on_platform(self, arbiter, space, data):
        player_shape = arbiter.shapes[0]
        platform_shape = arbiter.shapes[1]
        if player_shape.body.position.y > platform_shape.body.position.y:
            return False
        return True

    def ignore_collision(self, arbiter, space, data):
        return False
    
    def only_collision(self, arbiter, space, data):
        return True

    def load_map(self):
        ground = ((-200, 550), (1400, 550), 2, 0.5, 0.5)
        start, end, thickness, elasticity, friction = ground
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, start, end, thickness)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = 2
        self.space.add(body, shape)
        for _ in range(2):
            wall = ((800 * _, 0), (800 * _, 600), 2, 0.5, 0.5)
            start, end, thickness, elasticity, friction = wall
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            shape = pymunk.Segment(body, start, end, thickness)
            shape.elasticity = elasticity
            shape.friction = friction
            shape.collision_type = 6
            self.space.add(body, shape)
        platforms = [
            ((200, 400), (100, 10)),
            ((400, 300), (100, 10)),
            ((600, 200), (100, 10)),
        ]
        for pos, size in platforms:
            platform = Platform(pos, size)
            self.platforms.append(platform)
            self.space.add(platform.body, platform.shape)

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
                if event.key == pygame.K_q:
                    self.player.attack(self.manager.dragon_boss)
            if event.type == pygame.KEYUP:
                if event.key in keys.keys():
                    if self.player.direction == keys[event.key]:
                        self.player.set_stop()

    def update(self, dt):
        self.handle_events()
        self.player.update(dt)
        self.space.step(dt)
        self.manager.update(dt)

    def draw(self):
        for platform in self.platforms:
            platform.draw(self.screen)
        self.player.draw(self.screen)
        self.manager.draw(self.screen)
        self.player_interface.draw()
        #self.space.debug_draw(self.draw_options)

class FallenLogObstacle:
    def __init__(self, position, time_alive):
        self.position = [*position]
        self.body = pymunk.Body(
            10, float("inf"), body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(self.position[0], self.position[1])
        self.shape = pymunk.Poly.create_box(self.body, size=(20, 5))
        self.shape.elasticity = 0.1
        self.shape.friction = 1.
        self.shape.collision_type = 5
        self.time_alive = time_alive

    def update(self, dt):
        self.time_alive -= dt

    def destroy(self):
        self.time_alive = 0

    def is_alive(self):
        return self.time_alive > 0

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 25, 30), (self.body.position[0]-10, self.body.position[1], 20, 5))


class ManagerLevel1:
    def __init__(self, space, player, player_interface):
        self.level_state = LevelState.FIRST_PART
        self.first_part_time = 30
        self.is_first_part = True
        self.player_interface = player_interface
        self.space = space
        self.player = player
        self.logs = []
        self.fireballs = []
        self.log_alive_time = 2
        self.log_spawn_time = (0.1, 0.8)
        self.log_spawn_delta = random.uniform(*self.log_spawn_time)
        self.dragon_boss = DragonBoss((1000, 100), self)
        self.space.add(self.dragon_boss.body, self.dragon_boss.shape)
        self.player_interface.set_stage_text(str(self.first_part_time))
        self.player_interface.set_help_text("Dodge the logs")
        self.player_interface.set_life_text("Life " + str(self.player.life))

    def add_fireball(self, fireball):
        self.fireballs.append(fireball)
        self.space.add(fireball.body, fireball.shape)

    def update(self, dt):
        if self.level_state == LevelState.FIRST_PART or len(self.logs) > 0:
            self.first_part_logic(dt)
        elif self.level_state == LevelState.SECOND_PART:
            self.second_part_logic(dt)

        for fireball in self.fireballs:
            fireball.update(dt)
            if not fireball.is_alive():
                self.remove_fireball(fireball)

    def generate_log(self):
        self.logs.append(FallenLogObstacle(
            (random.randint(20, 780), 0), self.log_alive_time))
        self.space.add(self.logs[-1].body, self.logs[-1].shape)

    def remove_log(self, log):
        self.space.remove(log.body, log.shape)
        self.logs.remove(log)

    def remove_all_logs(self):
        for log in self.logs:
            self.remove_log(log)

    def first_part_logic(self, dt):
        if self.first_part_time <= 0:
            self.player_interface.set_stage_text("BOSS FIGHT!")
            self.remove_all_logs()
            self.player_interface.set_help_text("Press Q to calm")
            self.level_state = LevelState.SECOND_PART
            return
        for log in self.logs:
            log.update(dt)
            if not log.is_alive():
                self.remove_log(log)
        if self.log_spawn_delta <= 0:
            self.generate_log()
            self.log_spawn_delta = random.uniform(*self.log_spawn_time)
        self.log_spawn_delta -= dt
        self.first_part_time -= dt
        self.player_interface.set_stage_text(str(int(self.first_part_time)))

    def second_part_logic(self, dt):
        self.dragon_boss.update(dt, self.player.body.position)

    def remove_fireball(self, fireball):
        self.space.remove(fireball.body, fireball.shape)
        self.fireballs.remove(fireball)

    def draw(self, screen):
        for log in self.logs:
            log.draw(screen)
        for fireball in self.fireballs:
            fireball.draw(screen)
        self.dragon_boss.draw(screen)


class DragonBoss:
    class State(Enum):
        MOVING = 1
        ATTACKING = 2
        HURT = 3
        DEATH = 4

    def __init__(self, position, manager):
        self.size = (184, 120)
        self.position = [*position]
        self.body = pymunk.Body(100, float("inf"), body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(self.position[0], self.position[1])
        self.shape = pymunk.Poly.create_box(self.body, size=(self.size[0]-80,self.size[1]-40))
        self.shape.elasticity = 0.1
        self.shape.friction = 1.0
        self.shape.collision_type = 4
        self.facing_right = True
        self.animator = Animator("dragon", self.size,0.3)
        self.animator.update_animation("walk")
        self.manager = manager

        self.state = DragonBoss.State.MOVING
        self.state_timer = random.uniform(2.0, 5.0)
        self.velocity = 1000
        self.fireball_cooldown = 0

        self.life = 10

        self.blink_time = 0
        self.blink_duration = 1.0
        self.blink_interval = 0.1
        self.is_blinking = False
        self.visible = True
        self.is_dead = False

    def ignore_collision(self, arbiter, space, data):
        return False

    def update(self, dt, player_position):
        self.animator.update(dt)
        if self.is_dead:
            return
        self.state_timer -= dt
        self.fireball_cooldown -= dt

        if self.state_timer <= 0:
            if self.state == DragonBoss.State.MOVING:
                self.state = DragonBoss.State.ATTACKING
                self.fireball_cooldown = random.uniform(0.3,0.5)
            else:
                self.state = DragonBoss.State.MOVING
            self.state_timer = random.uniform(2.0, 5.0)

        if self.state == DragonBoss.State.MOVING:
            self.move_towards_player(player_position)
        elif self.state == DragonBoss.State.ATTACKING:
            self.attack(player_position)

        if self.is_blinking:
            self.blink_time -= dt
            if self.blink_time <= 0:
                self.is_blinking = False
                self.state = DragonBoss.State.ATTACKING
                self.animator.update_animation("idle")
            else:
                self.visible = int(self.blink_time / self.blink_interval) % 2 == 0
        else:
            self.visible = True

    def move_towards_player(self, player_position):
        tolerance = 10

        if abs(player_position[0] - self.body.position.x) > tolerance:
            if player_position[0] > self.body.position.x:
                self.body.apply_impulse_at_local_point((self.velocity, 0))
                self.facing_right = True
            elif player_position[0] < self.body.position.x:
                self.body.apply_impulse_at_local_point((-self.velocity, 0))
                self.facing_right = False


    def attack(self, player_position):
        if self.fireball_cooldown <= 0:
            fireball = Fireball(self.body.position, player_position)
            self.manager.add_fireball(fireball)
            self.fireball_cooldown = random.uniform(0.3,0.5)

    def draw(self, screen):
        if self.visible:
            x, y = self.body.position
            self.animator.animate(x, y, screen, self.facing_right)

    def take_damage(self):
        self.life -= 1
        self.animator.update_animation("hurt")
        self.state = DragonBoss.State.HURT
        if self.life <= 0:
            self.die()
        else:
            self.is_blinking = True
            self.blink_time = self.blink_duration

    def die(self):
        print("Dragon has been defeated!")
        self.animator.update_animation("death")
        self.state = DragonBoss.State.DEATH
        self.is_dead = True
        handle_dragon_ground = self.manager.space.add_collision_handler(4, 2)
        handle_dragon_ground.pre_solve = self.ignore_collision
        self.manager.player_interface.set_stage_text("VICTORY!")

    def ignore_collision(self, arbiter, space, data):
        return False


class Platform:
    def __init__(self, position, size):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = 0.5
        self.shape.friction = 0.5
        self.shape.collision_type = 3

    def draw(self, screen):
        vertices = self.shape.get_vertices()
        vertices = [(self.body.position.x + v.x, self.body.position.y + v.y)
                    for v in vertices]
        pygame.draw.polygon(screen, (0, 255, 0), vertices, 1)

class Fireball:
    def __init__(self, position, target_position):
        self.body = pymunk.Body(0.0001, float("inf"))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.collision_type = 7
        self.shape.elasticity = 0.5
        self.shape.friction = 0.5
        self.life_time = 2

        direction = pymunk.Vec2d(*target_position) - pymunk.Vec2d(*position)
        direction = direction.normalized()
        speed = 400
        self.body.velocity = direction * speed

    def draw(self, screen):
        x, y = self.body.position
        pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 10)

    def update(self, dt):
        self.life_time -= dt
        gravity = 900
        anti_gravity_force = (0, -self.body.mass * gravity)
        self.body.apply_force_at_local_point(anti_gravity_force)

    def is_alive(self):
        return self.life_time > 0