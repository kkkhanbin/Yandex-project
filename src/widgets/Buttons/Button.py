import pygame

from abc import abstractmethod

from widgets.Widget import Widget


class Button(Widget):
    def __init__(self, image: pygame.Surface, *args):
        super().__init__(*args)

        self.image = image

    def is_pos_inside(self, pos: tuple) -> bool:
        return self.get_rect().collidepoint(*pos)

    def get_image(self) -> pygame.Surface:
        return self.image

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if self.is_pos_inside(event.pos):
                    self.click()

    # Вызывается при нажатии на кнопку
    def click(self):
        pass