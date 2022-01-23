import sys
import sqlite3

import pygame
pygame.init()

from constants.main_settings import FPS, SIZE, BACKGROUND_COLOR, \
    START_WINDOWS_NAMES, TITLE
from constants.windows.windows_names import START_WINDOW_NAME, \
    MAIN_MENU_WINDOW_NAME, LEVELS_MENU_WINDOW_NAME, PROFILES_MENU_WINDOW_NAME,\
    RESTART_WINDOW_NAME, SETTINGS_WINDOW_NAME, LEVEL_EDITOR_WINDOW_NAME, \
    LEVEL_WINDOW_NAME
from constants.data_base.data_base_settings import USER_NAMES, \
    USER_DATABASE_PATH

from handlers.DataBaseHandler.DataBaseHandler import DataBaseHandler

from windows.Window import Window
from windows.SettingsWindow.SettingsWindow import SettingsWindow
from windows.MainMenuWindow.MainMenuWindow import MainMenuWindow
from windows.StartWindow.StartWindow import StartWindow
from windows.LevelsMenuWindow.LevelsMenuWindow import LevelsMenuWindow
from windows.LevelWindow.LevelWindow import LevelWindow
from windows.ProfilesMenuWindow.ProfilesMenuWindow import ProfilesMenuWindow


class Game:
    def __init__(self):
        self.running = True

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.background_color = BACKGROUND_COLOR
        self.fps = FPS
        self.title = TITLE

        # Настройка окон
        self.windows = {}
        self.add_windows(self.windows)
        self.current_windows = []
        self.add_start_windows(self.current_windows)

        # Настройка БД
        self.setup_data_base()
        self.normalize_data_base()

    def setup_data_base(self):
        self.data_base_handler = DataBaseHandler(
            sqlite3.connect(USER_DATABASE_PATH))

    def normalize_data_base(self):
        """Автоисправление данных в БД"""
        data = self.get_data_base_handler().select(
            'user_progress', ('*',), {}).fetchall()

        # Дополняет таблицу user_progress если в ней не хватает строк для
        # профилей
        if len(data) < len(USER_NAMES):
            for user_name in USER_NAMES:
                if user_name not in list(map(lambda row: row[0], data)):
                    self.get_data_base_handler().insert(
                        'user_progress',
                        ('user_name', 'game_time', 'stars_count'),
                        (f"'{user_name}'", 0, 0))

        self.get_data_base_handler().get_connection().commit()

    def run(self):
        # Цикл игры
        while self.get_running():
            self.get_screen().fill(self.get_background_color())
            pygame.display.set_caption(self.get_title())

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                self.update_current_windows(event)

            # Рендер окон
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

    def get_data_base_handler(self) -> DataBaseHandler:
        return self.data_base_handler

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
            windows.append(self.get_windows()[window_name](self))

    def add_windows(self, windows: dict) -> None:
        windows_info = \
            [(LEVEL_WINDOW_NAME, LevelWindow),
             (START_WINDOW_NAME, StartWindow),
             (MAIN_MENU_WINDOW_NAME, MainMenuWindow),
             (LEVELS_MENU_WINDOW_NAME, LevelsMenuWindow),
             (PROFILES_MENU_WINDOW_NAME, ProfilesMenuWindow),
             (SETTINGS_WINDOW_NAME, SettingsWindow)]

        for window_name, window in windows_info:
            windows[window_name] = window

    def get_windows(self) -> dict:
        return self.windows

    def quit(self):
        """Выход из игры"""
        self.set_running(False)
        self.get_data_base_handler().get_connection().close()
        pygame.quit()
        sys.exit()


def start_game():
    game = Game()
    game.run()


start_game()
