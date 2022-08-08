from settings import *


class Button:
    def __init__(self, x, y, width, height, colours, text='', is_active=False, game=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.colours = colours

        self.text = text
        self.text_size = (self.width * 0.5) // len(self.text)

        self.top_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.is_active = is_active
        self.hovering = False

        self.game = game

    def draw(self):
        # Call this method to draw the button on the screen
        scale = 1.05
        if self.hovering:
            top_rect = pygame.Rect(self.x - (scale - 1) * self.width // 2, self.y - (scale - 1) * self.height // 2,
                                   self.width * scale, self.height * scale)
            text_font = pygame.font.SysFont('tahoma', int(self.text_size * scale))
        else:
            top_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            text_font = pygame.font.SysFont('tahoma', int(self.text_size))
        text_surf = text_font.render(self.text, True, self.colours[not self.is_active])
        text_rect = text_surf.get_rect(center=top_rect.center)

        pygame.draw.rect(screen, self.colours[self.is_active], top_rect, border_radius=int(self.height // 10))
        screen.blit(text_surf, text_rect)

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.top_rect.height:
            if self.y < pos[1] < self.y + self.top_rect.height:
                return True
        return False

    def move_and_scale(self, pos=None, size=None, is_num_box=False, is_pencil=False):
        if pos is not None:
            self.x = pos[0]
            self.y = pos[1]
        if size is not None:
            self.width = size[0]
            self.height = size[1]
            self.text_size = self.height // 4
            if is_pencil:
                self.text_size = self.height // 4
            elif is_num_box:
                self.text_size = self.height // 2
        self.top_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.colours = self.game.colour_scheme['button']
