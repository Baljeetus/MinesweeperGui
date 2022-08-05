#from tkinter import ttk
from tkinter import *
import time

from game_logic import game_over
#Would consider creating parent class counter to inherit from but not enough use case to validate

class Timer:
    """Class for storing and managing the timer of the game"""
    def __init__(self, master, digits):
        """Initializes attributes for Flag_counter"""
        self.digits = digits
        self.game_over = False

        #Make digits for flag counter [tens, ones]
        self.time_counter = []
        hundreds_counter = Label(master, borderwidth=0)
        hundreds_counter.grid(column=4, row=0, sticky=E)
        self.time_counter.append(hundreds_counter)
        tens_counter = Label(master, borderwidth=0)
        tens_counter.grid(column=5, row=0, sticky=E)
        self.time_counter.append(tens_counter)
        ones_counter = Label(master, borderwidth=0)
        ones_counter.grid(column=6, row=0, sticky=E)
        self.time_counter.append(ones_counter)

        self.set_timer()

    def set_timer(self, seconds = 0):
        """Sets counter to match flags"""
        if seconds > 999:
            return

        hundreds = seconds // 10 // 10
        tens = seconds // 10 % 10
        ones = seconds % 10

        self.time_counter[1]['image'] = self.digits[tens]
        self.time_counter[2]['image'] = self.digits[ones]
        self.time_counter[0]['image'] = self.digits[hundreds]
            


class Flag_Counter:
    """Class for storing and managing the tiemr of the game"""
    def __init__(self, master, digits):
        """Initializes attributes for Flag_counter"""
        self.digits = digits

        #Make digits for flag counter [tens, ones]
        self.flag_counter = []
        hundreds_counter = Label(master, borderwidth=0)
        hundreds_counter.grid(column=0, row=0, sticky=W)
        self.flag_counter.append(hundreds_counter)
        tens_counter = Label(master, borderwidth=0)
        tens_counter.grid(column=1, row=0, sticky=W)
        self.flag_counter.append(tens_counter)
        ones_counter = Label(master, borderwidth=0)
        ones_counter.grid(column=2, row=0, sticky=W)
        self.flag_counter.append(ones_counter)

    def set_counter(self, flags = 0):
        """Sets counter to match flags"""
        hundreds = flags // 10 // 10
        tens = flags // 10 % 10
        ones = flags % 10

        self.flag_counter[0]['image'] = self.digits[hundreds]
        self.flag_counter[1]['image'] = self.digits[tens]
        self.flag_counter[2]['image'] = self.digits[ones]

