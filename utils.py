from enum import Enum

class Manager():
    __game = None
    __language = "en"
    @staticmethod
    def set_game(game):
        Manager.__game = game

    @staticmethod
    def change_level(level):
        Manager.__game.actual_level = level

    @staticmethod
    def set_language(language):
        Manager.__language = language

    @staticmethod
    def get_language():
        return Manager.__language


class LevelState(Enum):
    TEXT = 0
    FIRST_PART = 1
    SECOND_PART = 2
    GAME_OVER = 3
    MENU = 4


    


    