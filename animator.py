import pygame
from asset_loader import AssetLoader

class Animator:
    def __init__(self,name, size):
        self.name = name
        self.size = size
        self.sprites = AssetLoader.load_sprite_sheet(name, size=size)
        self.frames_size = {}
        for key in self.sprites.keys():
            if key.split("_")[0] not in self.frames_size:
                self.frames_size[key.split("_")[0]] = 1
            else:
                self.frames_size[key.split("_")[0]] += 1
        self.animation_name = "idle"
        self.sprite = self.sprites['idle_0']
        self.animation_delta = .5
        self.actual_animation_time = self.animation_delta
    
    def update(self, dt):
        self.actual_animation_time -= dt
        if self.actual_animation_time <= 0:
            self.actual_animation_time = self.animation_delta

    def update_animation(self, animation_name):
        self.animation_name = animation_name
        self.actual_animation_time = self.animation_delta

    def animate(self, x, y, screen, flip=False, color=None):
        total_frames = self.frames_size[self.animation_name]
        animation_name = self.animation_name + "_" + str(int((self.actual_animation_time / self.animation_delta) * total_frames) % total_frames)
        self.sprite = self.sprites[animation_name]
        
        if flip:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        else:
            self.sprite = pygame.transform.flip(self.sprite, False, False)

        if color:
            colored_sprite = self.sprite.copy()
            colored_sprite.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(colored_sprite, (x - self.size[0] // 2, y - self.size[1] // 2))
        else:
            screen.blit(self.sprite, (x - self.size[0] // 2, y - self.size[1] // 2))