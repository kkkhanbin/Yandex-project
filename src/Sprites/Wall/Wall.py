from Sprites.Sprite import Sprite

from constants.sprites.sprites_settings import ANGLES, DIRECTIONS
from constants.sprites.wall.wall_settings import IMAGE_PATH


class Wall(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = self.load_image(IMAGE_PATH)

        direction = ANGLES[self.get_direction()]
        self.set_direction((direction * 2) % 360)
        self.direction = DIRECTIONS[direction]
