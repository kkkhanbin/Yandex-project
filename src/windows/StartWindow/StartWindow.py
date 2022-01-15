import pygame

from windows.Window import Window

from handlers.ImageHandler import ImageHandler

from constants.windows.windows_names import MAIN_MENU_WINDOW_NAME
from constants.windows.start_window_settings import start_window_settings


class StartWindow(Window):
    def __init__(self, *args):
        super().__init__(*args)

        self.image = pygame.transform.scale(ImageHandler().load_image(
            start_window_settings.BACKGROUND_PATH),
            self.get_parent().get_screen_size())
        self.rect = self.image.get_rect()

    def render(self, screen: pygame.Surface):
        screen.blit(self.get_image(), start_window_settings.SCREEN_POS)

    def update(self, *args):
        event = args[0]

        if event.type == pygame.QUIT:
            self.get_parent().set_running(False)
        elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
            self.flip_window(self.get_parent().get_windows()
                             [MAIN_MENU_WINDOW_NAME])

    def get_image(self) -> pygame.Surface:
        return self.image
