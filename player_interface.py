import pygame

class PlayerInterface:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/easvhs.ttf", 28)
        self.color = (255,255,255)
        self.level_name = ""
        self.level_name_rect = None
        self.stage_text = "00"
        self.stage_text_rect = None
        self.help_text = ""
        self.help_text_rect = None
        self.life_text = ""
        self.life_text_rect = None

    def set_level_name(self, text):
        self.level_name = text
        self.level_name_rect = self.font.render(self.level_name, True, self.color).get_rect(midtop=(self.screen.get_width() / 2, 10))

    def set_stage_text(self, stage_text):
        self.stage_text = stage_text
        self.stage_text_rect = self.font.render(self.stage_text, True, self.color).get_rect(topleft=(10, 10))

    def set_help_text(self, help_text):
        self.help_text = help_text
        self.help_text_rect = self.font.render(self.help_text,True,self.color).get_rect(topright=(self.screen.get_width()-10, 10))

    def set_life_text(self, life_text):
        self.life_text = life_text
        self.life_text_rect = self.font.render(self.life_text, True, self.color).get_rect(bottomleft=(10, self.screen.get_height()-10))

    def draw(self):
        self.screen.blit(self.font.render(self.stage_text, True, self.color), self.stage_text_rect)
        self.screen.blit(self.font.render(self.level_name, True, self.color), self.level_name_rect)
        self.screen.blit(self.font.render(self.help_text, True, self.color), self.help_text_rect)
        self.screen.blit(self.font.render(self.life_text, True, self.color), self.life_text_rect)