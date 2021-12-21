from tkinter import *
import time

'''
The class is the window of the program. It contains all the different frames to display.
This class also holds all the game options (this may need to ba changed later)
'''
class Game_Window(Tk):

    def __init__(self, app):
        self.app = app

        super().__init__()
        self.title("Snake")
        self.configure(background = "blue")
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.menu_frame = Menu_Frame(self)
        self.game_frame = Game_Frame(self)
        self.options_frame = Options_Frame(self)

        self.show_menu()

        # self.mainloop()

    def show_menu(self):
        self.geometry("200x200")
        self.resizable(0, 0)
        self.menu_frame.grid(sticky = NSEW)

    def hide_menu(self):
        self.menu_frame.grid_forget()
        self.menu_frame.forget()

    def show_game(self):
        height = 600 + self.game_frame.top_bar.winfo_height() # TODO Hardcoded value to change
        width = 1000 # TODO Hardcoded value to change
        self.geometry(f"{width}x{height}+10+10")
        self.resizable(0, 0)
        print(self.game_frame.get_game_board_dimensions())
        print(self.game_frame.top_bar.winfo_height())
        self.game_frame.grid(sticky = NSEW)
        print(self.game_frame.get_game_board_dimensions())
        print(self.game_frame.top_bar.winfo_height())
        # time.sleep(1)
        # self.game_frame.advance_snake(0, False)
        # time.sleep(1)
        # self.game_frame.advance_snake(1, True)
        return

    def hide_game(self):
        self.game_frame.grid_forget()
        self.game_frame.forget()

    def show_options(self):
        pass

    def start_game(self):
        self.hide_menu()
        self.show_game()
        self.app.new_game()
        # print("show_game returned")
        return

    def stop_game(self):
        self.hide_game()
        self.show_menu()

class Menu_Frame(Frame):

    def __init__(self, container):
        super().__init__(container, bg = "green")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure((1, 2), weight=2)

        titleLabel = Label(self, text = "Welcome to Snake!", background = "green")
        titleLabel.grid(column = 1, row = 0)

        startButton = Button(self, text = "Start", command = self.start_game)
        startButton.grid(column = 1, row = 1, sticky = EW)

        optionsButton = Button(self, text = "Options", command = self.change_options)
        optionsButton.grid(column = 1, row = 2, sticky = EW)

    def start_game(self):
        # Button(self.master, text = "Added button").grid(column = 0, row = 1)
        self.master.start_game()
        # print("Start game returned")

    def change_options(self):
        # Button(self.master, text = "Added button").grid(column = 0, row = 1)
        pass

class Options_Frame(Frame):

    def __init__(self, container):
        super().__init__(container, bg = "green")
        # self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure((1, 2), weight = 2)

        titleLabel = Label(self, text = "Options", background = "green")
        titleLabel.grid(column = 0, row = 0)

        backButton = Button(self, text = "Start", command = self.back_to_menu)
        backButton.grid(column = 0, row = 1, sticky = EW)

    def back_to_menu(self):
        pass

class Game_Frame(Frame):

    def __init__(self, container):

        # Constants
        self.pixel_scale = 10

        super().__init__(container, bg = "red")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight = 1)

        self.top_bar = Frame(self, background = "#00B93E")
        self.top_bar.columnconfigure(10, weight = 1)
        back_button = Button(self.top_bar, text = "Return to Menu", command = self.back_to_menu)
        back_button.grid(column = 0, row = 0)
        points = Label(self.top_bar, text = "2")
        points.grid(column = 10, row = 0)
        self.top_bar.grid(sticky = EW)

        self.game_board = Canvas(self, background="green", highlightthickness = 0)
        self.game_board.grid(column = 0, row = 1, sticky = NSEW)

        self.snake_head = self.game_board.create_arc(20, 100, 40, 120, start = 30, extent = 300, fill = "blue", width = 0)
        self.snake_body = [self.game_board.create_oval(0, 100, 20, 120, fill = "blue")]

    def back_to_menu(self):
        self.master.stop_game()

    def get_game_board_dimensions(self) -> list:
        master = self.master
        while master.master is not None: # Loop to get the highest level master
            master = master.master
        master.update()
        return [self.game_board.winfo_width(), self.game_board.winfo_height()]

    def advance_snake(self, direction, eating):
        print("Request received")
        # Getting coords of head
        coords_of_head = self.game_board.coords(self.snake_head)

        # Adding new bulb in place of head
        self.snake_body.append(self.game_board.create_oval(coords_of_head, fill = "blue"))
        
        # Moving head
        print(coords_of_head)
        print(type(coords_of_head))
        coords_of_head[direction % 2] += (-1)**(direction//2)*20
        coords_of_head[(direction % 2) + 2] += (-1)**(direction//2)*20

        self.game_board.coords(self.snake_head, coords_of_head)

        # Removing the last bulb
        if not eating:
            self.game_board.delete(self.snake_body.pop(0))

        # This line updates the canvas
        self.game_board.update_idletasks()

    def change_snake_orientation(self, new_orientation):
        self.game_board.itemconfig(tagOrId = self.snake_head, start = new_orientation + 30)