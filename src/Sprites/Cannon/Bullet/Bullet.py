from constants.sprites.cannon.bullet.bullet_settings import IMAGE_PATH, \
    SPEED
from constants.sprites.sprites_settings import ANGLES, DIRECTIONS

from Sprites.Sprite import Sprite
from Sprites.MovableSprite import MovableSprite


class Bullet(Sprite, MovableSprite):
    def __init__(self, damage: int, cannon, *args):
        # Пришлось явно вызывать методы у родительских классов из-за странной
        # ошибки рекурсии, причем только у Sprite. Когда я писал
        # super().__init__() все выполнялось нормально, я переделал на
        # super(Sprite, self).__init__() и вылезла ошибка рекурсии,
        # причем такого не было у MovableSprite
        Sprite.__init__(self, *args)
        MovableSprite.__init__(self)

        self.damage = damage
        self.cannon = cannon

        # Изображение
        self.image = self.load_image(IMAGE_PATH, -1)

        # Движение
        self.speed = SPEED

        direction = ANGLES[self.get_direction()]
        self.set_direction((direction * 2) % 360)
        self.direction = DIRECTIONS[direction]

    def tick(self, fps: int):
        speed = self.get_speed() / fps

        self.move((self.get_direction()[0] * speed,
                   self.get_direction()[1] * speed))

        if self.out_of_map():
            self.kill()

    def out_of_map(self) -> bool:
        x1, y1 = self.get_rect().x, self.get_rect().y
        w2, h2 = self.get_parent().get_rect().size

        return any([x1 > w2, y1 > h2, y1 < 0, x1 < 0])

    def get_cannon(self):
        return self.cannon

    def get_speed(self) -> float:
        return self.speed
