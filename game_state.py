import random

import pyperclip

from settings import *

from button import Button

from popup import Popup

from string_array import array_to_string

from sudoku import Sudoku

from keys import *

import time

import sys

from cell import Cell


class GameState:
    def __init__(self, box_size):
        self.colour_scheme = COLOUR_SCHEMES[0]
        self.moving_background_cells = []
        self.state = "start screen"
        self.selected_cell = None
        self.number_type = "Pen"
        self.show_timer = True
        self.viewing_solution = False
        self.changed_state = True
        self.resized = True
        self.paused = False

        self.box_size = box_size
        self.height = start_height
        self.width = start_width

        self.sudoku = None

        self.game = None

        self.make_floating_cells()

        # Define buttons
        button_colours = self.colour_scheme['button']
        self.pen_button = Button(11 * self.box_size, self.box_size, self.box_size, self.box_size,
                                 button_colours, "Pen", is_active=True, game=self)
        self.pencil_button = Button(12.1 * self.box_size, self.box_size, self.box_size, self.box_size,
                                    button_colours, "Pencil", game=self)
        self.auto_candidate_button = Button(11 * self.box_size, self.box_size * 6.5, self.box_size, self.box_size,
                                            button_colours, "Auto", game=self)
        self.new_sudoku_button = Button(13.2 * self.box_size, self.box_size * 6.5, self.box_size, self.box_size,
                                        button_colours, "Create", game=self)
        self.confirm_sudoku_button = Button(11 * self.box_size, self.box_size, self.box_size, self.box_size,
                                            button_colours, "Confirm", game=self)
        self.enter_string_button = Button(12.1 * self.box_size, self.box_size, self.box_size, self.box_size,
                                          button_colours, "Enter Str", game=self)
        self.view_solution_button = Button(self.width * 5 // 8 - self.width // 16, self.height // 2, self.box_size,
                                           self.box_size,
                                           button_colours, "View Solution", game=self)
        self.print_string_button = Button(11 * self.box_size, self.box_size * 7.6, self.box_size, self.box_size,
                                          button_colours, "String", game=self)
        self.clear_sudoku_button = Button(11 * self.box_size, self.box_size * 5.4, self.box_size, self.box_size,
                                          button_colours, "Clear", game=self)
        self.edit_sudoku_button = Button(11 * self.box_size, self.box_size * 7.6, self.box_size, self.box_size,
                                         button_colours, "Edit", game=self)
        self.pause_button = Button(2.3 * self.box_size, self.box_size // 8, self.box_size // 2, self.box_size // 2,
                                   button_colours, "||", game=self)
        self.initial_string_button = Button(11 * self.box_size, self.box_size * 8.7, self.box_size, self.box_size,
                                            button_colours, "Init Str", game=self)
        self.preloaded_sudoku_button = Button(self.width // 3 - self.box_size, self.height // 2 - self.box_size,
                                              self.box_size * 2, self.box_size * 2,
                                              button_colours, "Pre-made", game=self)
        self.home_button = Button(13.2 * self.box_size, self.box_size * 8.7, self.box_size, self.box_size,
                                  button_colours, "Home", game=self)
        self.clear_pencil_button = Button(12.1 * self.box_size, 7.6 * self.box_size, self.box_size, self.box_size,
                                          button_colours, "No Pencil", game=self)
        self.colour_scheme_button = Button(self.width - self.box_size * 1.6, self.height - self.box_size * 1.6,
                                           self.box_size * 1.5, self.box_size * 1.5,
                                           button_colours, "Colour", game=self)
        self.restart_button = Button(12.1 * self.box_size, 6.5 * self.box_size, self.box_size, self.box_size,
                                     button_colours, "Restart", game=self)
        self.num_buttons = []
        for i in range(9):
            self.num_buttons.append(
                Button((11 + 1.1 * (i % 3)) * self.box_size, self.box_size + i // 3 * self.box_size * 1.1,
                       self.box_size, self.box_size,
                       button_colours, str(i + 1), game=self))
        self.sudoku_strings = ("000943000060010050000000000800000003750060014100000009000000000020050080000374000",
                               "000123000040050060000000000700000003860040092900000001000000000050060080000392000",
                               "010020300002003040050000006004700050000100008070098000200004090000600704006000000")
        self.sudoku_buttons = []
        for i in range(1, len(self.sudoku_strings) + 1):
            self.sudoku_buttons.append(
                Button(self.width // 2 - self.box_size, self.height // i - self.box_size, self.box_size * 2,
                       self.box_size * 2,
                       button_colours, f'Sudoku {i}', game=self))
        self.popup = None

    def start_screen(self):
        def redraw_buttons():
            self.new_sudoku_button.move_and_scale(
                (self.width * 2 // 3 - self.box_size, self.height // 2 - self.box_size),
                (self.box_size * 2, self.box_size * 2))
            self.preloaded_sudoku_button.move_and_scale(
                (self.width // 3 - self.box_size, self.height // 2 - self.box_size),
                (self.box_size * 2, self.box_size * 2))
            self.colour_scheme_button.move_and_scale(
                (self.width - self.box_size * 1.6, self.height - self.box_size * 1.6),
                (self.box_size * 1.5, self.box_size * 1.5))

        screen.fill(self.colour_scheme['background'])
        self.moving_background()

        if self.changed_state:
            self.changed_state = False
            redraw_buttons()

        if self.resized:
            self.resized = False
            redraw_buttons()
            self.make_floating_cells()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                self.resized = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if self.new_sudoku_button.is_over(event.pos):
                    self.get_new_sudoku()
                elif self.preloaded_sudoku_button.is_over(event.pos):
                    self.state = "sudoku selection"
                    self.changed_state = True
                elif self.colour_scheme_button.is_over(event.pos):
                    self.toggle_colours()
                    redraw_buttons()

        buttons = (self.new_sudoku_button, self.preloaded_sudoku_button,
                   self.colour_scheme_button)
        self.button_hovers(buttons)
        for button in buttons:
            button.draw()

        self.draw_title()

    def sudoku_selection(self):
        def redraw_buttons():
            for j, sudoku_button in enumerate(self.sudoku_buttons):
                sudoku_button.move_and_scale((self.width // 2 - self.box_size,
                                              self.height * (j + 1) // (len(self.sudoku_buttons) + 1) - self.box_size),
                                             (self.box_size * 2, self.box_size * 2))

        if self.changed_state:
            self.changed_state = False
            redraw_buttons()

        if self.resized:
            self.resized = False
            redraw_buttons()
            self.make_floating_cells()

        screen.fill(self.colour_scheme['background'])
        self.moving_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                self.resized = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                for i, button in enumerate(self.sudoku_buttons):
                    if button.is_over(event.pos):
                        self.state = "playing"
                        self.changed_state = True
                        self.sudoku = Sudoku(self.sudoku_strings[i], self.box_size, self.colour_scheme, self)

        self.button_hovers(self.sudoku_buttons)
        for button in self.sudoku_buttons:
            button.draw()

    def playing(self):
        def redraw_buttons():
            self.pen_button.move_and_scale((11 * self.box_size, self.box_size), (self.box_size, self.box_size))
            self.pencil_button.move_and_scale((12.1 * self.box_size, self.box_size), (self.box_size, self.box_size))
            self.auto_candidate_button.move_and_scale((11 * self.box_size, self.box_size * 6.5),
                                                      (self.box_size, self.box_size))
            self.new_sudoku_button.move_and_scale((13.2 * self.box_size, self.box_size * 6.5),
                                                  (self.box_size, self.box_size))
            self.edit_sudoku_button.move_and_scale((13.2 * self.box_size, 7.6 * self.box_size),
                                                   (self.box_size, self.box_size))
            self.print_string_button.move_and_scale((11 * self.box_size, self.box_size * 7.6),
                                                    (self.box_size, self.box_size))
            self.pause_button.move_and_scale((13 / 6 * self.box_size, self.box_size // 6),
                                             (self.box_size * 2 // 3, self.box_size * 2 // 3))
            self.initial_string_button.move_and_scale((11 * self.box_size, 8.7 * self.box_size),
                                                      (self.box_size, self.box_size))
            self.home_button.move_and_scale((13.2 * self.box_size, 8.7 * self.box_size), (self.box_size, self.box_size))
            self.clear_pencil_button.move_and_scale((12.1 * self.box_size, 7.6 * self.box_size),
                                                    (self.box_size, self.box_size))
            self.colour_scheme_button.move_and_scale((12.1 * self.box_size, 8.7 * self.box_size),
                                                     (self.box_size, self.box_size))
            self.restart_button.move_and_scale((12.1 * self.box_size, 6.5 * self.box_size),
                                               (self.box_size, self.box_size))
            self.position_num_buttons()

        screen.fill(self.colour_scheme['background'])

        if self.changed_state:
            self.pen_button.is_active = True
            self.pencil_button.is_active = False
            self.auto_candidate_button.is_active = False

        if self.changed_state or self.resized:
            self.changed_state = False
            self.resized = False
            redraw_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                redraw_buttons()
                self.resized = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if self.pause_button.is_over(event.pos):
                    self.pause()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    self.pause_button.is_active = not self.pause_button.is_active
            if not self.paused:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    self.check_selected(event.pos)
                    # Check if buttons have been clicked
                    if self.pen_button.is_over(event.pos):
                        self.number_type = "Pen"
                        self.pen_button.is_active = True
                        self.pencil_button.is_active = False
                    elif self.pencil_button.is_over(event.pos):
                        self.number_type = "Pencil"
                        self.pencil_button.is_active = True
                        self.pen_button.is_active = False
                    elif self.auto_candidate_button.is_over(event.pos):
                        self.auto_candidate_button.is_active = not self.auto_candidate_button.is_active
                        if self.auto_candidate_button.is_active:
                            for cell in self.sudoku.cells:
                                cell.auto_candidates()
                    elif self.edit_sudoku_button.is_over(event.pos):
                        self.get_new_sudoku(edit=True)
                    elif self.new_sudoku_button.is_over(event.pos):
                        self.get_new_sudoku()
                    elif self.print_string_button.is_over(event.pos):
                        self.print_string_button.is_active = True
                        self.get_sudoku_string()
                    elif self.initial_string_button.is_over(event.pos):
                        self.initial_string_button.is_active = True
                        self.get_sudoku_string(initial=True)
                    elif self.home_button.is_over(event.pos):
                        self.state = "start screen"
                        self.changed_state = True
                    elif self.clear_pencil_button.is_over(event.pos):
                        self.remove_pencils()
                        self.clear_pencil_button.is_active = True
                        self.auto_candidate_button.is_active = False
                    elif self.colour_scheme_button.is_over(event.pos):
                        self.toggle_colours()
                        redraw_buttons()
                    elif self.restart_button.is_over(event.pos):
                        self.reset_cells()
                        self.restart_button.is_active = True
                        self.auto_candidate_button.is_active = False
                    # Check if a cell has been selected
                    self.num_cells_check(event.pos)

                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key in num_keys.keys():
                        self.remove_highlights()
                        if self.selected_cell is not None:
                            if not self.selected_cell.locked:
                                pressed = num_keys[key]
                                if self.number_type == "Pen":
                                    if self.selected_cell.val == pressed:
                                        self.selected_cell.val = '0'
                                    else:
                                        self.selected_cell.val = pressed
                                    self.selected_cell.update_grid()
                                    if self.auto_candidate_button.is_active:
                                        for cell in self.sudoku.cells:
                                            cell.auto_candidates()
                                elif self.number_type == "Pencil" and self.selected_cell.val == '0':
                                    if pressed in self.selected_cell.pencils:
                                        self.selected_cell.manual_removed.append(pressed)
                                        self.selected_cell.pencils.remove(pressed)
                                    elif int(pressed) > 0:
                                        self.selected_cell.pencils.append(pressed)
                                        if pressed in self.selected_cell.manual_removed:
                                            self.selected_cell.manual_removed.remove(pressed)
                                for cell in self.sudoku.cells:
                                    cell.error = cell.is_error()
                    elif key in arrow_keys:
                        self.key_check(key)

        if self.sudoku.is_solved() and not self.viewing_solution:
            elapsed = time.time() - self.sudoku.start_time
            sec_zero = "0" if int(elapsed % 60) < 10 else ""
            self.popup = Popup(screen.get_width() // 4, screen.get_height() // 4,
                               screen.get_width() // 2, screen.get_height() // 2,
                               (self.colour_scheme['background'], self.colour_scheme['button'][1]),
                               f"You finished the sudoku in {int(elapsed % 3600) // 60}:{sec_zero}{int(elapsed % 60)}!",
                               game=self)
            self.changed_state = True
            self.state = "solved"

        buttons = (self.pencil_button, self.pen_button, self.auto_candidate_button,
                   self.new_sudoku_button, self.edit_sudoku_button, self.print_string_button,
                   self.pause_button, self.initial_string_button, self.home_button,
                   self.clear_pencil_button, self.colour_scheme_button, self.restart_button)

        self.button_hovers(buttons)
        self.button_hovers(self.num_buttons)

        for button in buttons:
            if button == self.pause_button and self.viewing_solution:
                continue
            button.draw()
            if button not in (self.pen_button, self.pencil_button, self.auto_candidate_button, self.pause_button):
                button.is_active = False
        for button in self.num_buttons:
            button.draw()
            button.is_active = False

        self.sudoku.display(box_size=self.box_size, timer=self.show_timer)

    def new_sudoku(self):
        def redraw_buttons():
            self.confirm_sudoku_button.move_and_scale((11 * self.box_size, self.box_size),
                                                      (self.box_size, self.box_size))
            # self.enter_string_button.move_and_scale((12.1 * self.box_size, self.box_size),
            #                                         (self.box_size, self.box_size))
            self.print_string_button.move_and_scale((11 * self.box_size, self.box_size * 7.6),
                                                    (self.box_size, self.box_size))
            self.clear_sudoku_button.move_and_scale((11 * self.box_size, 5.4 * self.box_size),
                                                    (self.box_size, self.box_size))
            self.home_button.move_and_scale((13.2 * self.box_size, 8.7 * self.box_size), (self.box_size, self.box_size))
            self.position_num_buttons()

        def confirm_sudoku():
            self.sudoku = Sudoku(array_to_string(self.sudoku.arr),
                                 box_size=self.box_size,
                                 colour_scheme=self.colour_scheme,
                                 game=self)
            self.show_timer = True
            self.state = "playing"
            self.changed_state = True

        self.viewing_solution = False
        # Fix buttons based on screen size
        screen.fill(self.colour_scheme['background'])
        if self.changed_state or self.resized:
            self.changed_state = False
            self.resized = False
            redraw_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                self.resized = True
                redraw_buttons()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                # Check if a cell has been clicked
                self.check_selected(event.pos)
                # Check which buttons have been pressed
                if self.confirm_sudoku_button.is_over(event.pos):
                    confirm_sudoku()
                # elif self.enter_string_button.is_over(event.pos):
                #     self.enter_string_button.is_active = True
                #     self.popup = Popup(screen.get_width() // 4, screen.get_height() // 4,
                #                        screen.get_width() // 2, screen.get_height() // 2,
                #                        (self.colour_scheme['background'], self.colour_scheme['button'][1]),
                #                        "Enter the sudoku string below: ", text_box=True,
                #                        game=self)
                #     self.state = "enter string"
                #     self.changed_state = True
                elif self.print_string_button.is_over(event.pos):
                    self.print_string_button.is_active = True
                    self.get_sudoku_string()
                elif self.clear_sudoku_button.is_over(event.pos):
                    self.clear_sudoku_button.is_active = True
                    if self.selected_cell is not None:
                        self.selected_cell.selected = False
                        self.selected_cell = None
                    self.sudoku = Sudoku("0" * 81, box_size=self.box_size, colour_scheme=self.colour_scheme, game=self)
                elif self.home_button.is_over(event.pos):
                    self.state = "start screen"
                    self.changed_state = True
                else:
                    # Check the number buttons
                    self.num_cells_check(event.pos)
            if event.type == pygame.KEYDOWN:
                key = event.key
                # Confirm sudoku
                if key == pygame.K_RETURN:
                    confirm_sudoku()
                # Check if arrow keys have been used to move cells
                elif key in arrow_keys:
                    self.key_check(key)
                # Check if a numerical key has been pressed
                elif key in num_keys.keys():
                    if self.selected_cell is not None:
                        pressed = num_keys[key]
                        if self.selected_cell.val == pressed:
                            self.selected_cell.val = '0'
                        else:
                            self.selected_cell.val = pressed
                        self.selected_cell.update_grid()
                    for cell in self.sudoku.cells:
                        cell.error = cell.is_error()
        buttons = (self.confirm_sudoku_button,
                   self.print_string_button, self.clear_sudoku_button,
                   self.home_button)  # self.enter_string_button,

        self.button_hovers(buttons)
        self.button_hovers(self.num_buttons)

        for button in buttons:
            button.draw()
            button.is_active = False
        for button in self.num_buttons:
            button.draw()
            button.is_active = False
        self.sudoku.display(box_size=self.box_size)

    def sudoku_string_popup(self):
        screen.fill(self.colour_scheme['background'])
        self.popup.height = screen.get_height() // 2
        self.popup.width = screen.get_width() // 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if not self.popup.is_over(event.pos):
                    self.state = "new sudoku"
        self.popup.draw()

    def solved(self):
        def redraw_buttons():
            self.new_sudoku_button.move_and_scale((self.width * 3 // 8 - self.width // 16, self.height // 2),
                                                  (self.width // 8, self.height // 8))
            self.view_solution_button.move_and_scale((self.width * 5 // 8 - self.width // 16, self.height // 2),
                                                     (self.width // 8, self.height // 8))

        screen.fill(self.colour_scheme['background'])
        if self.changed_state or self.resized:
            self.changed_state = False
            self.resized = False
            redraw_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                self.resized = True
                redraw_buttons()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if self.new_sudoku_button.is_over(event.pos):
                    self.get_new_sudoku()
                elif not self.popup.is_over(event.pos) or self.view_solution_button.is_over(event.pos):
                    self.show_timer = False
                    self.viewing_solution = True
                    self.state = "playing"
                    self.changed_state = True

        self.popup.draw()
        self.new_sudoku_button.draw()
        self.view_solution_button.draw()

    def game_state(self):
        if self.state == "playing":
            self.playing()
        elif self.state == "new sudoku":
            self.new_sudoku()
        elif self.state == "enter string":
            self.sudoku_string_popup()
        elif self.state == "solved":
            self.solved()
        elif self.state == "start screen":
            self.start_screen()
        elif self.state == "sudoku selection":
            self.sudoku_selection()

    def check_selected(self, mouse_pos):
        if self.selected_cell is not None:
            if self.selected_cell.is_over(mouse_pos):
                self.highlight_cells(self.selected_cell.val)
            else:
                for cell in self.sudoku.cells:
                    cell.highlight = False

        for cell in self.sudoku.cells:
            if cell.is_over(mouse_pos):
                self.selected_cell = cell
                cell.selected = True
            else:
                cell.selected = False

        if self.selected_cell is not None:
            self.selected_cell.selected = True

    def highlight_cells(self, val):
        if val != '0':
            for cell in self.sudoku.cells:
                if cell.val == val:
                    cell.highlight = not cell.highlight
                elif val in cell.pencils and cell.val == '0':
                    cell.highlight = not cell.highlight
                else:
                    cell.highlight = False

    def remove_highlights(self):
        for cell in self.sudoku.cells:
            cell.highlight = False

    def get_new_sudoku(self, edit=False):
        self.state = "new sudoku"
        self.changed_state = True
        self.selected_cell = None
        if edit:
            self.sudoku = Sudoku(array_to_string(self.sudoku.arr), self.box_size, self.colour_scheme, self)
            for cell in self.sudoku.cells:
                cell.font_colour = self.colour_scheme['number'][0]
                cell.locked = False
        else:
            self.sudoku = Sudoku(
                "000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                self.box_size, self.colour_scheme, self)
        self.auto_candidate_button.is_active = False

    def num_cells_check(self, mouse_pos):
        for button in self.num_buttons:
            if button.is_over(mouse_pos):
                button.is_active = True
                if self.selected_cell is not None:
                    if not self.selected_cell.locked:
                        pressed = button.text
                        if self.number_type == "Pen":
                            if self.selected_cell.val == pressed:
                                self.selected_cell.val = '0'
                            else:
                                self.selected_cell.val = pressed
                            self.selected_cell.update_grid()
                            if self.auto_candidate_button.is_active:
                                for cell in self.sudoku.cells:
                                    cell.auto_candidates()
                        elif self.number_type == "Pencil" and self.selected_cell.val == '0':
                            if pressed in self.selected_cell.pencils:
                                self.selected_cell.manual_removed.append(pressed)
                                self.selected_cell.pencils.remove(pressed)
                            else:
                                self.selected_cell.pencils.append(pressed)
                                if pressed in self.selected_cell.manual_removed:
                                    self.selected_cell.manual_removed.remove(pressed)
                        for cell in self.sudoku.cells:
                            cell.error = cell.is_error()
                break

    def position_num_buttons(self):
        for i, button in enumerate(self.num_buttons):
            button.is_active = False
            j, k = i % 3, i // 3
            button.move_and_scale(
                (11 * self.box_size + j * 1.1 * self.box_size, self.box_size + (k + 1) * 1.1 * self.box_size),
                (self.box_size, self.box_size), is_num_box=True, is_pencil=self.pencil_button.is_active)

    def get_sudoku_string(self, initial=False):
        sudoku_string = array_to_string(self.sudoku.initial_arr) if initial else array_to_string(self.sudoku.arr)
        pyperclip.copy(sudoku_string)

    def key_check(self, key):
        if self.selected_cell is not None:
            row, col = self.selected_cell.row, self.selected_cell.col
            self.selected_cell.selected = False
            k = 9 * (row - 1) + col - 1
            if key == pygame.K_RIGHT or key == pygame.K_d:
                if col < 9:
                    self.selected_cell = self.sudoku.cells[k + 1]
                else:
                    self.selected_cell = self.sudoku.cells[k - 8]
            elif key == pygame.K_LEFT or key == pygame.K_a:
                if col > 1:
                    self.selected_cell = self.sudoku.cells[k - 1]
                else:
                    self.selected_cell = self.sudoku.cells[k + 8]
            elif key == pygame.K_UP or key == pygame.K_w:
                if row > 1:
                    self.selected_cell = self.sudoku.cells[k - 9]
                else:
                    self.selected_cell = self.sudoku.cells[k + 72]
            elif key == pygame.K_DOWN or key == pygame.K_s:
                if row < 9:
                    self.selected_cell = self.sudoku.cells[k + 9]
                else:
                    self.selected_cell = self.sudoku.cells[k - 72]
            self.selected_cell.selected = True

    def pause(self):
        self.paused = not self.paused
        self.pause_button.is_active = not self.pause_button.is_active

    def draw_title(self):
        font = pygame.font.SysFont('tahoma', self.box_size, True)
        title_text = font.render("Matthew's Sudoku Tool", True, self.colour_scheme['button'][1])
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 6))
        pygame.draw.rect(screen, self.colour_scheme['button'][0], title_rect, border_radius=title_rect.height // 8)
        screen.blit(title_text, title_rect)

    def moving_background(self):
        for cell in self.moving_background_cells:
            cell.col += cell.box_size / 200
            if cell.col * cell.box_size > self.width:
                cell.col = -1
                cell.val = random.randint(1, 9)
            cell.show()

    @staticmethod
    def button_hovers(buttons):
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.hovering = button.is_over(mouse_pos)

    def make_floating_cells(self):
        self.moving_background_cells.clear()
        k = 14
        n = 30
        for i in range(n):
            box = 3 * self.box_size // int(k)
            row = random.randint(1, 150 * self.height // box) / 100
            col = random.randint(1, 100 * self.width // box) / 100
            val = random.randint(1, 9)
            self.moving_background_cells.append(Cell(row, col, val, box, self.colour_scheme, self))
            k -= 10 / n

    def remove_pencils(self):
        for cell in self.sudoku.cells:
            cell.pencils.clear()
            cell.manual_removed.clear()
            cell.show()

    def reset_cells(self):
        for cell in self.sudoku.cells:
            if not cell.locked:
                cell.val = "0"
                cell.pencils.clear()
                cell.manual_removed.clear()
            cell.error = False
            cell.update_grid()

    def toggle_colours(self):
        index = COLOUR_SCHEMES.index(self.colour_scheme)
        index = (index + 1) % len(COLOUR_SCHEMES)
        self.colour_scheme = COLOUR_SCHEMES[index]
        if self.sudoku is not None:
            for cell in self.sudoku.cells:
                cell.font_colour = self.colour_scheme['number'][0]
        for cell in self.moving_background_cells:
            cell.font_colour = self.colour_scheme['number'][0]
