import os

import pygame

from constants.windows.windows_names import LEVEL_WINDOW_NAME
from constants.windows.levels_menu_window.levels_menu_window_settings import \
    LEVELS_LAYOUT_ORDER_POS, LEVELS_LAYOUT_FONT_SIZE, LEVELS_LAYOUT_SPACING, \
    LEVELS_LAYOUT_SIZE, LEVELS_LAYOUT_POS, LEVELS_LAYOUT_NAME, \
    LEVEL_ICON_NAME, LEVEL_ICON_MIN_SIZE, CLOSED_ICON_COLOR, \
    OPENED_ICON_COLOR
from constants.paths import LEVELS_PATH, PARAMETERS_PATH
from constants.level.level_settings import STARS_PAR_NAME, OPENED_PAR_NAME, \
    TIME_PAR_NAME, NAME_PAR_NAME, LEVEL_ICON_PATH, DEFAULT_PARAMETERS, \
    PAR_SEPARATOR

from windows.Window import Window

from widgets.Layouts.HorizontalLayout.HorizontalLayout import HorizontalLayout
from widgets.Buttons.PushButton.PushButton import PushButton

from handlers.TextHandler.TextHandler import TextHandler
from handlers.ImageHandler.ImageHandler import ImageHandler
from handlers.ConvertHandler.ConvertHandler import ConvertHandler
from handlers.LevelHandler.LevelHandler import LevelHandler
from handlers.ExceptionHandler.ExceptionHandler import ExceptionHandler


class LevelsMenuWindow(Window):
    def __init__(self, user_name, *args):
        super(LevelsMenuWindow, self).__init__(*args)

        self.user_name = user_name

        self.add_levels_layout()

    def add_levels_layout(self):
        """Добавление лэйаута с уровнями"""
        level_icons = self.setup_level_push_buttons()
        pos, size = ConvertHandler.convert_percent(
            self.get_screen_size(), LEVELS_LAYOUT_POS,
            LEVELS_LAYOUT_SIZE)

        self.levels_layout = HorizontalLayout(
            [], LEVELS_LAYOUT_SPACING, True, LEVELS_LAYOUT_NAME, pos, size)

        for level_icon in level_icons:
            self.get_levels_layout().add_widget(level_icon)

    def setup_level_push_buttons(self) -> list:
        """Настройка иконок уровней"""
        level_push_buttons = []

        for level_name in os.listdir(LEVELS_PATH):
            level_name = os.path.join(LEVELS_PATH, level_name)

            action_info = self.flip_on_level_window, (level_name,), {}
            level_info = LevelHandler().get_level_info(level_name)
            image = self.get_level_icon(level_info)
            min_size = ConvertHandler.convert_percent(
                self.get_parent().get_screen_size(), LEVEL_ICON_MIN_SIZE)[0]
            try:
                enabled = level_info[OPENED_PAR_NAME]
            except TypeError as exception:
                ExceptionHandler().log(exception)
                enabled = True

            level_push_button = \
                PushButton(action_info, image, enabled, LEVEL_ICON_NAME,
                           (0, 0), (0, 0), min_size)
            level_push_buttons.append(level_push_button)

        return level_push_buttons

    def flip_on_level_window(self, level_name: str) -> Window:
        self.flip_window(self.get_parent().get_windows()[LEVEL_WINDOW_NAME]\
            (level_name, self.get_user_name(), self.get_parent()))

    def get_level_icon(self, level_info: dict) -> pygame.Surface:
        temp_screen = ImageHandler.load_image(LEVEL_ICON_PATH)
        size = temp_screen.get_rect().size

        try:
            name = level_info[NAME_PAR_NAME]
            opened = level_info[OPENED_PAR_NAME]
        except TypeError as exception:
            ExceptionHandler().log(exception)
            name, opened = '', False

        icon_color = OPENED_ICON_COLOR \
            if opened else CLOSED_ICON_COLOR
        font = pygame.font.Font(None, LEVELS_LAYOUT_FONT_SIZE)

        pygame.draw.rect(temp_screen, icon_color,
                         pygame.Rect(0, 0, *size))
        TextHandler.draw_text(
            temp_screen, name, LEVELS_LAYOUT_ORDER_POS, font=font)

        return temp_screen

    def render(self, screen: pygame.Surface):
        super().render(screen)
        self.get_levels_layout().render(screen)

    def update(self, event: pygame.event.Event):
        self.get_levels_layout().update(event)

    def start_game(self, level_path: str):
        self.flip_window(self.get_parent().get_windows()
                         [LEVEL_WINDOW_NAME](level_path, self.get_parent()))

    def get_user_name(self) -> str:
        return self.user_name

    def get_levels_layout(self) -> HorizontalLayout:
        return self.levels_layout
