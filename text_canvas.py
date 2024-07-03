import pygame
import json
import time

from asset_loader import AssetLoader
from utils import Manager


class TextCanvas:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("easvhs.ttf", 28)
        data = open(f"level1_{Manager.get_language()}.json").read()
        self.text = json.loads(data)
        self.paragraphs = self.text["initial"]
        self.lines = ["", "", "", ""]
        self.index = 0
        self.line_index = 0
        self.current_line = ""
        self.char_index = 0
        self.last_update_time = time.time()
        self.char_delay = 0.03
        self.is_writing = False
        self.down_arrow = AssetLoader.load_image("DownArrow.png")
        self.down_arrow = pygame.transform.scale(self.down_arrow, (34, 18))
        self.down_arrow_y = 580
        self.down_arrow_direction = 1
        self.down_arrow_speed = 1
        self.arrow_visible = False
        self.end_text = False
        self.delay_to_text = 0.5

    def add_line(self):
        if self.end_text:
            return False
        
        if self.is_writing:
            self.lines[self.line_index - 1] = self.current_line

        if self.line_index == 4:
            for i in range(4):
                self.lines[i] = ""
            self.line_index = 0
            self.index += 1
            self.current_line = ""
            self.char_index = 0
            self.arrow_visible = False
        if self.index == len(self.paragraphs):
            self.end_text = True
            return False
        self.current_line = self.paragraphs[self.index]['lines'][self.line_index]
        self.line_index += 1
        self.char_index = 0
        self.is_writing = True
        return True

    def update(self,dt):
        if self.end_text:
            return
        
        if self.delay_to_text > 0:
            self.delay_to_text -= dt
            if self.delay_to_text <= 0:
                self.add_line()

        current_time = time.time()
        if current_time - self.last_update_time > self.char_delay:
            self.last_update_time = current_time
            if self.char_index < len(self.current_line):
                self.lines[self.line_index -
                           1] += self.current_line[self.char_index]
                self.char_index += 1
            else:
                if self.is_writing:
                    self.is_writing = False
                    if self.line_index != 4:
                        self.add_line()
                    else:
                        self.arrow_visible = True

        self.down_arrow_y += self.down_arrow_speed * self.down_arrow_direction
        if self.down_arrow_y > 590 or self.down_arrow_y < 570:
            self.down_arrow_direction *= -1

    def draw(self):
        if self.end_text:
            return
        s = pygame.Surface((800, 208), pygame.SRCALPHA)
        s.fill((0,0,0,153))
        self.screen.blit(s, (0, 400))
        for i, line in enumerate(self.lines):
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (50, 420 + i * 45))
        if self.arrow_visible:
            self.screen.blit(self.down_arrow, (750, self.down_arrow_y))

    def update_paragraphs(self, key):
        self.paragraphs = self.text[key]
        self.index = 0
        self.line_index = 0
        self.current_line = ""
        self.char_index = 0
        self.last_update_time = time.time()
        self.arrow_visible = False
        self.end_text = False
        self.lines = ["", "", "", ""]
        self.is_writing = False
        self.delay_to_text = 0.5
