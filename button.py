"""Stores GameButton Class"""

from tkinter import *

from functools import partial

class GameButton(Button):
    """Stores game buttons for mines"""

    def __init__(self, master, row, column, default_sprite, flag, function1, function2):
        """
        Initializes Button attributes. Then initializes other 
        attributes for Game Button
        """
        super().__init__(master, command=partial(function1, self), height = 30, width = 30,
            borderwidth=0)
        self.row = row
        self.col = column
        self.grid(row = row, column = column, sticky="nsew")


        self.mines = False
        self.flagged = False
        self.off = False

        self.func2 = partial(function2, self)
        self.flag = flag
        self.default = default_sprite
        self.master = master
        self.bind('<Button-3>', self.func2)
        self['image'] = default_sprite

    def get_index(self):
        """Returns column and row placement of button AKA i and j of array"""
        return self.col, self.row

    def disable_but(self, disable_tile):
        """Sets state off and disables button"""
        self.off = True
        self['image'] = disable_tile
    
    def get_state(self):
        """Returns off if button has been disabled"""
        return self.off