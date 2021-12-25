import pygame
from src.window.Window import Window


class LevelsWindow(MainWindow):
    def __init__(self, *args):
        super(LevelsWindow, self).__init__(*args)
        self.level_1 = level_1
        self.level_2 = level_2
        self.level_3 = level_3

        self.parent = parent

    def render(self, screen: pygame.Surface):
        pass

    def update(self, *args):
        pass

    def get_parent(self):
        return self.parent
