class Manager():
    __game = None
    @staticmethod
    def set_game(game):
        Manager.__game = game

    @staticmethod
    def change_level(level):
        Manager.__game.actual_level = level


    


    