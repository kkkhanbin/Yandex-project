import pygame


class Star:
    def __init__(self, image: pygame.Surface, pos: tuple, size: tuple):
        self.image = image
        self.rect = pygame.Rect(*pos, *size)

    def render(self, screen: pygame.Surface):
        screen.blit(pygame.transform.scale(
            self.get_image(), self.get_rect().size), self.get_pos())

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_pos(self) -> tuple:
        return self.get_rect().x, self.get_rect().y

    def get_image(self) -> pygame.Surface:
        return self.image
