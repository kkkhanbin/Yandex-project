import pygame

from abc import abstractmethod

from widgets.Widget import Widget


class Button(Widget):
    def __init__(self, image: pygame.Surface, enabled: bool, *args):
        super().__init__(*args)

        self.image = image
        self.enabled = enabled

    def is_pos_inside(self, pos: tuple) -> bool:
        return self.get_rect().collidepoint(*pos)

    def get_image(self) -> pygame.Surface:
        return self.image

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if self.is_pos_inside(event.pos):
                    if self.get_enabled():
                        self.click()

    def get_enabled(self) -> bool:
        return self.enabled

    # Вызывается при нажатии на кнопку
    @abstractmethod
    def click(self):
        pass