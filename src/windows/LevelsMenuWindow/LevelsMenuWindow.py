import pygame

from windows.Window import Window


class LevelsMenuWindow(Window):
    def __init__(self, user_name, *args):
        super(LevelsMenuWindow, self).__init__(*args)

        self.user_name = user_name

    def get_user_name(self) -> str:
        return self.user_name
