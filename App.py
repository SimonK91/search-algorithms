import pygame
from typing import Optional


class App:
    def __init__(self, width, height):
        self.size = self.width, self.height = width, height
        self._running = False
        self.screen: Optional[pygame.Surface] = None

    @property
    def is_running(self):
        return self._running

    def init(self):
        if self._running:
            return False
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        if self.screen is not None:
            self._running = True
        return self._running

    def quit(self):
        self._running = False
