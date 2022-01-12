import pygame


class Window:
    def __init__(self, parent):
        self.parent = parent

    def render(self, screen: pygame.Surface):
        pass

    def update(self, *args):
        pass

    def get_parent(self):
        return self.parent
