import pygame


class Button:
    IDLE = 0
    HOVER = 1
    PRESSED = 2
    @staticmethod
    def _noop():
        print("button pressed")

    def __init__(self, text, x, y, padding=0, on_click=_noop):
        self._color = (200, 200, 200)
        self._color_hover = (220, 220, 220)
        self._color_pressed = (180, 180, 180)
        self.state = Button.IDLE
        self.padding = padding

        font = pygame.font.SysFont("comicsansms", 16)
        self.text = font.render(text, True, (255, 0, 0))
        rect = self.text.get_rect()
        self.rect = x, y, rect[2]+padding*2, rect[3]+padding*2
        self.on_click = on_click

    @property
    def color(self):
        return (self._color if self.state == Button.IDLE else
                self._color_hover if self.state == Button.HOVER else
                self._color_pressed)

    def mouse_over(self, pos):
        return (self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2] and
                self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3])

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, (self.rect[0]+self.padding, self.rect[1]+self.padding))


