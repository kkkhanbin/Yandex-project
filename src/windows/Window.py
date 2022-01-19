from abc import abstractmethod
import pygame


class Window:
    def __init__(self, parent):
        self.parent = parent

        self.screen = pygame.Surface(parent.get_screen_size())
        self.pos = 0, 0

    def render(self, screen: pygame.Surface):
        screen.blit(self.get_screen(), self.get_pos())

    @abstractmethod
    def update(self, *args):
        pass

    def flip_window(self, window):
        self.get_parent().delete_current_window(self)
        self.get_parent().add_current_window(window(self.get_parent()))

    def get_parent(self):
        return self.parent

    def get_screen(self) -> pygame.Surface:
        return self.screen

    def get_pos(self) -> tuple:
        return self.pos

    # Конвертирует процентное значение координат в обычное
    def convert_percent(self, value):
        screen_w, screen_h = self.get_screen().get_size()

        if type(value) == float or type(value) == int:
            return max(screen_w, screen_h) * value
        elif type(value) == tuple:
            return (value[0] * screen_w, value[1] * screen_h)
        elif type(value) == list:
            return [value[0] * screen_w, value[1] * screen_h]
