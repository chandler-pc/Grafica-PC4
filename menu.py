import pygame
from level1 import Level1
from manager import Manager

class Menu:
    def __init__(self,screen):
        self.screen = screen
        pygame.display.set_caption("Menu")
        self.button = Button(self.screen,"Start",100,100,100,50)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.button.draw()

    def update(self,dt):
        self.handle_events()
        self.button.update()
        pass

class Button:
    def __init__(self,screen,text,x,y,width,height):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.color = (255,255,255)
        self.hover_color = (200,200,200)
        self.clicked_color = (150,150,150)
        self.is_clicked = False

    def draw(self):
        pygame.draw.rect(self.screen,self.color,(self.x,self.y,self.width,self.height))
        text = self.font.render(self.text,True,(0,0,0))
        text_rect = text.get_rect(center=(self.x+self.width/2,self.y+self.height/2))
        self.screen.blit(text,text_rect)

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if not click[0]:
            if self.is_clicked:
                Manager.change_level(Level1(self.screen))
                return
        self.is_clicked = False
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            self.color = self.hover_color
            if click[0]:
                self.color = self.clicked_color
                self.is_clicked = True
        else:
            self.color = (255,255,255)