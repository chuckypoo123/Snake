from tkinter import *
from typing import List

'''
The class is the window of the program. It contains all the different frames to display.
This class also holds all the game options (this may need to ba changed later)
'''
class Game_Window(Tk):

    def __init__(self):

        super().__init__()
        self.title("Snake")
        self.configure(background = "blue")
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.menu_frame = Menu_Frame(self)
        self.game_frame = Game_Frame(self)
        self.options_frame = Options_Frame(self)

        self.show_menu()

        self.mainloop()

    def show_menu(self):
        self.geometry("200x200")
        self.resizable(0, 0)
        self.menu_frame.grid(sticky = NSEW)

    def hide_menu(self):
        self.menu_frame.grid_forget()
        self.menu_frame.forget()

    def show_game(self):
        self.geometry("1000x600")
        self.resizable(0, 0)
        self.game_frame.grid(sticky = NSEW)
        print(self.game_frame.get_game_board_dimensions())


    def hide_game(self):
        self.game_frame.grid_forget()
        self.game_frame.forget()

    def show_options(self):
        pass

    def start_game(self):
        self.hide_menu()
        self.show_game()

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
        super().__init__(container, bg = "red")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight = 1)

        top_bar = Frame(self, background = "#00B93E")
        top_bar.columnconfigure(10, weight = 1)
        back_button = Button(top_bar, text = "Return to Menu", command = self.back_to_menu)
        back_button.grid(column = 0, row = 0)
        points = Label(top_bar, text = "1")
        points.grid(column = 10, row = 0)
        top_bar.grid(sticky = EW)

        self.game_board = Canvas(self, background="green")
        self.game_board.grid(column = 0, row = 1, sticky = NSEW)

    def back_to_menu(self):
        self.master.stop_game()

    def get_game_board_dimensions(self) -> List:
        master = self.master
        while master.master is not None: # Loop to get the highest level master
            master = master.master
        master.update()
        return [self.game_board.winfo_width(), self.game_board.winfo_height()]