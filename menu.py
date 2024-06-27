import pygame
from asset_loader import AssetLoader
from level1 import Level1
from utils import Manager

class Menu:
    def __init__(self,screen):
        self.screen = screen
        pygame.display.set_caption("Menu")
        self.button = Button(self.screen,250,229,300,150)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def draw(self):
        self.screen.fill((153, 204, 255))
        self.button.draw()

    def update(self,dt):
        self.handle_events()
        self.button.update()
        pass

class Button:
    def __init__(self,screen,x,y,width,height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_clicked = False
        self.image = AssetLoader.load_image("PlayButton.png")
        self.image_hover = AssetLoader.load_image("PlayButtonHover.png")
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.image_hover = pygame.transform.scale(self.image_hover,(self.width,self.height))

    def draw(self):
        mouse = pygame.mouse.get_pos()
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            self.screen.blit(self.image_hover,(self.x,self.y))
        else:
            self.screen.blit(self.image,(self.x,self.y))

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if not click[0]:
            if self.is_clicked:
                Manager.change_level(Level1(self.screen))
                return
        self.is_clicked = False
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            if click[0]:
                self.is_clicked = True