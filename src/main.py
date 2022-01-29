import sys
import sqlite3

import pygame
pygame.init()

from constants.main_settings import FPS, SIZE, BACKGROUND_COLOR, \
    START_WINDOWS_NAME, TITLE
from constants.windows.windows_names import START_WINDOW_NAME, \
    MAIN_MENU_WINDOW_NAME, LEVELS_MENU_WINDOW_NAME, PROFILES_MENU_WINDOW_NAME,\
    RESTART_WINDOW_NAME, SETTINGS_WINDOW_NAME, LEVEL_EDITOR_WINDOW_NAME, \
    LEVEL_WINDOW_NAME
from constants.data_base.data_base_settings import USER_NAMES, \
    USER_DATABASE_PATH

from handlers.DataBaseHandler.DataBaseHandler import DataBaseHandler
from handlers.WindowsLogHandler.WindowsLogHandler import WindowsLogHandler

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

        self.current_window = self.get_start_window()
        self.windows_log = WindowsLogHandler([self.get_current_window()])

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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.get_windows_log().pop()
                        self.current_window = self.get_windows_log().get()[-1]
                self.get_current_window().update(event)

            self.get_current_window().tick(self.get_fps())
            self.get_current_window().render(self.get_screen())

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

    def get_current_window(self) -> Window:
        return self.current_window

    def get_screen_size(self) -> tuple:
        return self.get_screen().get_size()

    def get_title(self) -> str:
        return self.title

    def set_current_window(self, window: Window):
        self.current_window = window
        self.get_windows_log().add([window])

    def get_start_window(self) -> Window:
        return self.get_windows()[START_WINDOWS_NAME](self)

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

    def get_windows_log(self) -> WindowsLogHandler:
        return self.windows_log

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
