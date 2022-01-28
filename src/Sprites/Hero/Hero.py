import pygame

from constants.sprites.hero.hero_settings import IMAGE_PATH, STEP, \
    MAX_JUMP_COUNT, JUMP_HEIGHT, OBSTACLES, HIT_BOX_PADDING
from constants.windows.level_window.map.map_settings import G

from handlers.ConvertHandler.ConvertHandler import ConvertHandler
from handlers.ImageHandler.ImageHandler import ImageHandler

from Sprites.Sprite import Sprite


class Hero(Sprite):
    # Аргументы вводятся в виде строки потому что они берутся из файла и каждый
    # спрайт должен сам конвертировать их в нужный тип
    def __init__(self, hp_info: str, *args):
        super().__init__(*args)
        # Информация об очках здоровья в формате
        # "минимальное, текущее, максимальное кол-во ОЗ"
        self.hp_info = ConvertHandler.str_to_tuple(hp_info, float)

        # Изображение (Rect задается в родительском классе)
        self.image = pygame.transform.scale(
            ImageHandler.load_image(IMAGE_PATH, -1), self.get_rect().size)

        # Падение
        self.vector = 0, 0

        # Прыжок
        self.hook = False
        self.jump_count = 0
        self.max_jump_count = MAX_JUMP_COUNT
        self.jump_height = \
            self.get_parent().get_screen().get_height() * JUMP_HEIGHT

        # Движение
        self.obstacles = OBSTACLES
        self.hit_box_padding = HIT_BOX_PADDING

    def update(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()

    def tick(self, fps: int):
        """Вызывается при каждом тике игрового цикла"""
        pressed_keys = pygame.key.get_pressed()
        g, step = G / fps, STEP / fps

        if pressed_keys[pygame.K_a]:
            self.move((-1 * step, 0))
        elif pressed_keys[pygame.K_d]:
            self.move((1 * step, 0))

        self.move(self.get_vector())

        self.normalize_pos()
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
            self.set_vector((self.get_vector()[0], -self.get_jump_height()))

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
            collided_sided = [self.temp_move(
                next_pos, self.get_collided, pygame.sprite.collide_rect, i)
                for i in range(4)]
            can_move = self.collided_obstacle(*collided_sided)

            if not can_move:
                break

            self.set_pos(next_pos)

    def collided_obstacle(self, t, r, b, l) -> bool:
        """Вызывается каждый раз при касании с препятствием или наоборот.
        Параметры  t, r, b, l - top, left, bottom, right - это булевы значения,
        отвечающие за стороны спрайта, True означает что соответствующей
        стороной спрайт коснулся препятствия. Возвращает булево значение,
        говорящее о том, может ли спрайт двигаться дальше"""

        self.set_hook(any([r, b, l]))
        self.set_jump_count(0 if any([r, b, l]) else self.get_jump_count())

        if b:
            self.set_vector((0, 0))

        return not any([t, r, b, l])

    def temp_move(self, pos: tuple, func, *args) -> move:
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

    def get_collided(self, func, sprite1: pygame.sprite.Sprite):
        collided_sprite = False
        for sprite in self.get_all_sprites_group():
            if func(sprite1, sprite):
                collided_sprite = sprite
        return collided_sprite

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

    def normalize_pos(self):
        rect_w, screen_w = \
            self.get_rect().width, self.get_parent().get_rect().width
        self.rect.x = \
            screen_w - rect_w if self.get_rect().x < 0 else self.get_rect().x
        self.rect.x = \
            0 if self.get_rect().x + rect_w > screen_w else self.get_rect().x

        rect_h, screen_h = \
            self.get_rect().height, self.get_parent().get_rect().height
        self.get_rect().y = \
            screen_h - rect_h if self.get_rect().y < 0 else self.get_rect().y
        self.get_rect().y = \
            0 if self.get_rect().y + rect_h > screen_h else self.get_rect().y

    def get_all_sprites_group(self) -> pygame.sprite.Group:
        return self.get_parent().get_sprites_without_hero_group()

    def get_min_hp(self) -> int:
        return self.hp_info[0]

    def get_hp(self) -> int:
        return self.hp_info[1]

    def get_max_hp(self) -> int:
        return self.hp_info[2]

    def get_hp_info(self) -> tuple:
        return self.hp_info

    def set_vector(self, vector: tuple):
        self.vector = vector

    def add_vector(self, vector: tuple):
        self.get_vector()[0] += vector[0]
        self.get_vector()[1] += vector[1]

    def get_vector(self) -> tuple:
        return self.vector

    def get_image(self) -> pygame.Surface:
        return self.image

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

    def get_obstacles(self) -> list:
        return self.obstacles

    def get_hit_box_padding(self) -> int:
        return self.hit_box_padding
