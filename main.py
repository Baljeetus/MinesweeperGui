from game import Game

#Hack that removes blurry window issue for high dpi
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

#Start our game
game = Game()
game.run()

