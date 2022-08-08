from pygame import display, RESIZABLE


def get_resize_params(game_object, window):
    w, h = window.get_width(), window.get_height()
    game_object.box_size = int(min(h, w * 3 // 4) // 11)
    game_object.width, game_object.height = w, h
    window = display.set_mode((w, h), RESIZABLE)
    return window
