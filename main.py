import pygame
from game import Game
from utils import Manager
import asyncio

pygame.init()
game = Game()

Manager.set_game(game)

asyncio.run(game.run())