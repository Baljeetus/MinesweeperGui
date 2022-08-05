"""
Stores functions for managaing inner game logic\n
Functions Include:\n
add_mines(), check_mines(), game_over

"""
from random import randint

from tkinter import messagebox

from PIL import ImageTk

def add_mines(buttons, btn_id, height, width, nmines):
    """Sets up game by randomly adding mines"""
    col, row = btn_id.get_index()
    mines_to_add = nmines

    #Loops until nmines have been randomly added
    while mines_to_add:
        i = randint(0, height-1)
        j = randint(0, width-1)

        if col == j and row == i or buttons[i][j].mines:
            continue 
        if col - 1 == j or col + 1 == j:
            continue 
        if row - 1 == i or row + 1 == i:
            continue

        buttons[i][j].mines = True
        mines_to_add -= 1

def check_mines(buttons, btn_id, height, width, safe_buttons, disable_tile, numbers):
    """Checks surroundings for mines"""
    col, row = btn_id.get_index()
    mine_count = 0

    #Generate mines
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
            btn_id.disable_but(disable_tile)
            safe_buttons[0] -= 1
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if row + i >= 0 and row + i < height and col + j >= 0 and col + j < width:
                        check_mines(buttons, buttons[row + i][col + j], height, width, safe_buttons,
                            disable_tile, numbers)

    #Otherwise just disable the button and show the number of mines around
    else:
        if btn_id.get_state():
            return
        btn_id.disable_but(disable_tile)
        btn_id['image'] = numbers[mine_count - 1]
        safe_buttons[0] -= 1

def game_over(master, self):
    """Handles Game Over State"""
    self.time_counter.game_over = True
    message = "Try Again"
    retry = messagebox.askyesno("Retry", message)
    if retry:
        reset(self, self.difficulty)
    elif not retry:
        master.destroy()

def reset(self, difficulty):
    """Resets game"""
    self.reset_button['image'] = self.faces['smile']
    self.game_frm.destroy()
    self.make_grid(difficulty)

def select_sprite(image, col, rows, image_place, rwidth = 30, rheight = 30):
    """
    Loads sprite sheet and loads desired image from sprite sheet\n
    image_place: If first in grid put 0 etc
    """
    #Measures of entire image to get size of each grid
    width, height = image.size
    len_x = width / col
    len_y = height / rows

    #Handle multi row sprite sheets
    if image_place + 1 > col:
        row_ptn = image_place // col
        col_ptn = image_place % col
    else:
        row_ptn = 0
        col_ptn = image_place

    #Generate pixel positions of square grid to crop
    left = len_x * col_ptn
    upper = len_y * row_ptn
    right = len_x * (col_ptn + 1)
    lower = len_y * (row_ptn + 1)

    crop_box = (left, upper, right, lower)

    cropped_image = ImageTk.PhotoImage(image.crop(crop_box).resize((rwidth, rheight)))

    return cropped_image