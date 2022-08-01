"""Stores Menu and GameWindow Classes"""
from tkinter import ttk

from functools import partial

from button import GameButton

import game_logic as gl

class Menu(ttk.Frame):
    """Stores the menu frame"""

    def __init__(self, master):
        """Initializes the menu frame"""
        super().__init__(master, padding=10)
        self.master = master
        self.show_start_menu()

    def show_start_menu(self):
        """Show menu for difficulty options and quit"""
        #Show frame
        self.pack()
        #Prompt Label
        ttk.Label(self, text="Choose Difficulty").pack()       
        #Easy
        ttk.Button(self, text="Easy", 
            command=partial(self.show_game_window, "Easy")).pack()
        #Medium
        ttk.Button(self, text="Medium", 
            command=partial(self.show_game_window, "Medium")).pack()
        #Hard
        ttk.Button(self, text="Hard", 
            command=partial(self.show_game_window,"Hard")).pack()
        #Exit
        ttk.Button(self, text="Exit", command=exit).pack()

    def show_game_window(self, difficulty):
        """
        Delete current frame from use.\n
        Load game window and button grid based on diffculty.\n
        """
        self.pack_forget()
        GameWindow(self.master, difficulty)

    def exit(self):
        """Exits the program"""
        self.master.destroy()

class GameWindow(ttk.Frame):
    """Stores Game Window Frame"""

    def __init__(self, master, difficulty):
        """
        Initalize Game Window Frame and attributes. Then iniitialize the
        info frame and game grid frames.
        """
        super().__init__(master, padding=10)
        self.master = master
        self.first_click = True
        self.pack()
        self.show_info()
        self.make_grid(difficulty)

    def show_info(self):
        """Shows game info such as time and reset"""
        self.info = ttk.Frame(self)
        self.info.grid()

        title = ttk.Label(self.info, text="Hello")
        title.grid(column = 0, row = 0)

    def make_grid(self, difficulty):
        """Set up button grid"""

        self.game_frm = ttk.Frame(self)
        self.game_frm.grid()
        self.buttons = []
        
        #Configure game setting (grid size & mine count)
        if difficulty == "Easy":
            self.nheight, self.nwidth, self.nmines = 9, 9, 10
        elif difficulty == "Medium":
            self.nheight, self.nwidth, self.nmines = 16, 16, 40
        elif difficulty == "Hard":
            self.nheight, self.nwidth, self.nmines = 16, 30, 99

        #Display button Grid
        for i in range(0, self.nheight):
            btn_row = []
            for j in range(0, self.nwidth):
                btn = GameButton(self.game_frm, i, j, self.check_button)
                btn_row.append(btn)

            self.buttons.append(btn_row)

        #Make countdown to win game if all safe buttons are pressed/disabled
        #Created as array to pass by reference, easier than manually assigning to.
        self.safe_buttons = [self.nwidth * self.nheight - self.nmines]

    def check_button(self, btn_id):
        """Checks button range"""
        if self.first_click:
            gl.add_mines(self.buttons, btn_id, self.nheight, 
                self.nwidth, self.nmines)
        if btn_id.mines:
            #Game over
            self.master.destroy()

        gl.check_mines(self.buttons, btn_id, self.nheight, self.nwidth, self.safe_buttons)
        self.first_click = False

        if self.safe_buttons[0] == 0:
            self.master.destroy()


