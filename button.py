"""Stores GameButton Class"""

from tkinter import DISABLED, ttk

from functools import partial

class GameButton(ttk.Button):
    """Stores game buttons for mines"""

    def __init__(self, master, row, column, function1, function2):
        super().__init__(master, command=partial(function1, self), width=3)
        self.row = row
        self.col = column
        self.grid(row = row, column = column, ipadx=5, ipady=5)

        self.mines = False
        self.flagged = False
        self.off = False

        self.func2 = function2
        self.bind('<Button-3>', partial(function2, btn_id=self)) #self.right_click)

    def get_index(self):
        return self.col, self.row

    def disable_but(self):
        self.off = True
        self.config(state=DISABLED)
    
    def get_state(self):
        return self.off