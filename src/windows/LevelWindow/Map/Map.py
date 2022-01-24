import os

import pygame

from constants.paths import LEVELS_PATH, PARAMETERS_PATH, MAP_PATH
from constants.sprites.sprite_settings import SPRITES_NAMES
from constants.windows.level_window.map.map_settings import BORDERS_COLOR, \
    BORDERS_WIDTH


class Map:
    def __init__(self, level_path: str, size: tuple, pos: tuple):
        self.map_path = os.path.join(level_path, MAP_PATH)
        self.rect = pygame.Rect(*pos, *size)

        self.map = self.load_map()

    def load_map(self) -> list:
        """Загрузка карты"""
        pass

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, BORDERS_COLOR, self.get_rect(), BORDERS_WIDTH)

    def update(self, *args):
        pass

    def get_map_path(self) -> str:
        return self.map_path

    def get_map(self) -> list:
        return self.map

    def get_rect(self) -> pygame.Rect:
        return self.rect
