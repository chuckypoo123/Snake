from Game import Game
from Frames import Game_Window

class Application():

    def __init__(self):
        self.window = Game_Window(self)
        self.window.mainloop()

    def new_game(self):
        print(self.window)
        self.game = Game(self)
        self.game.start()

if __name__ == "__main__":
    application = Application()