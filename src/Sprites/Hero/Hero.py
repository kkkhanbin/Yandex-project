import pygame

from constants.sprites.hero.hero_settings import IMAGE_PATH, STEP

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

        self.image = pygame.transform.scale(
            ImageHandler.load_image(IMAGE_PATH, -1), self.get_rect().size)

        self.setup_step()
        self.vector = 0, 0
        self.inertia = 0, 0

    def setup_step(self):
        self.step = \
            STEP / self.get_parent().get_parent().get_parent().get_fps()

    def update(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()

    def tick(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_a]:
            self.set_rect(self.get_rect().move(-1 * self.get_step(), 0))
        elif pressed_keys[pygame.K_d]:
            self.set_rect(self.get_rect().move(1 * self.get_step(), 0))

        self.set_rect(self.get_rect().move(*self.get_vector()))

        self.normalize_pos()
        self.set_vector((
            self.get_vector()[0], self.get_vector()[1] + self.get_g()))

    def jump(self):
        pass

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

    def set_rect(self, rect: pygame.Rect):
        self.rect = rect

    def get_rect(self) -> pygame.Rect:
        return self.rect

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

        # TODO Столкновение с непроходимыми объектами
