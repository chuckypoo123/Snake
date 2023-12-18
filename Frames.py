from tkinter import *
import tkinter.ttk as ttk
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
        self.protocol("WM_DELETE_WINDOW", self.kill_threads)

        self.menu_frame = Menu_Frame(self)
        self.game_frame = Game_Frame(self)
        self.options_frame = Options_Frame(self)

        self.show_menu()

    def kill_threads(self):

        if self.app.game is not None:
            self.app.game.paused = True
            self.app.thread.join()
        
        self.destroy()

    def bind_controls(self):
        self.bind("<space>", self.app.game.pause)
        # Arrow key binding
        self.bind("<Right>", lambda event, dir = 0: self.app.game.snake.orient(event, dir))
        self.bind("<Down>",  lambda event, dir = 1: self.app.game.snake.orient(event, dir))
        self.bind("<Left>",  lambda event, dir = 2: self.app.game.snake.orient(event, dir))
        self.bind("<Up>",    lambda event, dir = 3: self.app.game.snake.orient(event, dir))
        # WASD key bindings
        self.bind("d",       lambda event, dir = 0: self.app.game.snake.orient(event, dir))
        self.bind("s",       lambda event, dir = 1: self.app.game.snake.orient(event, dir))
        self.bind("a",       lambda event, dir = 2: self.app.game.snake.orient(event, dir))
        self.bind("w",       lambda event, dir = 3: self.app.game.snake.orient(event, dir))

    def unbind_controls(self):
        self.unbind("<space>")
        # Arrow key binding
        self.unbind("<Right>")
        self.unbind("<Down>")
        self.unbind("<Left>")
        self.unbind("<Up>")
        # WASD key bindings
        self.unbind("d")
        self.unbind("s")
        self.unbind("a")
        self.unbind("w")

    def show_menu(self):
        self.geometry("200x200")
        self.resizable(0, 0)
        self.menu_frame.grid(sticky = NSEW)

    def hide_menu(self):
        self.menu_frame.grid_forget()

    def show_options(self):
        self.geometry("300x300")
        self.resizable(True, True)
        self.menu_frame.grid_forget()
        self.options_frame.grid(sticky = NSEW)

    def hide_options(self):
        self.options_frame.grid_forget()

    def show_game(self):
        height = 600 + self.game_frame.toolbar.winfo_height() + 6 # TODO Hardcoded value to change
        width = 1000 + 6 # TODO Hardcoded value to change
        self.geometry(f"{width}x{height}+10+10")
        self.resizable(0, 0)
        self.game_frame.grid(sticky = NSEW)
        # self.app.new_game()
        self.bind_controls()

    def hide_game(self):
        self.game_frame.grid_forget()

class Menu_Frame(Frame):

    def __init__(self, container):
        super().__init__(container, background = "green")
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
        self.master.hide_menu()
        self.master.app.new_game()
        self.master.show_game()

    def change_options(self):
        # Button(self.master, text = "Added button").grid(column = 0, row = 1)
        self.master.hide_menu()
        self.master.show_options()

class Options_Frame(Frame):

    def __init__(self, container):
        super().__init__(container, bg = "green")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure((1, 2, 3), weight = 2)

        titleLabel = Label(self, text = "Options", background = "green")
        titleLabel.grid(column = 0, row = 0)

        difFrame = Frame(self)
        difFrame.grid(column = 0, row = 1)
        difLabel = Label(difFrame, text = "Choose a difficulty:", background = "green")
        difLabel.grid(column = 0, row = 0, sticky = EW, columnspan = 5)
        # difficulty = StringVar(difFrame, "Medium")
        difficulties = ["Easy", "Medium", "Hard", "Custom"]
        self.difficulty = StringVar(difFrame, "Easy")
        s = ttk.Style()
        s.configure(
            'green.TRadiobutton',
            background = "green",
            foreground = "white"
        )
        for i in range(len(difficulties)):
            ttk.Radiobutton(difFrame, text = difficulties[i], value = difficulties[i],\
                variable = self.difficulty, style = 'green.TRadiobutton', command = self.set_options)\
                .grid(column = i, row = 1)

        s = ttk.Style()
        s.configure(
            'green.Horizontal.TScale',
            background = "green",
            foreground = "white"
        )
        width_frame = Frame(self)
        width_frame.columnconfigure((0, 1), weight = 1)
        width_frame.rowconfigure((0, 1), weight = 1)
        width_frame.grid(column = 0, row = 2)
        width_label = Label(width_frame, text = "Width", background = "green")
        width_label.grid(column = 0, row = 0, sticky = EW)
        self.width_scale = ttk.Scale(width_frame, from_ = 10, to = 60, orient = HORIZONTAL, style = 'green.Horizontal.TScale')
        self.width_scale.set(50)
        self.width_scale.grid(column = 0, row = 1, sticky=EW)

        height_frame = Frame(self)
        height_frame.columnconfigure(0, weight = 1)
        height_frame.rowconfigure((0, 1), weight = 1)
        # height_frame.grid(column = 0, row = 3)
        height_label = Label(width_frame, text = "Height", background = "green")
        height_label.grid(column = 1, row = 1, sticky = EW)
        self.height_scale = ttk.Scale(width_frame, from_ = 10, to = 60, orient = HORIZONTAL, style = 'green.Horizontal.TScale')
        self.height_scale.set(30)
        self.height_scale.grid(column = 1, row = 1, sticky=EW)

        back_button = ttk.Button(self, text = "Back to Menu", command = self.back_to_menu)
        back_button.grid(column = 0, row = 4, sticky = EW)

    def set_options(self):
        difficulty = self.difficulty.get()
        if difficulty == "Easy":
            print("Hello")
        elif difficulty == "Medium":
            pass
        elif difficulty == "Hard":
            pass
        else:
            pass

    def back_to_menu(self):
        self.master.hide_options()
        self.master.show_menu()

class Game_Frame(Frame):

    def __init__(self, container):

        # Constants
        self.pixel_scale = 20 # TODO not used

        # self.bg_r = 
        super().__init__(container, bg = "#00B93E")
        # Grid configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight = 1)

        # Creating toolbar
        self.toolbar_colour = 0x00B93E
        self.toolbar = Frame(self, background = "#00B93E")
        self.toolbar.columnconfigure(10, weight = 1)
        back_button = Button(self.toolbar, text = "Return to Menu", command = self.stop_game)
        back_button.grid(column = 0, row = 0)
        points = Label(self.toolbar, text = "2")
        points.grid(column = 10, row = 0)
        self.toolbar.grid(sticky = EW)

        # Creating game canvas
        self.game_board = Canvas(self, background="green", highlightthickness = 0)
        self.game_board.grid(column = 0, row = 1, sticky = NSEW, padx = 3, pady = 3)

        self.pause_label = Label(self, background = "red", text = "Game Paused")

    def stop_game(self):
        self.master.app.game.paused = True
        self.master.app.game.remove_all()
        self.remove_pause_popup()
        self.master.hide_game()
        self.master.show_menu()

    # Useless method
    def get_game_board_dimensions(self) -> list:
        master = self.master
        while master.master is not None: # Loop to get the highest level master
            master = master.master
        master.update()
        return [self.game_board.winfo_width(), self.game_board.winfo_height()]

    def pause_popup(self):
        self.pause_label.place(x = 300, y = 100)
        self.update_idletasks()

    def remove_pause_popup(self):
        self.pause_label.place_forget()