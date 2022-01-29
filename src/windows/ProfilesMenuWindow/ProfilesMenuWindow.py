import pygame

from windows.Window import Window

from handlers.ImageHandler.ImageHandler import ImageHandler
from handlers.ConvertHandler.ConvertHandler import ConvertHandler

from widgets.Layouts.HorizontalLayout.HorizontalLayout import HorizontalLayout
from widgets.Layouts.VerticalLayout.VerticalLayout import VerticalLayout
from widgets.Buttons.RadioButton.RadioButtonGroup.RadioButtonGroup import \
    RadioButtonGroup
from widgets.Buttons.RadioButton.RadioButton import RadioButton
from widgets.Buttons.PushButton.PushButton import PushButton

from constants.windows.windows_names import LEVELS_MENU_WINDOW_NAME
from constants.data_base.data_base_settings import USER_NAMES, \
    USER_DATABASE_PATH
from constants.gui import colors
from constants.windows.profiles_menu_window.profiles_menu_window_settings \
    import PROFILES_LAYOUT_POS, PROFILES_LAYOUT_SPACING, \
    PROFILES_LAYOUT_NAME, PROFILES_LAYOUT_SIZE, \
    PROFILE_RADIO_BUTTON_IMAGE_PATH, RADIO_BUTTON_SELECTION_LINE_WIDTH, \
    RESET_PROGRESS_PUSH_BUTTON_PATH, RESET_PROGRESS_PUSH_BUTTON_NAME, \
    CONTINUE_GAME_PUSH_BUTTON_NAME, CONTINUE_GAME_PUSH_BUTTON_PATH, \
    GAME_ACTIONS_LAYOUT_POS, GAME_ACTIONS_LAYOUT_SIZE, \
    GAME_ACTIONS_LAYOUT_SPACING, GAME_ACTIONS_LAYOUT_NAME


class ProfilesMenuWindow(Window):
    def __init__(self, *args):
        super().__init__(*args)

        self.profiles_radio_buttons = []
        self.game_actions_push_buttons = []

        self.layouts = []
        self.add_layouts()

    def add_layouts(self):
        """Добавляем лэйауты окна"""
        layouts_info = [
            (self.setup_profiles_radio_buttons(), PROFILES_LAYOUT_NAME,
             PROFILES_LAYOUT_SPACING, PROFILES_LAYOUT_POS,
             PROFILES_LAYOUT_SIZE, HorizontalLayout),

            (self.setup_game_actions_push_buttons(), GAME_ACTIONS_LAYOUT_NAME,
             GAME_ACTIONS_LAYOUT_SPACING, GAME_ACTIONS_LAYOUT_POS,
             GAME_ACTIONS_LAYOUT_SIZE, VerticalLayout)
        ]

        for layout_info in layouts_info:
            widgets, name, spacing, pos, size, layout = layout_info

            pos, size = ConvertHandler.convert_percent(
                self.get_screen_size(), pos, size)

            self.get_layouts().append(
                layout(widgets, spacing, False, name, pos, size))

    def setup_profiles_radio_buttons(self) -> list:
        """Настраиваем радио-кнопки профилей"""
        self.profiles_radio_buttons_group = RadioButtonGroup([])
        radio_buttons = []

        image = ImageHandler.load_image(PROFILE_RADIO_BUTTON_IMAGE_PATH)

        selection_line_width = RADIO_BUTTON_SELECTION_LINE_WIDTH

        for user_name in USER_NAMES:
            radio_buttons.append(RadioButton(
                self.get_profiles_radio_buttons_group(),
                selection_line_width, colors.RED,
                image, True, user_name, (0, 0), (0, 0)))

        radio_buttons[0].set_checked(True)

        return radio_buttons

    def setup_game_actions_push_buttons(self) -> list:
        """Настраиваем кнопки взаимодействия с игрой"""
        push_buttons = []

        # ResetProgressPushButton
        image = ImageHandler.load_image(RESET_PROGRESS_PUSH_BUTTON_PATH)
        action_info = (self.reset_progress, (), {})
        push_buttons.append(PushButton(
            action_info, image, True, RESET_PROGRESS_PUSH_BUTTON_NAME,
            (0, 0), (0, 0)))

        # ContinueGamePushButton
        image = ImageHandler.load_image(CONTINUE_GAME_PUSH_BUTTON_PATH)
        action_info = (self.continue_game, (), {})
        push_buttons.append(PushButton(
            action_info, image, True, CONTINUE_GAME_PUSH_BUTTON_NAME,
            (0, 0), (0, 0)))

        return push_buttons

    def reset_progress(self) -> None:
        """Обнуление данных профиля в БД"""
        user_name = self.get_profiles_radio_buttons_group()\
            .get_checked_button().get_name()
        db_handler = self.get_parent().get_data_base_handler()

        db_handler.update(
            'user_progress', {'game_time': 0, 'stars_count': 0},
            {'user_name': user_name})

        db_handler.get_connection().commit()

        self.start_game(user_name)

    def continue_game(self) -> None:
        user_name = self.get_profiles_radio_buttons_group()\
            .get_checked_button().get_name()
        self.start_game(user_name)

    def start_game(self, user_name):
        self.flip_window(
            self.get_parent().get_windows()[LEVELS_MENU_WINDOW_NAME]
            (user_name, self.get_parent()))

    def get_profiles_radio_buttons_group(self) -> RadioButtonGroup:
        return self.profiles_radio_buttons_group

    def get_layouts(self) -> list:
        return self.layouts

    def update(self, event: pygame.event.Event):
        for layout in self.get_layouts():
            layout.update(event)

    def render(self, screen: pygame.Surface):
        super().render(screen)

        for layout in self.get_layouts():
            layout.render(screen)
