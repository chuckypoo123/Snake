from Game import Game
from Frames import Game_Window
from threading import Thread

class Application():

    def __init__(self):
        self.window = Game_Window(self)
        self.window.mainloop() # This makes program actually display GUI and respond to input

    def new_game(self):
        self.game = Game(self)
        thread = Thread(target = self.game.start)
        thread.start()


if __name__ == "__main__":
    application = Application()