from settings import *


class Cell:
    def __init__(self, row, col, val, box_size, colour_scheme, game):
        # initialise row, col & box number
        self.row = row
        self.col = col
        self.box = (self.row + 2) // 3 + 3 * ((self.col - 1) // 3) - 1

        self.box_size = box_size

        # make rect
        self.x, self.y = self.row * box_size, self.col * box_size
        self.border = pygame.Rect((self.x - 1, self.y - 1), (box_size + 2, box_size + 2))
        self.rect = pygame.Rect((self.x, self.y), (box_size, box_size))
        self.smaller_rect = pygame.Rect((self.x + self.box_size // 10, self.y + self.box_size / 10),
                                        (self.box_size * 0.8, self.box_size * 0.8))

        # initialise val
        self.val = val
        self.locked = (self.val != '0')

        # set font colour
        self.font_colour = colour_scheme['number'][0] if self.locked else colour_scheme['number'][1]

        # set rectangle colour
        self.rect_colour = colour_scheme['cell'][1] if self.locked else colour_scheme['cell'][0]

        # set initial pencil marks
        self.pencils = []
        self.manual_removed = []

        # Initially all of the below are false
        self.over = False
        self.selected = False
        self.highlight = False
        self.error = False

        self.game = game

    def show(self):
        # call this to draw the cell on the screen
        self.x, self.y = self.col * self.box_size, self.row * self.box_size
        self.border = pygame.Rect((self.x - 1, self.y - 1), (self.box_size + 2, self.box_size + 2))
        self.rect = pygame.Rect((self.x, self.y), (self.box_size, self.box_size))
        self.smaller_rect = pygame.Rect((self.x + self.box_size // 20, self.y + self.box_size // 20),
                                        (self.box_size * 0.9, self.box_size * 0.9))
        # check which colour the cell should be
        if self.highlight:
            self.rect_colour = self.game.colour_scheme['highlighted cell']
        elif self.error:
            if self.selected:
                self.rect_colour = DARK_RED if self.locked else LIGHT_RED
            else:
                self.rect_colour = DARKEST_RED if self.locked else RED
        elif not self.selected:
            self.rect_colour = self.game.colour_scheme['cell'][1] if self.locked else self.game.colour_scheme['cell'][0]
        else:
            self.rect_colour = self.game.colour_scheme['selected cell'][1] if self.locked else \
                self.game.colour_scheme['selected cell'][0]

        # choose font colour
        self.font_colour = self.game.colour_scheme['number'][0] if self.locked else self.game.colour_scheme['number'][1]

        # draw parts of cell based on some requirements
        pygame.draw.rect(screen, self.game.colour_scheme['border'], self.border)
        pygame.draw.rect(screen, self.rect_colour, self.rect)
        text_font = pygame.font.SysFont('tahoma', self.box_size // 2)
        if not self.game.paused or self.locked:
            val_text = text_font.render(str(self.val) if self.val != '0' else "", True, self.font_colour)
            screen.blit(val_text, (self.x + self.rect.width // 2 - val_text.get_width() // 2,
                                   self.y + self.rect.height // 2 - val_text.get_height() // 2))
        self.show_pencils()

    def is_over(self, mouse_pos):
        # call this to check if mouse is over cell
        if self.x < mouse_pos[0] < self.x + self.rect.width:
            if self.y < mouse_pos[1] < self.y + self.rect.height:
                self.over = True
                return True
        return False

    def update_grid(self):
        # call this to update the sudoku grid for this cell
        self.game.sudoku.arr[self.row - 1][self.col - 1] = str(self.val)
        self.game.sudoku.boxes[self.box][(self.col - 1) % 3 + (self.row - 1) % 3 * 3] = str(self.val)

    def auto_candidates(self):
        # call this to automatically update candidates for cells
        if not self.locked:
            for i in range(1, 10):
                i = str(i)
                if i in self.game.sudoku.boxes[self.box] or i in self.game.sudoku.arr[self.row - 1, :] or  \
                        i in self.game.sudoku.arr[:, self.col - 1]:
                    if i in self.pencils:
                        self.pencils.remove(i)
                elif i not in self.manual_removed and i not in self.pencils:
                    self.pencils.append(i)

    def is_error(self):
        # call this to check if the cell value collides with another cell
        if self.val == '0':
            return False
        # Your IDE may show these 3 lines as warnings but they are fine
        occurrences_box = sum(self.game.sudoku.boxes[self.box] == self.val)
        occurrences_row = sum(self.game.sudoku.arr[self.row - 1, :] == self.val)
        occurrences_col = sum(self.game.sudoku.arr[:, self.col - 1] == self.val)

        return sum((occurrences_box, occurrences_row, occurrences_col)) != 3

    def show_pencils(self):
        # call this to display pencil marks in the cell
        if self.val == '0' and not self.game.paused:
            text_font = pygame.font.SysFont('tahoma', self.box_size // 5)
            for pencil in self.pencils:
                pencil_val = int(pencil)
                pencil = text_font.render(pencil, True, self.game.colour_scheme['number'][1])
                screen.blit(pencil,
                            (self.x + (((pencil_val - 1) % 3 + 0.5) * self.rect.width) // 3 - pencil.get_width() // 2,
                             self.y + (((
                                                pencil_val - 1) // 3 + 0.5) * self.rect.height) // 3 - pencil.get_height() // 2))
