from Frames import *
from time import sleep
from random import *
from threading import Thread

class Game():

    def __init__(self, app):
        self.app = app
        self.game_board = self.app.window.game_frame.game_board 

        # Settings
        self.paused = True
        self.width = 50
        self.height = 30
        self.pixel_scale = 20
        self.taurus = True

        self.snake = self.Snake(self)
        self.edible = self.new_edible()

    def start(self):
        self.paused = False
        sleep(1)
        while not self.paused:
            self.snake.advance()
            sleep(0.2)

    def pause(self, event):
        print(event)
        self.paused = not self.paused
        if self.paused:
            self.game_board.master.pause_popup()
            self.app.thread.join()
            print("Game paused")
        else:
            self.game_board.master.remove_pause_popup()
            self.app.thread = Thread(target = self.start)
            self.app.thread.start()
            print("Game Unpaused")

    def game_over(self):
        self.edible = self.new_edible()

    def new_edible(self):
        edible_cell = randint(0, self.width*self.height - 1)

        node_coords = self.game_board.coords(self.snake.head)
        if edible_cell == int(node_coords[0] * self.width + node_coords[1]):
            return self.new_edible()
        for node in self.snake.nodes:
            node_coords = self.game_board.coords(node)
            if edible_cell == int(node_coords[0] * self.width + node_coords[1]):
                return self.new_edible()

        edible_x = (edible_cell % self.width) * self.pixel_scale
        edible_y = (edible_cell // self.width) * self.pixel_scale
        # print(f"Coords of edible: {edible_x}, {edible_y}")
        return self.game_board.create_oval(edible_x, edible_y, edible_x + self.pixel_scale - 1, edible_y + self.pixel_scale - 1, fill = "red", width = 0)
    
    '''
    FUNCTION TO TEST: This should ensure an edible spawn on the snake (this function is used to test the logic avoiding the snake in new_edible() above)
    def new_edible(self):
        edible_cell = randint(0, 50*30 - 1)

        if self.snake is not None:
            node_coords = self.game_board.coords(self.snake.head)
            if edible_cell == int(node_coords[0] * 50 + node_coords[1]):
                return self.new_edible()
            for node in self.snake.nodes:
                node_coords = self.game_board.coords(node)
                if edible_cell == int(node_coords[0] * 50 + node_coords[1]):
                    edible_x = (edible_cell % 50) * 20
                    edible_y = (edible_cell // 50) * 20
                    return self.game_board.create_oval(edible_x, edible_y, edible_x + self.pixel_scale - 1, edible_y + self.pixel_scale - 1, fill = "red", width = 0)
            return self.new_edible()
        else:
            edible_x = (edible_cell % 50) * 20
            edible_y = (edible_cell // 50) * 20
            # print(f"Coords of edible: {edible_x}, {edible_y}")
            return self.game_board.create_oval(edible_x, edible_y, edible_x + self.pixel_scale - 1, edible_y + self.pixel_scale - 1, fill = "red", width = 0)
    '''

    class Snake():

        def __init__(self, game):
            self.game = game
            self.game_board = self.game.game_board
            self.orientation = 0
            self.head = self.game_board.create_arc(0, 0, self.game.pixel_scale - 1, self.game.pixel_scale - 1, start = 30, extent = 300, fill = "blue", width = 0)
            self.nodes = [self.game_board.create_oval(-self.game.pixel_scale, 0, -1, self.game.pixel_scale - 1, fill = "blue", width = 0)] # Nodes are elements in the body of the Snake

        def orient(self, event, new_orientation):

            # Do nothing if new orientation is forward or back OR if new orientation is opposite to last move's orientation (which would mean moving backwards)
            if not (self.orientation - new_orientation)%2 or new_orientation == (self.last_move_orientation + 2)%4:
                return

            self.orientation = new_orientation
            self.game_board.itemconfig(tagOrId = self.head, start = -90*new_orientation + 30) # Rotation clockwise because +y is downward on computer screen
            self.game_board.update_idletasks()
        
        def advance(self):

            self.last_move_orientation = self.orientation
            
            # Getting coords of head
            coords_of_head = self.game_board.coords(self.head)
            # print(coords_of_head) # Debug

            # Adding new node in position of head
            self.nodes.append(self.game_board.create_oval(coords_of_head, fill = "blue"))
            
            # Moving head
            mod = self.orientation % 2
            
            coords_of_head[mod]     += (-1)**(self.orientation//2)*self.game.pixel_scale
            coords_of_head[mod + 2] += (-1)**(self.orientation//2)*self.game.pixel_scale

            # Wall hits
            if int(coords_of_head[0]) == self.game.pixel_scale*self.game.width:
                if self.game.taurus == True:
                    coords_of_head[0] = 0
                    coords_of_head[2] = self.game.pixel_scale - 1
                else:
                    self.game.game_over()
            elif int(coords_of_head[0]) == -self.game.pixel_scale:
                if self.game.taurus == True:
                    coords_of_head[0] = self.game.pixel_scale*(self.game.width - 1)
                    coords_of_head[2] = self.game.pixel_scale*self.game.width - 1
                else:
                    self.game.game_over()
            elif coords_of_head[1] == self.game.pixel_scale*self.game.height:
                if self.game.taurus == True:
                    coords_of_head[1] = 0
                    coords_of_head[3] = self.game.pixel_scale - 1
                else:
                    self.game.game_over()
            elif coords_of_head[1] == -self.game.pixel_scale:
                if self.game.taurus == True:
                    coords_of_head[1] = self.game.pixel_scale*(self.game.height - 1)
                    coords_of_head[3] = self.game.pixel_scale*self.game.height - 1
                else:
                    self.game.game_over()

            self.game_board.coords(self.head, coords_of_head)

            # Eating
            if self.game_board.coords(self.head) == self.game_board.coords(self.game.edible):
                self.game_board.delete(self.game.edible)
                self.game.edible = self.game.new_edible()
            else:
                self.game_board.delete(self.nodes.pop(0))

            # Update canvas
            self.game_board.tag_raise(self.head)
            self.game_board.update_idletasks()

            if self.hit_self():
                self.game.game_over()

            return

        def hit_self(self):
            for node in self.nodes:
                if self.game_board.coords(self.head) == self.game_board.coords(node):
                    return True
            return False