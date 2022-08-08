import pygame

from colour_schemes import *

# load colour schemes
COLOUR_SCHEMES = (LIGHT_THEME, DARK_THEME, UGLY_THEME, BEIGE_THEME, EVANS_THEME)

# set start sizes
start_width, start_height = 960, 700
cell_size = start_height // 10

# initialise pygame and window
pygame.init()
screen = pygame.display.set_mode((start_width, start_height), pygame.RESIZABLE)
pygame.display.set_caption("Matthew's Sudoku Tool")
icon = pygame.image.load('images/matthews_sudoku_tool_icon.png')
pygame.display.set_icon(icon)

# create clock
clock = pygame.time.Clock()
