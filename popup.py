from settings import *


class Popup:
    def __init__(self, x, y, width, height, colours, text, text_box=False, text_box_text=None, game=None):
        self.game = game

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.colours = colours

        self.text = text
        self.text_size = 2 * self.width // len(self.text)

        self.text_box = text_box
        self.text_box_text = text_box_text
        self.top_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        text_font = pygame.font.SysFont('tahoma', int(self.text_size))
        text_surf = text_font.render(self.text, True, self.colours[1])
        text_rect = text_surf.get_rect(center=(self.top_rect.centerx, self.top_rect.centery - self.height // 4))
        border_rect = pygame.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4)

        pygame.draw.rect(screen, self.game.colour_scheme['border'], border_rect)
        pygame.draw.rect(screen, self.colours[0], self.top_rect, border_radius=self.width // 20)
        screen.blit(text_surf, text_rect)

        if self.text_box:
            text_box_border = pygame.Rect(self.x + self.width // 8 - 1, self.y + self.height // 2 - 1,
                                          self.width * 3 / 4 + 2, self.height // 8 + 2)
            text_box = pygame.Rect(self.x + self.width // 8, self.y + self.height // 2, self.width * 3 / 4,
                                   self.height // 8)
            pygame.draw.rect(screen, self.game.colour_scheme['border'], text_box_border)
            pygame.draw.rect(screen, self.game.colour_scheme['cell'][0], text_box)
            text = text_font.render(self.text_box_text, True, self.game.colour_scheme['border'])
            text_box_rect = text.get_rect(center=(self.top_rect.centerx, self.top_rect.centery + self.height // 6))
            screen.blit(text, text_box_rect)

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.top_rect.width:
            if self.y < pos[1] < self.y + self.top_rect.height:
                return True
        return False
