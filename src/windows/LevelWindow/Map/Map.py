import os

import pygame

from constants.level.level_settings import PAR_SEPARATOR, TUPLE_SEPARATOR
from constants.paths import LEVELS_PATH, PARAMETERS_PATH, MAP_PATH
from constants.sprites.sprites import SPRITES
from constants.sprites.sprites_settings import HERO_SPRITE_NAME
from constants.windows.level_window.map.map_settings import BORDERS_COLOR, \
    BORDERS_WIDTH, G
from constants.gui.colors import BLACK

from handlers.ExceptionHandler.ExceptionHandler import ExceptionHandler


class Map:
    def __init__(self, parent, level_path: str, size: tuple, pos: tuple):
        self.parent = parent
        self.map_path = os.path.join(level_path, MAP_PATH)

        self.rect = pygame.Rect(*pos, *size)
        self.screen = pygame.Surface(self.get_rect().size)

        self.hero = None
        self.map = self.load_map()

        # Значения по умолчанию
        self.borders_color = BORDERS_COLOR
        self.borders_width = BORDERS_WIDTH
        self.background_color = BLACK

    def load_map(self):
        """Загрузка карты - распределение спрайтов по группам"""
        self.setup_sprite_groups()

        with open(self.get_map_path(), encoding='utf-8') as map_file:
            rows = filter(bool, map_file.read().split('\n'))

        # Проход по спрайтам в файле
        for row in rows:
            try:
                row = row.split(PAR_SEPARATOR)
                sprite = SPRITES[row[0]](*row[1:], self)
                self.add_sprite_in_groups(sprite)
            except TypeError as exception:
                ExceptionHandler().log(exception)
            except KeyError as exception:
                ExceptionHandler().log(exception)

    def add_sprite_in_groups(self, sprite: pygame.sprite.Sprite):
        # Все спрайты добавляются в эту группу для удобного рендера и
        # обновления
        self.get_all_sprites_group().add(sprite)

        if isinstance(sprite, SPRITES[HERO_SPRITE_NAME]):
            # Группа только для игрока
            self.get_hero_group().add(sprite)
            self.set_hero(sprite)
        else:
            # Группа без игрока для возможного добавления камеры
            self.get_sprites_without_hero_group().add(sprite)

    def setup_sprite_groups(self):
        self.hero_group = pygame.sprite.Group()
        self.sprites_without_hero_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()

    def render(self, screen: pygame.Surface):
        self.get_screen().fill(self.get_background_color())

        # Рамка
        pygame.draw.rect(screen, self.get_borders_color(), self.get_rect(),
                         self.get_borders_width())

        # Спрайты
        self.get_all_sprites_group().draw(self.get_screen())

        screen.blit(self.get_screen(), self.get_rect())

    def update(self, event: pygame.event.Event):
        self.get_all_sprites_group().update(event)

    def tick(self, fps: int):
        """Вызывается при каждом тике игрового цикла"""
        for sprite in self.get_all_sprites_group().sprites():
            sprite.tick(fps)

    def get_map_path(self) -> str:
        return self.map_path

    def get_map(self) -> list:
        return self.map

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_hero(self):
        return self.hero

    def set_hero(self, hero: pygame.sprite.Sprite):
        self.hero = hero
        return self

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

    def get_parent(self):
        return self.parent

    def get_screen(self) -> pygame.Surface:
        return self.screen

    def get_background_color(self) -> pygame.Color:
        return self.background_color
