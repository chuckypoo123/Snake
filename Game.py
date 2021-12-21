from Frames import *
from time import sleep

class Game():

    def __init__(self, app):
        self.app = app
        self.snake = Snake()

    def start(self):
        sleep(3)
        while True:
            self.app.window.game_frame.advance_snake(0, False)
            sleep(0.5)

class Snake():

    def __init__(self):
        self.orientation = 0
        self.locations = []
