import pygame


class ImageHandler:
    @staticmethod
    def load_image(path: str, color_key=None) -> pygame.Surface:
        image = pygame.image.load(path)

        if color_key is not None:
            image = image.convert()
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()

        return image