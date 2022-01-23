import os

import pygame

from constants.paths import LEVELS_PATH

from windows.Window import Window


class LevelWindow(Window):
    def __init__(self, level_name: str, *args):
        super(LevelWindow, self).__init__(*args)

        self.level_path = os.path.join(LEVELS_PATH, level_name)

    def get_level_path(self) -> str:
        return self.level_path
