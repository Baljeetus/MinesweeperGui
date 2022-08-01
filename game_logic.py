"""Stores functions for managaing inner game logic"""
from random import randint

from tkinter import DISABLED

def add_mines(buttons, btn_id, height, width, nmines):
    """Sets up game by randomly adding mines"""
    col, row = btn_id.get_index()
    mines_to_add = nmines

    #Loops until nmines have been randomly added
    while mines_to_add:
        i = randint(0, height-1)
        j = randint(0, width-1)

        if (col == j and row == j) or buttons[i][j].mines:
            continue 
        if col - 1 == j or col + 1 == j:
            continue 
        if row - 1 == i or row + 1 == i:
            continue

        buttons[i][j].mines = True
        #buttons[i][j].config(text = "MINE")
        mines_to_add -= 1

def check_mines(buttons, btn_id, height, width, safe_buttons):
    """Checks surroundings for mines"""
    col, row = btn_id.get_index()
    #Set top row and bottom row to check

    mine_count = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if row + i >= 0 and row + i < height and col + j >= 0 and col + j < width:
                if buttons[row + i][col + j].mines:
                    mine_count += 1

    #If button clicked has 0 mines, check buttons next to it too
    if mine_count == 0:
        if btn_id.get_state(): 
            return
        else:
            btn_id.disable_but()
            safe_buttons[0] -= 1
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if row + i >= 0 and row + i < height and col + j >= 0 and col + j < width:
                        check_mines(buttons, buttons[row + i][col + j], height, width, safe_buttons)

    #Otherwise just disable the button and show the number of mines around
    else:
        if btn_id.get_state():
            return
        btn_id.config(text = mine_count)
        btn_id.disable_but()
        safe_buttons[0] -= 1

    return safe_buttons