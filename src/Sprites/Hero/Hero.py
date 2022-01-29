import pygame

from constants.sprites.hero.hero_settings import IMAGE_PATH, STEP, OBSTACLES, \
    ENEMIES, DESTINATIONS
from constants.sprites.sprites_settings import DOOR_SPRITE_NAME
from constants.windows.level_window.map.map_settings import G
from constants import events

from handlers.ConvertHandler.ConvertHandler import ConvertHandler

from Sprites.Sprite import Sprite
from Sprites.MovableSprite import MovableSprite


class Hero(Sprite, MovableSprite):
    # Аргументы вводятся в виде строки потому что они берутся из файла и каждый
    # спрайт должен сам конвертировать их в нужный тип
    def __init__(self, hp_info: str, *args):
        # Пришлось явно вызывать методы у родительских классов из-за странной
        # ошибки рекурсии, причем только у Sprite. Когда я писал
        # super().__init__() все выполнялось нормально, я переделал на
        # super(Sprite, self).__init__() и вылезла ошибка рекурсии,
        # причем такого не было у MovableSprite
        Sprite.__init__(self, *args)
        MovableSprite.__init__(self)

        # Информация об очках здоровья в формате
        # "минимальное, текущее, максимальное кол-во ОЗ"
        self.hp_info = ConvertHandler.str_to_tuple(hp_info, float)

        # Изображение (Rect задается в родительском классе)
        self.image = self.load_image(IMAGE_PATH, -1)

        # Движение (переопределяем)
        self.obstacles = OBSTACLES
        self.enemies = ENEMIES
        self.destinations = DESTINATIONS

        self.set_direction(self.get_direction())

    def update(self, event: pygame.event.Event):
        super().update(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()

    def tick(self, fps: int):
        """Вызывается при каждом тике игрового цикла"""
        pressed_keys = pygame.key.get_pressed()
        g, step = G / fps, STEP / fps

        self.move(self.get_vector())

        if pressed_keys[pygame.K_a]:
            self.move((-1 * step, 0))
            self.set_direction((-1, 0), (True, True, False))
        elif pressed_keys[pygame.K_d]:
            self.move((1 * step, 0))
            self.set_direction((1, 0), (True, True, False))

        self.fall(g)

    def reach_destination(self, sprite: pygame.sprite.Sprite):
        """Вызывается при столкновении с пунктом назначения, sprite - спрайт,
         с которым стокнулись"""
        if sprite.__class__.__name__ == DOOR_SPRITE_NAME:
            pygame.time.set_timer(events.GAME_COMPLETED_EVENT, 1, 1)
