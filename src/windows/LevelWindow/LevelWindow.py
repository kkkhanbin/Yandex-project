import os

import pygame

from handlers.ConvertHandler.ConvertHandler import ConvertHandler

from constants.paths import LEVELS_PATH
from constants.windows.level_window.level_window_settings import MAP_POS, \
    MAP_SIZE, HP_BAR_POS, HP_BAR_SIZE

from windows.Window import Window
from windows.LevelWindow.Map.Map import Map
from windows.LevelWindow.HpBar.HpBar import HpBar


class LevelWindow(Window):
    def __init__(self, level_path: str, *args):
        print(level_path)
        super(LevelWindow, self).__init__(*args)

        self.level_path = level_path

        self.add_map()
        self.add_hp_bar()

    def add_map(self):
        self.map = Map(self.get_level_path(), *ConvertHandler.convert_percent(
            self.get_screen_size(), MAP_SIZE, MAP_POS))

    def add_hp_bar(self):
        self.hp_bar = HpBar(
            *ConvertHandler.convert_percent(
                self.get_screen_size(), HP_BAR_SIZE, HP_BAR_POS),
            self.get_map().get_hero())

    def render(self, screen: pygame.Surface):
        super().render(screen)

        self.get_map().render(screen)
        self.get_hp_bar().render(screen)

    def update(self, event: pygame.event.Event):
        self.get_map().update(event)

    def get_map(self) -> Map:
        return self.map

    def get_level_path(self) -> str:
        return self.level_path

    def get_hp_bar(self) -> HpBar:
        return self.hp_bar
