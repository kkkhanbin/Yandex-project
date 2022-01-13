import pygame
pygame.init()

from constants.main_settings import FPS, SIZE, BACKGROUND_COLOR, \
    START_WINDOWS, TITLE
from windows.Window import Window


class Game:
    def __init__(self):
        self.running = True

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.background_color = BACKGROUND_COLOR
        self.fps = FPS
        self.title = TITLE

        self.current_windows = self.load_current_windows()

        self.run()

    def run(self):
        while self.get_running():
            self.get_screen().fill(self.get_background_color())
            pygame.display.set_caption(self.get_title())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.set_running(False)

                self.update_current_windows(event)

            self.render_current_windows(self.get_screen())

            pygame.display.flip()
            self.get_clock().tick(round(self.get_fps()))

    def set_running(self, running: bool):
        self.running = running
        return self

    def get_running(self) -> bool:
        return self.running

    def get_clock(self) -> pygame.time.Clock:
        return self.clock

    def get_screen(self) -> pygame.Surface:
        return self.screen

    def get_background_color(self) -> pygame.Color:
        return self.background_color

    def get_fps(self) -> float:
        return self.fps

    def get_current_windows(self) -> list:
        return self.current_windows

    def get_screen_size(self) -> tuple:
        return self.get_screen().get_size()

    def get_title(self) -> str:
        return self.title

    def update_current_windows(self, *args):
        for current_window in self.get_current_windows():
            current_window.update(*args)

    def render_current_windows(self, screen: pygame.Surface):
        for current_window in self.get_current_windows():
            current_window.render(screen)

    def delete_current_window(self, window: Window):
        self.get_current_windows().remove(window)

    def add_current_window(self, window: Window):
        self.get_current_windows().append(window)

    def load_current_windows(self) -> list:
        return list(map(lambda window: window(self), START_WINDOWS))


Game()