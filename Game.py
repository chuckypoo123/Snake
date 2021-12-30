from Frames import *
from time import sleep

class Game():

    def __init__(self, app):
        self.app = app
        self.snake = self.Snake()
        self.started = False
        self.unpaused = False

    def start(self):
        self.started = True
        self.unpaused = True
        sleep(1)
        while self.unpaused:
            self.app.window.game_frame.advance_snake(self.snake.orientation, False)
            sleep(0.2)

    def pause(self, event):
        self.unpaused = False
        print("Game paused")

    def orient_snake(self, event, new_orientation):
        if not (self.snake.orientation - new_orientation)%2:
            return

        self.snake.orientation = new_orientation
        self.app.window.game_frame.change_snake_orientation(new_orientation*90)        
        
    class Snake():

        def __init__(self):
            self.orientation = 0
            self.nodes = [] # Nodes are elements in the body of the Snake