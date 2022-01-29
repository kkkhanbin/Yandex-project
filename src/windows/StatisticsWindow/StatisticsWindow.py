import os
import math
import csv

import pygame

from constants.paths import PARAMETERS_PATH, LEVELS_PATH
from constants.windows.statistics_window.statistics_window_settings import \
    CONFIRM_PUSH_BUTTON_NAME, CONFIRM_PUSH_BUTTON_POS, \
    CONFIRM_PUSH_BUTTON_SIZE, CONFIRM_PUSH_BUTTON_IMAGE_PATH, \
    RESTART_PUSH_BUTTON_NAME, RESTART_PUSH_BUTTON_POS, \
    RESTART_PUSH_BUTTON_SIZE, RESTART_PUSH_BUTTON_IMAGE_PATH, \
    MIN_NUMBER_OF_STARS, MAX_NUMBER_OF_STARS, STARS_POS, \
    STARS_SIZE, STARS_SPACING, STAR_IMAGE_PATH, TIME_COUNT_POS, \
    TIME_COUNT_FONT, TIME_COUNT_COLOR, TIME_COUNT_MESSAGE
from constants.windows.windows_names import MAIN_MENU_WINDOW_NAME, \
    LEVEL_WINDOW_NAME
from constants.level.level_settings import STARS_PAR_NAME, OPENED_PAR_NAME, \
    TIME_PAR_NAME, NAME_PAR_NAME, LEVEL_ICON_PATH, DEFAULT_PARAMETERS, \
    PAR_SEPARATOR, UNLOCK_LEVEL_NAME

from handlers.ConvertHandler.ConvertHandler import ConvertHandler
from handlers.ImageHandler.ImageHandler import ImageHandler
from handlers.LevelHandler.LevelHandler import LevelHandler

from widgets.Buttons.PushButton.PushButton import PushButton

from windows.Window import Window
from windows.StatisticsWindow.Star.Star import Star
from windows.StatisticsWindow.TimeCount.TimeCount import TimeCount


class StatisticsWindow(Window):
    def __init__(self, level_window: Window, *args):
        super(StatisticsWindow, self).__init__(*args)

        self.level_window = level_window

        self.setup_level_info()
        self.save_in_data_base()
        self.save_in_level_parameters()
        self.unlock_level()

        self.push_buttons = []
        self.add_push_buttons()
        self.add_stars()
        self.add_time()

    def render(self, screen: pygame.Surface):
        super().render(screen)

        for button in self.get_push_buttons():
            button.render(screen)

        for star in self.get_stars():
            star.render(screen)

        self.get_time_count_widget().render(screen)

    def update(self, event: pygame.event.Event):
        for button in self.get_push_buttons():
            button.update(event)

    def setup_level_info(self):
        """Установка нужных значений уровня для
        вывода их на экран и запись в БД"""
        self.time_count = self.get_level_window().get_time_count()
        self.user_name = self.get_level_window().get_user_name()

        min_hp, hp, max_hp = \
            self.get_level_window().get_map().get_hero().get_hp_info()
        self.stars_count = math.floor(
            (hp / (max_hp - min_hp)) *
            (MAX_NUMBER_OF_STARS - MIN_NUMBER_OF_STARS))

        self.parameters_path = \
            os.path.join(self.get_level_window().get_level_path(),
                         PARAMETERS_PATH)

        with open(self.get_parameters_path(), mode='r', encoding='utf-8') \
                as parameters:
            file_rows = list(
                csv.DictReader(parameters, delimiter=PAR_SEPARATOR))[0]
            self.unlock_level_path = \
                os.path.join(LEVELS_PATH, file_rows[UNLOCK_LEVEL_NAME])

    def save_in_data_base(self):
        """Сохранение прогресса в БД"""
        handler = self.get_parent().get_data_base_handler()

        # Запоминаем информацию о профиле
        user_info = handler.select(
            'user_progress', ('game_time', 'stars_count'),
            {'user_name': self.get_user_name()}).fetchone()

        # Записываем измененную информацию о профиле
        handler.update('user_progress', {'game_time': float(user_info[0]) +
            self.get_time_count(), 'stars_count': int(user_info[1]) +
            self.get_stars_count()}, {'user_name': self.get_user_name()})

        handler.commit()

    def update_parameters_file(self, path: str, func):
        """Обновляет файл параметров уровня, исходя из его текущего наполнения.
        В вашу функцию передается сохраненное значение - словарь, которое было
        до его перезаписи, а функция должна менять это значение, после чего
        новый словарь будет записан"""
        with open(path, mode='r', encoding='utf-8') \
                as parameters:
            # Запоминаем содержимое файла
            file_rows = list(
                csv.DictReader(parameters, delimiter=PAR_SEPARATOR))[0]

        with open(path, mode='w+', encoding='utf-8') \
                as parameters:
            writer = csv.DictWriter(parameters, delimiter=PAR_SEPARATOR,
                                    fieldnames=file_rows.keys())
            writer.writeheader()

            # Меняем полученные значения
            func(file_rows)

            # И записываем их обратно
            writer.writerow(file_rows)

    def unlock_level(self):
        """Открывает следующий уровень"""
        self.update_parameters_file(
            os.path.join(self.get_unlock_level_path(), PARAMETERS_PATH),
            self.set_unlock_parameter)

    def set_unlock_parameter(self, file_rows: dict):
        """Функция созданная для update_parameters_file"""
        file_rows[OPENED_PAR_NAME] = 'True'

    def save_in_level_parameters(self):
        """Сохранение прогресса в параметры уровня"""
        self.update_parameters_file(self.get_parameters_path(),
            self.add_parameters)

    def add_parameters(self, file_rows: dict):
        """Функция созданная для update_parameters_file"""
        file_rows[STARS_PAR_NAME] = \
            self.get_stars_count() + int(file_rows[STARS_PAR_NAME])
        file_rows[TIME_PAR_NAME] = \
            self.get_time_count() + float(file_rows[TIME_PAR_NAME])

    def add_stars(self):
        """Добавляем звезды"""
        self.stars = []
        size, pos, spacing = ConvertHandler.convert_percent(
            self.get_parent().get_screen_size(),
            STARS_SIZE, STARS_POS, (STARS_SPACING, STARS_SPACING))
        spacing = spacing[0]
        star_width = size[0] / (MAX_NUMBER_OF_STARS - MIN_NUMBER_OF_STARS) -\
                     spacing / 2

        image = ImageHandler.load_image(STAR_IMAGE_PATH, -1)

        for i in range(self.get_stars_count()):
            x, y = pos[0] + spacing + i * (star_width + spacing), \
                   pos[1] + spacing
            w, h = star_width, size[1] - 2 * spacing

            self.get_stars().append(Star(image, (x, y), (w, h)))

    def add_time(self):
        """Добавляем отображение времени прохождения"""
        self.time_count_widget = TimeCount(TIME_COUNT_MESSAGE.format(round(
            self.get_time_count())),
            *ConvertHandler.convert_percent(
            self.get_parent().get_screen_size(), TIME_COUNT_POS),
            TIME_COUNT_FONT, TIME_COUNT_COLOR)

    def add_push_buttons(self):
        for button in self.setup_push_buttons():
            self.push_buttons.append(PushButton(*button))

    def setup_push_buttons(self) -> list:
        """Установка кнопок"""
        buttons = []
        windows = self.get_parent().get_windows()

        # action_info, image, enabled, name, pos, size

        # Кнопка перехода в меню уровней
        action_info = self.flip_window, (
            windows[MAIN_MENU_WINDOW_NAME](self.get_parent()),), {}
        pos, size = ConvertHandler.convert_percent(
            self.get_parent().get_screen_size(), CONFIRM_PUSH_BUTTON_POS,
            CONFIRM_PUSH_BUTTON_SIZE)
        image = pygame.transform.scale(ImageHandler.load_image(
            CONFIRM_PUSH_BUTTON_IMAGE_PATH, -1), size)
        name = CONFIRM_PUSH_BUTTON_NAME
        buttons.append((action_info, image, True, name, pos, size))

        # Кнопка рестарта уровня
        action_info = self.restart_level, (), {}
        pos, size = ConvertHandler.convert_percent(
            self.get_parent().get_screen_size(), RESTART_PUSH_BUTTON_POS,
            RESTART_PUSH_BUTTON_SIZE)
        image = pygame.transform.scale(ImageHandler.load_image(
            RESTART_PUSH_BUTTON_IMAGE_PATH, -1), size)
        name = RESTART_PUSH_BUTTON_NAME
        buttons.append((action_info, image, True, name, pos, size))

        return buttons

    def restart_level(self):
        windows, level = \
            self.get_parent().get_windows(), self.get_level_window()
        self.flip_window(windows[LEVEL_WINDOW_NAME](
            level.get_level_path(), level.get_user_name(), self.get_parent()))

    def get_level_window(self) -> Window:
        return self.level_window

    def get_push_buttons(self) -> list:
        return self.push_buttons

    def get_time_count(self) -> float:
        return self.time_count

    def get_stars_count(self) -> int:
        return self.stars_count

    def get_user_name(self) -> str:
        return self.user_name

    def get_stars(self) -> list:
        return self.stars

    def get_time_count_widget(self) -> TimeCount:
        return self.time_count_widget

    def get_parameters_path(self) -> str:
        return self.parameters_path

    def get_unlock_level_path(self) -> str:
        return self.unlock_level_path
