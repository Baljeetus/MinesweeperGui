"""Stores GameButton Class"""

from tkinter import DISABLED, ttk

from functools import partial

class GameButton(ttk.Button):
    """Stores game buttons for mines"""

    def __init__(self, master, row, column, function):
        super().__init__(master, command=partial(function, self), width=3)
        self.row = row
        self.col = column
        self.mines = False
        self.grid(row = row, column = column, ipadx=5, ipady=5)
        self.off = False

    def get_index(self):
        return self.col, self.row

    def disable_but(self):
        self.off = True
        self.config(state=DISABLED)
    
    def get_state(self):
        return self.off