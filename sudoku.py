from settings import *

import numpy as np

from string_array import string_to_array

import time

from cell import Cell


class Sudoku:
    def __init__(self, grid_string, box_size, colour_scheme, game):
        self.game = game
        self.box_size = box_size
        self.colour_scheme = colour_scheme
        self.arr = np.array(string_to_array(grid_string))
        self.initial_arr = self.arr.copy()
        self.cells = self.make_cells()
        self.boxes = [[], [], [], [], [], [], [], [], []]
        for j in range(3):
            for i in range(9):
                self.boxes[i // 3 + j * 3].extend(self.arr[i][j * 3: (j + 1) * 3])
        self.boxes = np.array(self.boxes)
        self.start_time = time.time()
        self.elapsed = 0
        self.pause_time = 0

    def make_cells(self):
        cells = []
        for row, c in enumerate(self.arr):
            for col, val in enumerate(c):
                cells.append(Cell(row + 1, col + 1, val, self.box_size, self.colour_scheme, self.game))
        return cells

    def display(self, box_size, timer=False):
        self.box_size = box_size
        first_cell = self.cells[0]
        x, y = first_cell.x, first_cell.y
        big_box = pygame.Rect((x - 3, y - 3), (self.box_size * 9 + 6, self.box_size * 9 + 6))
        pygame.draw.rect(screen, self.game.colour_scheme['border'], big_box)
        for cell in self.cells:
            cell.box_size = self.box_size
            cell.show()
        for i in range(1, 3):
            pygame.draw.line(screen, self.game.colour_scheme['border'], (x + self.box_size * 3 * i, y),
                             (x + self.box_size * 3 * i, y + 9 * self.box_size), 2)
            pygame.draw.line(screen, self.game.colour_scheme['border'], (x, self.box_size * 3 * i + y),
                             (x + 9 * self.box_size, self.box_size * 3 * i + y), 2)
        if timer:
            self.show_timer(self.game.paused)

    def show_timer(self, is_paused):
        if is_paused:
            self.pause_time = time.time() - self.start_time - self.elapsed
            font = pygame.font.SysFont('tahoma', self.box_size * 2 // 3, True)
            paused_text = font.render("Paused", True, self.game.colour_scheme['button'][1])
            text_rect = paused_text.get_rect(center=(self.box_size * 5.5, self.box_size * 5.5))
            screen.blit(paused_text, text_rect)
        if not is_paused:
            self.elapsed = time.time() - self.start_time - self.pause_time
        font = pygame.font.SysFont("tahoma", self.box_size // 2, True)
        sec_zero = "0" if self.elapsed % 60 < 10 else ""
        timer = font.render(f'{int(self.elapsed) // 60}:{sec_zero}{int(self.elapsed % 60)}', True,
                            self.game.colour_scheme['timer'])
        text_surf = timer.get_rect(topleft=(self.box_size // 6, self.box_size // 6))
        screen.blit(timer, text_surf)

    def is_solved(self):
        for box, row, col in zip(self.boxes, self.arr, np.transpose(self.arr)):
            if '0' in box or len(box) != len(set(box)) or len(row) != len(set(row)) or len(col) != len(set(col)):
                return False
        return True
