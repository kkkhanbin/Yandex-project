import os

import pygame

from handlers.ConvertHandler.ConvertHandler import ConvertHandler

from constants.paths import LEVELS_PATH
from constants.windows.level_window.level_window_settings import MAP_POS, \
    MAP_SIZE

from windows.Window import Window
from windows.LevelWindow.Map.Map import Map


class LevelWindow(Window):
    def __init__(self, level_name: str, *args):
        super(LevelWindow, self).__init__(*args)

        self.level_path = os.path.join(LEVELS_PATH, level_name)

        self.add_map()

    def add_map(self):
        self.map = Map(self.get_level_path(), *ConvertHandler.convert_percent(
            self.get_screen_size(), MAP_SIZE, MAP_POS))

    def get_level_path(self) -> str:
        return self.level_path

    def render(self, screen: pygame.Surface):
        super().render(screen)

        self.get_map().render(screen)

    def update(self, event: pygame):
        pass

    def get_map(self) -> Map:
        return self.map
