from abc import abstractmethod
import pygame


class Widget:
    def __init__(self, name: str, pos: tuple, size: tuple):
        self.name = name

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
