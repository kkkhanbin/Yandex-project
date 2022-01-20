import pygame

from windows.Window import Window

from handlers.ImageHandler.ImageHandler import ImageHandler

from constants.windows.windows_names import MAIN_MENU_WINDOW_NAME
from constants.windows.start_window import start_window_settings


class StartWindow(Window):
    def __init__(self, *args):
        super().__init__(*args)

        self.add_background()

    def add_background(self):
        self.get_screen().blit(pygame.transform.scale(ImageHandler.load_image(
            start_window_settings.BACKGROUND_PATH),
            self.get_parent().get_screen_size()),
            start_window_settings.BACKGROUND_POS)
        self.rect = self.get_screen().get_rect()

    def update(self, *args):
        event = args[0]

        if event.type == pygame.QUIT:
            self.get_parent().set_running(False)
        elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
            self.flip_window(self.get_parent().get_windows()
                             [MAIN_MENU_WINDOW_NAME](self.get_parent()))

