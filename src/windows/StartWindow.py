import pygame

from src.windows.Window import Window
from src.handlers.ImageHandler import ImageHandler

from src.constants import start_screen_settings


class StartWindow(Window):
    def __init__(self, parent, *args):
        super().__init__(*args)

        self.parent = parent

        self.image = pygame.transform.scale(ImageHandler().load_image(
            start_screen_settings.BACKGROUND_PATH),
            self.get_parent().get_screen_size())
        self.rect = self.image.get_rect()

    def render(self, screen: pygame.Surface):
        screen.blit(self.get_image(), start_screen_settings.SCREEN_POS)

    def update(self, *args):
        event = args[0]

        if event.type == pygame.QUIT:
            self.get_parent().set_running(False)
        elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
            self.get_parent().delete_current_window(self)

    def get_parent(self):
        return self.parent

    def get_image(self) -> pygame.Surface:
        return self.image
