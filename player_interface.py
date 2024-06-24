import pygame

class PlayerInterface:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/easvhs.ttf", 28)
        self.color = (255,255,255)
        self.level_name = ""
        self.level_name_rect = None
        self.timer = "00"
        self.timer_rect = None

    def set_text(self, text):
        self.level_name = text
        self.level_name_rect = self.font.render(self.level_name, True, self.color).get_rect(center=(self.screen.get_width() / 2, 25))

    def set_timer(self, timer):
        self.timer = timer
        self.timer_rect = self.font.render(self.timer, True, self.color).get_rect(center=(self.screen.get_width() - 50, 25))

    def draw(self):
        self.screen.blit(self.font.render(self.timer, True, self.color), self.timer_rect)
        self.screen.blit(self.font.render(self.level_name, True, self.color), self.level_name_rect)

    def update(self):
        pass