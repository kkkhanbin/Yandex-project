import pygame

from Sprites.Sprite import Sprite

from constants.sprites.wall.wall_settings import IMAGE_PATH

from handlers.ImageHandler.ImageHandler import ImageHandler


class Wall(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.transform.scale(
            ImageHandler.load_image(IMAGE_PATH), self.get_rect().size)

    def get_image(self) -> pygame.Surface:
        return self.image
