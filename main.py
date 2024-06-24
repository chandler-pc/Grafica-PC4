import pygame
from game import Game
from manager import Manager

pygame.init()
game = Game()

Manager.set_game(game)

game.run()