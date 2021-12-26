import pygame
from src.window.Window import Window


class RestartWindow(MainWindow):
    def __init__(self, *args):
        super(RestartWindow, self).__init__(*args)

        self.parent = parent

    def render(self, screen: pygame.Surface):
        pass

    def update(self, *args):
        pass

    def get_parent(self):
        return self.parent
