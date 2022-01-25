import os

import pygame

from constants.level.level_settings import PAR_SEPARATOR, POS_SEPARATOR
from constants.paths import LEVELS_PATH, PARAMETERS_PATH, MAP_PATH
from constants.sprites.sprite_settings import SPRITES_NAMES
from constants.windows.level_window.map.map_settings import BORDERS_COLOR, \
    BORDERS_WIDTH

from Sprites.Hero.Hero import Hero
from Sprites.Cannon.Cannon import Cannon
from Sprites.Door.Door import Door
from Sprites.Ladder.Ladder import Ladder
from Sprites.Saws.Saws import Saws
from Sprites.Wall.Wall import Wall


class Map:
    def __init__(self, level_path: str, size: tuple, pos: tuple):
        print(level_path, MAP_PATH)
        self.map_path = os.path.join(level_path, MAP_PATH)
        self.rect = pygame.Rect(*pos, *size)

        self.map = self.load_map()

        self.borders_color = BORDERS_COLOR
        self.borders_width = BORDERS_WIDTH

    def load_map(self):
        """Загрузка карты - распределение спрайтов по группам"""
        self.setup_sprite_groups()

        with open(self.get_map_path(), encoding='utf-8') as map_file:
            rows = filter(bool, map_file.read().split('\n'))

        # Проход по спрайтам в файле
        for row in rows:
            row = row.split(PAR_SEPARATOR)
            sprite = SPRITES_NAMES[row[0]](*row[1:])
            self.add_sprite_in_groups(sprite)

    def add_sprite_in_groups(self, sprite: pygame.sprite.Sprite):
        # Все спрайты добавляются в эту группу для удобного рендера и
        # обновления
        self.get_all_sprites_group().add(sprite)

        if isinstance(sprite, Hero):
            # Группа только для игрока
            self.get_hero_group().add(sprite)
        else:
            # Группа без игрока для возможного добавления камеры
            self.get_sprites_without_hero_group().add(sprite)

    def setup_sprite_groups(self):
        self.hero_group = pygame.sprite.Group()
        self.sprites_without_hero_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.get_borders_color(), self.get_rect(),
                         self.get_borders_width())
        self.get_all_sprites_group().draw(screen)

    def update(self, event: pygame.event.Event):
        self.get_all_sprites_group().update(event)

    def get_map_path(self) -> str:
        return self.map_path

    def get_map(self) -> list:
        return self.map

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_hero(self):
        # TODO Заглушка
        return Hero((0, 0), (30, 30), (0, 1, 5))

    def get_borders_color(self) -> pygame.Color:
        return self.borders_color

    def get_borders_width(self) -> int:
        return self.borders_width

    def get_hero_group(self) -> pygame.sprite.Group:
        return self.hero_group

    def get_sprites_without_hero_group(self) -> pygame.sprite.Group:
        return self.sprites_without_hero_group

    def get_all_sprites_group(self) -> pygame.sprite.Group:
        return self.all_sprites_group
