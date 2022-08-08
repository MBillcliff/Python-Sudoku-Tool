from settings import *

from get_resize_params import get_resize_params

from game_state import GameState


if __name__ == "__main__":
    game = GameState(cell_size)
    running = True
    screen = screen
    while running:
        screen = get_resize_params(game, screen)
        game.game_state()
        pygame.display.update()
        clock.tick(60)
