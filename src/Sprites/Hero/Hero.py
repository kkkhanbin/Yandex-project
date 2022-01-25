import pygame

from constants.sprites.hero.hero_settings import IMAGE_PATH

from handlers.ImageHandler.ImageHandler import ImageHandler

from Sprites.Sprite import Sprite


class Hero(Sprite):
    def __init__(self, pos: tuple, size: tuple, step: int, hp_info: tuple,
                 *groups):
        super().__init__(*groups)
        # Информация об очках здоровья в виде
        # "минимальное, текущее, максимальное кол-во ОЗ"
        self.hp_info = hp_info

        self.rect = pygame.Rect(*pos, *size)
        self.image = ImageHandler.load_image(IMAGE_PATH)

        self.step = step

    def update(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.button == pygame.K_SPACE:
                self.jump()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_a]:
            self.move((-1, 0))
        elif pressed_keys[pygame.K_d]:
            self.move((1, 0))

        # TODO сделать падение вниз

    def jump(self):
        pass

    def move(self, vector: tuple):
        rect = self.get_rect()
        rect.move(rect.x + vector[0] * self.get_step(),
                  rect.y + vector[1] * self.get_step())

    def get_min_hp(self) -> int:
        return self.hp_info[0]

    def get_hp(self) -> int:
        return self.hp_info[1]

    def get_max_hp(self) -> int:
        return self.hp_info[2]

    def get_hp_info(self) -> tuple:
        return self.hp_info

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_step(self) -> int:
        return self.step
