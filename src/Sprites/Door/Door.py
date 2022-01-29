from constants.sprites.door.door_settings import IMAGE_PATH
from constants.sprites.sprites_settings import ANGLES, DIRECTIONS

from Sprites.Sprite import Sprite


class Door(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = self.load_image(IMAGE_PATH, -1)

        direction = ANGLES[self.get_direction()]
        self.set_direction((direction * 2) % 360)
        self.direction = DIRECTIONS[direction]
