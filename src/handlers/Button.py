import pygame

from handlers.ImageHandler import ImageHandler

from constants.paths import DEFAULT_BUTTON_PATH


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, size: tuple,
                 action, *groups, image_path: tuple = DEFAULT_BUTTON_PATH):
        super().__init__(*groups)

        self.pos = pos
        self.image = pygame.transform.scale(
            ImageHandler.load_image(image_path), size)
        self.action = action

        self.rect = self.get_image().get_rect()

    def is_pos_inside(self, pos: tuple) -> bool:
        return self.get_rect().collidepoint(*pos)

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if self.is_pos_inside(event.pos):
                    self.action()

    def get_image(self) -> pygame.Surface:
        return self.image

    def get_pos(self) -> tuple:
        return self.pos

    def get_x(self) -> float:
        return self.pos[0]

    def get_y(self) -> float:
        return self.pos[1]

    def set_pos(self, pos: tuple):
        self.pos = pos
        return self

    def get_rect(self) -> pygame.Rect:
        return self.rect
