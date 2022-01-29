from abc import ABCMeta

import pygame

from constants.sprites.movable_sprite_settings import HIT_BOX_PADDING, \
    MAX_JUMP_COUNT, JUMP_HEIGHT


class MovableSprite(metaclass=ABCMeta):
    def __init__(self):
        # Прыжок
        self.hook = False
        self.jump_count = 0
        self.max_jump_count = MAX_JUMP_COUNT
        self.jump_height = \
            self.get_parent().get_screen().get_height() * JUMP_HEIGHT

        # Движение
        self.hit_box_padding = min(self.get_rect().size) * HIT_BOX_PADDING
        self.obstacles = []
        self.vector = 0, 0

        # Урон
        self.enemies = []
        self.collided_enemies = pygame.sprite.Group()

    def move(self, vector: tuple):
        """Двигает на заданный вектор"""
        shift = 0, 0
        steps = max(map(lambda value: abs(round(value)), vector)) + 1
        shift = shift[0] + round(vector[0] / steps), \
                shift[1] + round(vector[1] / steps)

        # Разделяет большой шаг на меньшие, длиной максимум в 1 пиксель, нужен
        # для того, чтобы при большом значении вектора спрайт не
        # телепортировался на этот вектор и не пропускал все препятствия на
        # своем пути
        for i in range(steps, 0, -1 if steps > 0 else 1):
            next_pos = shift[0] + self.get_rect().x,\
                       shift[1] + self.get_rect().y

            # Стороны, столкнувшиеся с препятствием
            collided_sides = [self.temp_move(next_pos, self.get_collided,
                pygame.sprite.collide_rect, sprite)
                for sprite in [self, 0, 1, 2, 3]]
            can_move = self.collided_obstacle(*collided_sides)

            if not can_move:
                break

            self.set_pos(next_pos)

    def fall(self, g: float):
        self.set_vector((self.get_vector()[0], self.get_vector()[1] + g))

    def jump(self):
        # hook - определяет есть ли возможность прыгнуть, т.е. прикасаемся ли
        # мы к твердому объекту от которого можно прыгнуть.
        # Или есть вариант прыжка в воздухе, max_jump_count - максимальное
        # кол-во прыжков в воздухе
        if self.get_hook() or \
                self.get_jump_count() < self.get_max_jump_count():
            # Первым делом прибавляем кол-во прыжков
            self.add_jump_count()

            # Задаем начальную инерцию при прыжке
            self.set_vector((0, -self.get_jump_height()))

    def collided_obstacle(self, rect, t, r, b, l) -> bool:
        """Вызывается каждый раз при касании с препятствием или наоборот.
        Параметры  t, r, b, l - top, left, bottom, right - это списки,
        содержащие спрайты, столкнувшиеся с соответствующей стороной. rect это
        столкновение с rect'ом спрайта. Возвращает булево значение,
        говорящее о том, может ли спрайт двигаться дальше"""
        self.set_hook(bool(self.intersection([r, b, l])))
        self.set_jump_count(0 if self.intersection([r, b, l])
                            else self.get_jump_count())

        if self.intersection([b]):
            self.set_vector((0, 0))

        enemies = self.intersection([rect], self.get_enemies())
        if enemies:
            if not self.get_collided_enemies().has(enemies[0]):
                self.damage_received(enemies[0].get_damage())
                self.get_collided_enemies().add(enemies[0])
        else:
            self.get_collided_enemies().empty()

        return not self.intersection([rect])

    def intersection(self, list1, list2=None) -> list:
        list2 = self.get_obstacles() if not list2 else list2

        intersection = []
        for sprites in list1:
            for sprite in sprites:
                for sprite_type in list2:
                    if type(sprite) == sprite_type:
                        intersection.append(sprite)

        return intersection

    def temp_move(self, pos: tuple, func, *args):
        """Временно перемещает себя на указанную позицию и выполняет заданную
         функцию в промежутке"""
        real_pos = self.get_rect().x, self.get_rect().y
        self.get_rect().x, self.get_rect().y = pos

        if args[1] != self:
            return_value = func(args[0], self.get_hit_box(args[1]))
        else:
            return_value = func(*args)

        self.get_rect().x, self.get_rect().y = real_pos
        return return_value

    def get_collided(self, func, sprite1: pygame.sprite.Sprite) -> list:
        collided_sprites = []
        for sprite in self.get_all_sprites_group():
            if func(sprite1, sprite):
                collided_sprites.append(sprite)
        return collided_sprites

    def get_hit_box(self, side: int=0) -> pygame.sprite.Sprite:
        """Возвращает спрайт - хитбокс. Возвращает именно спрайт, а не Rect
        потому что в pygame нет функции для коллайда Rect'ов.
        Параметр side может быть в диапазоне
        от 0 до 3 включительно - верх, право, низ, лево соответственно"""

        padding = self.get_hit_box_padding()
        x, y = self.get_rect().x, self.get_rect().y
        w, h = self.get_rect().size

        hit_box = pygame.sprite.Sprite()
        if side in [0, 2]:
            coeff = 0 if side == 0 else 1
            hit_box.rect = pygame.Rect(
                x + padding, y + h * coeff, w - padding * 2, 1)
        else:
            coeff = 0 if side == 1 else 1
            hit_box.rect = pygame.Rect(
                x + w * coeff, y + padding, 1, h - padding * 2)

        return hit_box

    def get_obstacles(self) -> list:
        return self.obstacles

    def get_hit_box_padding(self) -> int:
        return self.hit_box_padding

    def set_vector(self, vector: tuple):
        self.vector = vector

    def add_vector(self, vector: tuple):
        self.get_vector()[0] += vector[0]
        self.get_vector()[1] += vector[1]

    def get_vector(self) -> tuple:
        return self.vector

    def set_hook(self, hook: bool):
        self.hook = hook
        return self

    def get_hook(self) -> bool:
        return self.hook

    def get_jump_count(self) -> int:
        return self.jump_count

    def set_jump_count(self, jump_count: int):
        self.jump_count = jump_count
        return self

    def add_jump_count(self, jump_count: int=1):
        self.jump_count += jump_count
        return self

    def get_max_jump_count(self) -> int:
        return self.max_jump_count

    def get_jump_height(self) -> float:
        return self.jump_height

    def get_enemies(self) -> list:
        return self.enemies

    def get_collided_enemies(self) -> pygame.sprite.Group:
        return self.collided_enemies
