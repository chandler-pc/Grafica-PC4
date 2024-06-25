import random
import pygame
import pymunk
import pymunk.pygame_util
from asset_loader import AssetLoader
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
        self.player = Player((100,100))
        self.running = True
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space.add(self.player.body, self.player.shape)
        self.platforms = []
        self.load_map()
        self.player_interface = PlayerInterface(screen)
        self.player_interface.set_text(level_name)
        self.manager = ManagerLevel1(self)


        handler = self.space.add_collision_handler(1, 2)
        handler.begin = self.on_ground_begin
        handler.separate = self.on_ground_end
        handler_platform = self.space.add_collision_handler(1, 3)
        handler_platform.pre_solve = self.on_platform
        handler_platform.begin = self.on_ground_begin
        handler_platform.separate = self.on_ground_end

        handler_dragon_platform = self.space.add_collision_handler(4, 3)
        handler_dragon_platform.begin = self.ignore_collision

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
            shape.collision_type = 2
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
            if event.type == pygame.KEYUP:
                if event.key in keys.keys():
                    if self.player.direction == keys[event.key]:
                        self.player.set_stop()
                        self.player.update_animation("idle")

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
    def __init__(self,position, time_alive):
        self.position = [*position]
        self.body = pymunk.Body(10,float("inf"), body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(self.position[0], self.position[1])
        self.shape = pymunk.Poly.create_box(self.body, size=(20, 5))
        self.shape.elasticity = 0.1
        self.shape.friction = 1.
        self.time_alive = time_alive

    def update(self,dt):
        self.time_alive -= dt

    def is_alive(self):
        return self.time_alive > 0
    
    def draw(self,screen):
        pygame.draw.rect(screen,(139,25, 30),(*self.body.position,20,5))
        

class ManagerLevel1:
    def __init__(self, level1):
        self.level_state = LevelState.SECOND_PART
        self.first_part_time = 5
        self.is_first_part = True
        self.level1 = level1
        self.level1.player_interface.set_timer(str(self.first_part_time))
        self.logs = []
        self.log_alive_time = 2
        self.log_spawn_time = (0.1,0.8)
        self.log_spawn_delta = random.uniform(*self.log_spawn_time)
        self.dragon_boss = DragonBoss((400,100))
        self.level1.space.add(self.dragon_boss.body,self.dragon_boss.shape)

    def update(self,dt):
        if self.level_state == LevelState.FIRST_PART or len(self.logs) > 0:
            self.first_part_logic(dt)
        elif self.level_state == LevelState.SECOND_PART:
            self.second_part_logic(dt)

    def generate_log(self):
        self.logs.append(FallenLogObstacle((random.randint(20,780),0),self.log_alive_time))
        self.level1.space.add(self.logs[-1].body,self.logs[-1].shape)
    
    def remove_log(self,log):
        self.level1.space.remove(log.body,log.shape)
        self.logs.remove(log)

    def remove_all_logs(self):
        for log in self.logs:
            self.remove_log(log)

    def first_part_logic(self,dt):
            if self.first_part_time <= 0:
                self.remove_all_logs()
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
            self.level1.player_interface.set_timer(str(int(self.first_part_time)))

    def second_part_logic(self,dt):
        self.dragon_boss.update(dt, self.level1.player.body.position)

    def draw(self,screen):
        for log in self.logs:
            log.draw(screen)
        self.dragon_boss.draw(screen)

class DragonBoss:
    def __init__(self,position):
        self.size = (184,120)
        self.position = [*position]
        self.body = pymunk.Body(10000,float("inf"), body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(self.position[0], self.position[1])
        self.shape = pymunk.Poly.create_box(self.body, size=self.size)
        self.shape.elasticity = 0.1
        self.shape.friction = 1.
        self.shape.collision_type = 4
        self.facing_right = True

        self.sprites = AssetLoader.load_sprite_sheet("rat", size=self.size)
        self.animation_name = "idle_rat_"
        self.sprite = self.sprites['idle_rat_0']
        self.animation_delta = .5
        self.actual_animation_time = self.animation_delta

    def update(self,dt,player_position):
        self.actual_animation_time -= dt
        if self.actual_animation_time <= 0:
            self.actual_animation_time = self.animation_delta
        if player_position[0] > self.body.position.x:
            self.facing_right = True
        else:
            self.facing_right = False
    
    def update_animation(self, animation_name):
        self.animation_name = animation_name + "_" + str(self.direction) + "_"
        self.actual_animation_time = self.animation_delta

    def draw(self,screen):
        x, y = self.body.position
        self.animate()
        if self.facing_right:
            sprite_to_draw = self.sprite
        else:
            sprite_to_draw = pygame.transform.flip(self.sprite, True, False)
        screen.blit(sprite_to_draw, ((x-self.size[0]/2), y-self.size[1]/2))

    def animate(self):
        animation_name = self.animation_name + str(int((self.actual_animation_time / self.animation_delta) * 2) % 2)
        self.sprite = self.sprites[animation_name]

class Platform:
    def __init__(self, position, size):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = 0.1
        self.shape.friction = 1.0
        self.shape.collision_type = 3
    
    def draw(self, screen):
        vertices = self.shape.get_vertices()
        vertices = [(self.body.position.x + v.x, self.body.position.y + v.y) for v in vertices]
        pygame.draw.polygon(screen, (0, 255, 0), vertices, 1)