from Frames import *
from time import sleep

class Game():

    def __init__(self, app):
        self.app = app
        self.snake = self.Snake(self)
        self.started = False
        self.unpaused = False

    def start(self):
        self.started = True
        self.unpaused = True
        sleep(1)
        while self.unpaused:
            # self.app.window.game_frame.advance(self.snake.orientation, False)
            self.snake.advance(False)
            sleep(0.2)

    def pause(self, event):
        self.unpaused = False
        print("Game paused")
        
    class Snake():

        def __init__(self, game):
            self.game = game
            self.game_board = self.game.app.window.game_frame.game_board
            self.orientation = 0 # Only useful for the head
            self.head = self.game_board.create_arc(0, 0, 19, 19, start = 30, extent = 300, fill = "blue", width = 0)
            self.nodes = [self.game_board.create_oval(-19, 0, -1, 19, fill = "blue", width = 0)] # Nodes are elements in the body of the Snake

        def change_orientation(self, event, new_orientation):

            if not (self.orientation - new_orientation)%2:
                return

            self.orientation = new_orientation
            self.game_board.itemconfig(tagOrId = self.head, start = -90*new_orientation + 30)
            self.game_board.update_idletasks()
        
        def advance(self, eating):
            # Getting coords of head
            coords_of_head = self.game_board.coords(self.head)

            # Adding new bulb in place of head
            self.nodes.append(self.game_board.create_oval(coords_of_head, fill = "blue"))
            
            # Moving head
            print(coords_of_head)
            mod = self.orientation % 2
            
            coords_of_head[mod]     += (-1)**(self.orientation//2)*20
            coords_of_head[mod + 2] += (-1)**(self.orientation//2)*20

            self.game_board.coords(self.head, coords_of_head)

            # Removing the last bulb
            if not eating:
                self.game_board.delete(self.nodes.pop(0))

            # This line updates the canvas
            self.game_board.update_idletasks()