from abc import abstractmethod
import pygame


class Widget:
    def __init__(self, name: str, pos: tuple, size: tuple,
                 min_size: tuple=(0, 0)):
        self.name = name
        self.min_size = min_size

        self.rect = pygame.Rect(*pos, *size)

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass

    def update(self):
        pass

    def get_name(self) -> str:
        return self.name

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_min_size(self) -> tuple:
        return self.min_size

    def get_min_width(self) -> int:
        return self.get_min_size()[0]

    def get_min_height(self) -> int:
        return self.get_min_size()[1]
