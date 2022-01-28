import pygame

from handlers.ConvertHandler.ConvertHandler import ConvertHandler


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos: str, size: str, parent, *groups):
        super().__init__(*groups)

        self.parent = parent

        self.rect = pygame.Rect(*self.convert_str_percent(pos),
                                *self.convert_str_percent(size))

    def convert_str_percent(self, value) -> tuple:
        return ConvertHandler.convert_percent(
            self.get_parent().get_rect().size,
            ConvertHandler.str_to_tuple(value, float))

    def update(self, event: pygame.event.Event):
        pass

    def get_parent(self):
        return self.parent

    def tick(self, fps: int):
        pass

    def set_rect(self, rect: pygame.Rect):
        self.rect = rect

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def set_pos(self, pos: tuple):
        self.get_rect().x = pos[0]
        self.get_rect().y = pos[1]
