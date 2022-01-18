import pygame

from widgets.Widget import Widget


class Button(Widget):
    def __init__(self, image: pygame.Surface, *args):
        super().__init__(*args)

        self.image = image

    def is_pos_inside(self, pos: tuple) -> bool:
        return self.get_rect().collidepoint(*pos)

    def get_image(self) -> pygame.Surface:
        return self.image
