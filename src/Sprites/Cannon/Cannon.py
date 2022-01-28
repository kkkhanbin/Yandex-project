import pygame

from constants.sprites.cannon.cannon_settings import IMAGE_PATH, BULLET, \
    SHOT_INTERVAL, BULLET_SIZE, BULLET_DAMAGE
from constants.sprites.sprites_settings import ANGLES, DIRECTIONS

from handlers.ConvertHandler.ConvertHandler import ConvertHandler

from Sprites.Sprite import Sprite


class Cannon(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # Снаряд
        self.bullet = BULLET
        self.bullets = pygame.sprite.Group()
        self.bullet_size = ConvertHandler.convert_percent(
            self.get_parent().get_screen().get_size(), BULLET_SIZE)[0]
        self.bullet_damage = BULLET_DAMAGE

        # Изображение
        self.image = self.load_image(IMAGE_PATH, -1)

        # Время с последнего выстрела в секундах
        self.shot_timer = 0
        self.shot_interval = SHOT_INTERVAL

        direction = ANGLES[self.get_direction()]
        self.set_direction((direction * 2) % 360)
        self.direction = DIRECTIONS[direction]

    def tick(self, fps: int):
        self.add_shot_timer(1 / fps)

        if self.get_shot_timer() // self.get_shot_interval() > 0:
            self.reload_shot_timer()
            self.shoot()

        for bullet in self.get_bullets().sprites():
            bullet.tick(fps)

    def shoot(self):
        bullet = self.get_bullet()(
            self.get_bullet_damage(), self, self.get_pos(),
            self.get_bullet_size(), self.get_direction(), self.get_parent())
        self.get_parent().get_all_sprites_group().add(bullet)
        self.get_bullets().add(bullet)

    def get_bullet(self) -> BULLET:
        return self.bullet

    def get_shot_interval(self) -> float:
        return self.shot_interval

    def get_shot_timer(self) -> float:
        return self.shot_timer

    def reload_shot_timer(self):
        self.shot_timer %= self.get_shot_interval()
        return self

    def add_shot_timer(self, time: float):
        self.shot_timer += time
        return self

    def get_bullets(self) -> pygame.sprite.Group:
        return self.bullets

    def get_bullet_size(self) -> tuple:
        return self.bullet_size

    def get_bullet_damage(self) -> int:
        return self.bullet_damage
