import pygame
from game import Game
from utils import Manager

pygame.init()
game = Game()

Manager.set_game(game)

game.run()