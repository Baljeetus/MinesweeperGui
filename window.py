"""Stores Menu and GameWindow Classes"""
from tkinter import messagebox
from tkinter import *

from PIL import Image

from functools import partial

from button import GameButton

from counters import Flag_Counter, Timer

import game_logic as gl

class Menu(Frame):
    """Stores the menu frame"""

    def __init__(self, master):
        """Initializes the menu frame"""
        super().__init__(master)
        self.master = master
        self.show_start_menu()

    def show_start_menu(self):
        """Show menu for difficulty options and quit"""
        #Show frame
        self.pack(ipadx=100, ipady= 10)
        #Restrict Window Size
        self.master.resizable(width=False, height=False)
        #Prompt Label
        Label(self, text="Choose Difficulty").pack()       
        #Easy
        Button(self, text="Easy", 
            command=partial(self.show_game_window, "Easy"), width=10).pack()
        #Medium
        Button(self, text="Medium", 
            command=partial(self.show_game_window, "Medium"), width=10).pack()
        #Hard
        Button(self, text="Hard", 
            command=partial(self.show_game_window,"Hard"), width=10).pack()
        #Exit
        Button(self, text="Exit", command=exit, width=10).pack()

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

class GameWindow(Frame):
    """Stores Game Window Frame"""

    def __init__(self, master, difficulty):
        """
        Initalize Game Window Frame and attributes. Then iniitialize the
        info frame and game grid frames.
        """
        super().__init__(master)
        self.master = master
        self.difficulty = difficulty
        self.time = 0

        self.pack(ipadx = 20, ipady = 10)

        #Load Images
        BUTTON_TILE_MAP = Image.open('assets/tiles.png')
        BUTTON_FACES_MAP = Image.open('assets/faces.png')
        LABEL_NUMBERS_MAP = Image.open('assets/scores.png')

        #For Buttons
        self.tiles = {
            'default_tile' : gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 0),
            'disabled_tile': gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 1),
            'flagged_tile' : gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 2),
            #Number Tiles from 1-8
            'numbers' : [
                gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 8),
                gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 9),
                gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 10),
                gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 11),
                gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 12),
                gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 13),
                gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 14),
                gl.select_sprite(BUTTON_TILE_MAP, 8, 2, 15)
             ]
        } 
        
        #For Reset Button
        self.faces = {
            'smile' : gl.select_sprite(BUTTON_FACES_MAP, 5, 1, 0, 40, 40),
            'tense' : gl.select_sprite(BUTTON_FACES_MAP, 5, 1, 2, 40, 40),
            'glasses' : gl.select_sprite(BUTTON_FACES_MAP, 5, 1, 3, 40, 40),
            'dead' : gl.select_sprite(BUTTON_FACES_MAP, 5, 1, 4, 40, 40)
        }

        #For Timer and Flags
        self.scores = [
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 0, 24, 46),
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 1, 24, 46),
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 2, 24, 46),
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 3, 24, 46),
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 4, 24, 46),
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 5, 24, 46),
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 6, 24, 46),
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 7, 24, 46),
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 8, 24, 46),
            gl.select_sprite(LABEL_NUMBERS_MAP, 10, 1, 9, 24, 46)
        ]
        
        #Load Frames
        self.show_info()
        self.make_grid(difficulty)

    def show_info(self):
        """Shows game info such as time and reset"""
        self.info = Frame(self)
        self.info.pack()

        self.flag_counter = Flag_Counter(self.info, self.scores)
        
        #Make Reset button
        self.reset_button = Button(self.info, image = self.faces['smile'], 
            command=partial(gl.reset, self, self.difficulty), borderwidth=0)
        self.reset_button.grid(column=3, row = 0, sticky =(W,E), padx=40)

        #Make Digits for timer [2, 1, 0]

        self.time_counter = Timer(self.info, self.scores)

    def make_grid(self, difficulty):
        """Sets up button grid frame, aka mine grid"""

        #Create new frame
        self.game_frm = Frame(self)
        self.game_frm.pack()

        self.buttons = []
        self.first_click = True

        #Configure game setting (grid size & mine count)
        if difficulty == "Easy":
            self.height, self.width, self.nmines = 9, 9, 10
        elif difficulty == "Medium":
            self.height, self.width, self.nmines = 16, 16, 40
        elif difficulty == "Hard":
            self.height, self.width, self.nmines = 16, 30, 99

        #Display button Grid
        for i in range(0, self.height):
            btn_row = []
            for j in range(0, self.width):
                btn = GameButton(self.game_frm, i, j, 
                    self.tiles['default_tile'], self.tiles['flagged_tile'],
                    self.check_button, self.flag_button)

                btn_row.append(btn)

            self.buttons.append(btn_row)

        #Make countdown to win game if all safe buttons are pressed/disabled
        #Created as array to pass by reference, easier than manually assigning to.
        self.safe_buttons = [self.width * self.height - self.nmines]
        self.game_frm.flags = self.nmines
        self.flag_counter.set_counter(self.game_frm.flags)

    def check_button(self, btn_id):
        """Checks button range"""
        
        if self.first_click:
            gl.add_mines(self.buttons, btn_id, self.height, 
                self.width, self.nmines)
            #self.time_counter.start_timer()
        if btn_id.flagged or btn_id.get_state():
            #Do nothing if player has flagged or already pressed button
            pass
        elif btn_id.mines:
            #Game over (Lose)
            self.reset_button['image'] = self.faces['dead']
            message = "You lose"
            messagebox.showinfo("Loser", message)
            gl.game_over(self.master, self)
        else:
            #Check around button to count mines
            gl.check_mines(self.buttons, btn_id, self.height, self.width, 
                self.safe_buttons, self.tiles['disabled_tile'], 
                self.tiles['numbers'])

            self.first_click = False

        if self.safe_buttons[0] == 0:
            #Game Over (Win)
            self.reset_button['image'] = self.faces['glasses']
            message = "You win"
            messagebox.showinfo("Congrats", message)
            gl.game_over(self.master, self)

    def flag_button(self, btn_id, event):
        """Flags and unflags buttons when right clicked"""
        if btn_id.get_state():
            return
        if not btn_id.flagged:
            btn_id.flagged = True
            btn_id['image'] = self.tiles['flagged_tile']
            self.game_frm.flags -= 1
            self.flag_counter.set_counter(self.game_frm.flags)
        elif btn_id.flagged:
            btn_id.flagged = False
            btn_id['image'] = self.tiles['default_tile']
            self.game_frm.flags += 1
            self.flag_counter.set_counter(self.game_frm.flags)