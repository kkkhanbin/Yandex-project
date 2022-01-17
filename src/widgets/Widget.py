from abc import abstractmethod
import pygame


class Widget:
    def __init__(self, name: str, pos: tuple, image: pygame.Surface):
        self.name = name
        self.pos = pos
        self.image = image

        self.rect = self.get_image().get_rect()
        self.update_rect()

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass

    def update(self):
        pass

    def get_pos(self) -> tuple:
        return self.pos

    def get_x(self) -> float:
        return self.pos[0]

    def get_y(self) -> float:
        return self.pos[1]

    def get_image(self) -> pygame.Surface:
        return self.image

    def set_pos(self, pos: tuple):
        self.pos = pos
        self.update_rect()
        return self

    def update_rect(self):
        x, y = self.get_pos()
        self.get_rect().x = x
        self.get_rect().y = y

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_name(self) -> str:
        return self.name
