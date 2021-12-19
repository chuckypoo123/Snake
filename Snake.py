from Snake import Game
from Frames import Game_Window

class Program():

    def __init__(self):
        self.window = Game_Window(self)

    def new_game(self):
        self.game = Game(self)
        

if __name__ == "__main__":
    program = Program()