from enum import Enum

class Manager():
    __game = None
    @staticmethod
    def set_game(game):
        Manager.__game = game

    @staticmethod
    def change_level(level):
        Manager.__game.actual_level = level


class LevelState(Enum):
    FIRST_PART = 1
    SECOND_PART = 2
    GAME_OVER = 3


    


    