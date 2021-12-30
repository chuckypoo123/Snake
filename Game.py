from Frames import *
from time import sleep
from random import *

class Game():

    def __init__(self, app):
        self.app = app
        self.game_board = self.app.window.game_frame.game_board 
        self.snake = self.Snake(self)
        self.unpaused = False
        self.edible = self.new_edible()

    def start(self):
        self.unpaused = True
        sleep(1)
        while self.unpaused:
            self.snake.advance()
            sleep(0.2)

    def pause(self, event):
        self.unpaused = False
        print("Game paused")

    def new_edible(self):
        edible_cell = randint(0, 50*30 - 1)
        edible_x = (edible_cell % 50) * 20
        edible_y = (edible_cell // 50) * 20
        print(f"Coords of edible: {edible_x}, {edible_y}")
        return self.game_board.create_oval(edible_x, edible_y, edible_x + 19, edible_y + 19, fill = "red", width = 0)
        # edible = self.game_board.create_oval(edible_x, edible_y, edible_x + 19, edible_y + 19, fill = "red", width = 0)
        # self.game_board.update_idletasks()
        # print(f"Edible created and printed")
        # return edible
        
    class Snake():

        def __init__(self, game):
            self.game = game
            self.game_board = self.game.game_board
            self.orientation = 0 # Only useful for the head
            self.head = self.game_board.create_arc(0, 0, 19, 19, start = 30, extent = 300, fill = "blue", width = 0)
            self.nodes = [self.game_board.create_oval(-19, 0, -1, 19, fill = "blue", width = 0)] # Nodes are elements in the body of the Snake

        def orient(self, event, new_orientation):

            if not (self.orientation - new_orientation)%2:
                return

            self.orientation = new_orientation
            self.game_board.itemconfig(tagOrId = self.head, start = -90*new_orientation + 30)
            self.game_board.update_idletasks()
        
        def advance(self):
            
            # Getting coords of head
            coords_of_head = self.game_board.coords(self.head)

            # Adding new bulb in place of head
            self.nodes.append(self.game_board.create_oval(coords_of_head, fill = "blue"))
            
            # Moving head
            # print(coords_of_head)
            mod = self.orientation % 2
            
            coords_of_head[mod]     += (-1)**(self.orientation//2)*20
            coords_of_head[mod + 2] += (-1)**(self.orientation//2)*20

            self.game_board.coords(self.head, coords_of_head)

            if self.game_board.coords(self.head) == self.game_board.coords(self.game.edible):
                self.game_board.delete(self.game.edible)
                self.game.edible = self.game.new_edible()
            else:
                self.game_board.delete(self.nodes.pop(0))

            # This line updates the canvas
            self.game_board.update_idletasks()