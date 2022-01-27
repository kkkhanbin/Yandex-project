import pygame

from constants.sprites.hero.hero_settings import IMAGE_PATH, STEP

from handlers.ConvertHandler.ConvertHandler import ConvertHandler
from handlers.ImageHandler.ImageHandler import ImageHandler

from Sprites.Sprite import Sprite
from Sprites.Wall.Wall import Wall


class Hero(Sprite):
    # Аргументы вводятся в виде строки потому что они берутся из файла и каждый
    # спрайт должен сам конвертировать их в нужный тип
    def __init__(self, hp_info: str, *args):
        super().__init__(*args)
        # Информация об очках здоровья в формате
        # "минимальное, текущее, максимальное кол-во ОЗ"
        self.hp_info = ConvertHandler.str_to_tuple(hp_info, float)

        self.image = pygame.transform.scale(
            ImageHandler.load_image(IMAGE_PATH, -1), self.get_rect().size)
        self.mask = pygame.mask.from_surface(self.get_image())

        self.setup_step()
        self.vector = 0, 0
        self.inertia = 0, 0

        self.hook = False

    def setup_step(self):
        self.step = \
            STEP / self.get_parent().get_parent().get_parent().get_fps()

    def update(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()

    def tick(self):
        """Вызывается при каждом тике игрового цикла"""
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_a]:
            self.move((-1 * self.get_step(), 0))
        elif pressed_keys[pygame.K_d]:
            self.move((1 * self.get_step(), 0))


        self.move(self.get_vector())

        self.normalize_pos()
        self.set_vector((
            self.get_vector()[0], self.get_vector()[1] + self.get_g()))

    def jump(self):
        if self.get_hook():
            self.get_rect().y = 0

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
            next_pos = \
                shift[0] + self.get_rect().x, shift[1] + self.get_rect().y

            if not self.check_collides(next_pos):
                break

    def check_collides(self, pos: tuple) -> bool:
        collided_sprite_by_mask = self.temp_move(
            pos, self.get_collided, pygame.sprite.collide_mask, self)
        collided_sprite_by_bottom = self.temp_move(
            pos, self.get_collided, pygame.sprite.collide_rect,
            self.get_bottom)

        # Если нижний хитбокс задел препятствие, это значит что спрайт
        # коснулся пола, в этом случае нужно обнулить вектор и остановить
        # движение
        if isinstance(collided_sprite_by_bottom, Wall):
            self.set_vector((0, 0))
            return False

        # Если маска задела препятствие, а нижний хитбокс нет, это значит
        # что спрайт находится параллельно от препятствия
        elif isinstance(collided_sprite_by_mask, Wall) \
                and not isinstance(collided_sprite_by_bottom, Wall):
            self.set_hook(True)
            return False

        # Иначе просто двигаемся дальше
        else:
            self.set_hook(False)
            self.get_rect().x = pos[0]
            self.get_rect().y = pos[1]
            return True

    def temp_move(self, pos: tuple, func, *args) -> move:
        """Временно перемещает себя на указанную позицию и выполняет заданную
         функцию в промежутке"""
        real_pos = self.get_rect().x, self.get_rect().y
        self.get_rect().x, self.get_rect().y = pos

        if args[1] == self.get_bottom:
            return_value = func(args[0], self.get_bottom())
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

    def get_bottom(self) -> pygame.sprite.Sprite:
        """Возвращает спрайт - "низ игрока", нужен для различия между
        скольжением около стены и падением на нее сверху. Возвращает именно
        спрайт, а не Rect потому что в pygame нет функции для коллайда
        Rect'ов"""

        x, y = self.get_rect().x, self.get_rect().y
        w, h = self.get_rect().size

        padding = 20
        bottom = pygame.sprite.Sprite()
        bottom.rect = pygame.Rect(
            x + padding, y + h, w - padding * 2, 1)

        return bottom

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

    def get_step(self) -> int:
        return self.step

    def get_g(self) -> float:
        return self.get_parent().get_g()

    def set_vector(self, vector: tuple):
        self.vector = vector

    def add_vector(self, vector: tuple):
        self.get_vector()[0] += vector[0]
        self.get_vector()[1] += vector[1]

    def get_vector(self) -> tuple:
        return self.vector

    def get_inertia(self) -> tuple:
        return self.inertia

    def get_image(self) -> pygame.Surface:
        return self.image

    def set_hook(self, hook: bool):
        self.hook = hook
        return self

    def get_hook(self) -> bool:
        return self.hook
