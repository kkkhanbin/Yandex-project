import pygame
pygame.init()

from constants.main_settings import FPS, SIZE, BACKGROUND_COLOR, \
    START_WINDOWS_NAMES, TITLE
from constants.windows.windows_names import *

from windows.Window import Window

from windows.MainMenuWindow.MainMenuWindow import MainMenuWindow
from windows.StartWindow.StartWindow import StartWindow
from windows.LevelsListWindow.LevelsListWindow import LevelsListWindow
from windows.LevelWindow.LevelWindow import LevelWindow
from windows.ProfileActionsMenuWindow.ProfileActionsMenuWindow import \
    ProfileActionsMenuWindow
from windows.ProfilesMenuWindow.ProfilesMenuWindow import ProfilesMenuWindow
from windows.RestartWindow.RestartWindow import RestartWindow
from windows.StatisticsWindow.StatisticsWindow import StatisticsWindow


class Game:
    def __init__(self):
        self.running = True

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.background_color = BACKGROUND_COLOR
        self.fps = FPS
        self.title = TITLE

        self.windows = {}
        self.add_windows(self.windows)
        self.current_windows = []
        self.add_start_windows(self.current_windows)

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

    def add_start_windows(self, windows: list) -> None:
        for window_name in START_WINDOWS_NAMES:
            windows.append(self.get_windows()[window_name])

    def add_windows(self, windows: dict) -> None:
        windows_list = [(START_WINDOW_NAME, StartWindow),
            (MAIN_MENU_WINDOW_NAME, MainMenuWindow),
            (LEVELS_LIST_WINDOW_NAME, LevelsListWindow),
            (PROFILE_ACTIONS_MENU_WINDOW_NAME,
             ProfileActionsMenuWindow),
            (PROFILES_MENU_WINDOW_NAME, ProfilesMenuWindow)]

        for window in windows_list:
            windows[window[0]] = window[1](self)

    def get_windows(self) -> dict:
        return self.windows


Game()