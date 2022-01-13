import pygame

from windows.Window import Window
from handlers.Button import Button

from handlers.TextHandler import TextHandler

from constants.windows.main_menu_window_settings.main_menu_window_settings \
    import BUTTON_SIZE


class MainMenuWindow(Window):
    def __init__(self, *args):
        super().__init__(*args)

        self.button_size = BUTTON_SIZE

        self.buttons = pygame.sprite.Group()
        self.add_buttons(self.get_buttons())

    # Добавляет кнопки в группу спрайтов
    def add_buttons(self, buttons: pygame.sprite.Group) -> None:
        Button((0, 0), (
            self.get_screen().get_width() * self.get_button_width(),
            self.get_screen().get_height() * self.get_button_height()),
               self.test_button_func, buttons)

    def test_button_func(self):
        print('Тест')

    def render(self, screen: pygame.Surface):
        super().render(screen)

        self.get_buttons().draw(screen)

    def update(self, *args):
        event = args[0]

        for button in self.get_buttons().sprites():
            button.update(event)

    def get_buttons(self) -> pygame.sprite.Group:
        return self.buttons

    def get_button_size(self) -> tuple:
        return self.button_size

    def get_button_width(self) -> float:
        return self.get_button_size()[0]

    def get_button_height(self) -> float:
        return self.get_button_size()[1]