from game import Game
from utils import Manager
import asyncio

# /// script
# dependencies = [
# "pygame-ce",
# "cffi",
# "pymunk",
# "pytmx",
# ]
# ///

game = Game()
Manager.set_game(game)

asyncio.run(game.run())