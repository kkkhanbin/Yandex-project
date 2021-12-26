import pygame

from windows.Window import Window


class ProfileActionsMenuWindow(Window):
    def __init__(self, parent, *args):
        super().__init__(*args)

        self.parent = parent

    def render(self, screen: pygame.Surface):
        pass

    def update(self, *args):
        pass

    def get_parent(self):
        return self.parent

