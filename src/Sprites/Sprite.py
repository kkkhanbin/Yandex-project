from abc import abstractmethod

import pygame

from constants.sprites.sprites_settings import ANGLES, DIRECTIONS, \
    HERO_SPRITE_NAME
from constants import events

from handlers.ConvertHandler.ConvertHandler import ConvertHandler
from handlers.ImageHandler.ImageHandler import ImageHandler


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos: str, size: str, direction: str, parent, *groups):
        super().__init__(*groups)

        self.parent = parent

        if type(direction) != tuple:
            self.direction = ConvertHandler.str_to_tuple(direction, float)
        else:
            self.direction = direction

        if type(pos) != tuple or type(size) != tuple:
            self.rect = pygame.Rect(*self.convert_str_percent(pos),
                                    *self.convert_str_percent(size))
        else:
            self.rect = pygame.Rect(*pos, *size)

        self.hp_info = (0, 0, 0)
        self.damage = 0

    def convert_str_percent(self, value) -> tuple:
        return ConvertHandler.convert_percent(
            self.get_parent().get_rect().size,
            ConvertHandler.str_to_tuple(value, float))

    def update(self, event: pygame.event.Event):
        pass

    def update_hp(self):
        if self.get_hp() <= self.get_min_hp():
            if self.__class__.__name__ == HERO_SPRITE_NAME:
                pygame.time.set_timer(events.GAME_OVER_EVENT, 1, loops=1)

    def get_parent(self):
        return self.parent

    def tick(self, fps: int):
        pass

    def set_rect(self, rect: pygame.Rect):
        self.rect = rect

    def set_direction(self, direction, flip: tuple=(False, False, False)):
        """Аргумент flip нужен для выбора между rotate и flip, первое значение
        означает будет ли сделан flip, остальные два - flip_x и flip_y.
        В качестве direction можно написать кортеж-направление или угол"""

        # Если поворачиваем
        if not flip[0]:
            # Угол
            angle = ANGLES[self.get_direction()] - ANGLES[direction] \
                if direction not in ANGLES.values() \
                else direction - ANGLES[self.get_direction()]
            self.set_image(pygame.transform.rotate(
                self.get_image(), -angle))

        # Если флипаем
        elif self.get_direction() != direction:
            self.set_image(pygame.transform.flip(
                self.get_image(), *flip[1:]))

        self.direction = direction if direction not in ANGLES.values() \
            else DIRECTIONS[direction]

        return self

    def set_pos(self, pos: tuple):
        self.get_rect().x = pos[0]
        self.get_rect().y = pos[1]

    def load_image(self, path: str, color_key=None):
        return pygame.transform.scale(
            ImageHandler.load_image(path, color_key), self.get_rect().size)

    def get_image(self):
        return self.image

    @abstractmethod
    def set_image(self, image: pygame.Surface):
        self.image = image

    def get_all_sprites_group(self) -> pygame.sprite.Group:
        return self.get_parent().get_all_sprites_group()

    def get_all_sprites_without_hero_group(self) -> pygame.sprite.Group:
        return self.get_parent().get_all_sprites_without_hero_group()

    def get_damage(self) -> int:
        return self.damage

    def get_direction(self):
        return self.direction

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_pos(self) -> tuple:
        return self.get_rect().x, self.get_rect().y

    def get_min_hp(self) -> int:
        return self.hp_info[0]

    def get_hp(self) -> int:
        return self.hp_info[1]

    def get_max_hp(self) -> int:
        return self.hp_info[2]

    def add_hp(self, hp: int):
        new_hp = self.get_hp_info()[1] + hp
        self.set_hp_info(
            self.get_min_hp(), new_hp if new_hp <= self.get_max_hp() else
            self.get_max_hp(), self.get_max_hp())
        self.update_hp()

    def set_hp_info(self, min_hp: int, hp: int, max_hp: int):
        self.hp_info = min_hp, hp, max_hp

    def get_hp_info(self) -> tuple:
        return self.hp_info

    def damage_received(self, damage: int):
        """Вызывается при получении урона"""
        self.add_hp(-damage)
