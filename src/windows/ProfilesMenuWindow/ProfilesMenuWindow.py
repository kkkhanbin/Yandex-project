import pygame

from windows.Window import Window

from handlers.DataBaseHandler.DataBaseHandler import DataBaseHandler
from handlers.ImageHandler.ImageHandler import ImageHandler

from widgets.Layouts.HorizontalLayout.HorizontalLayout import HorizontalLayout
from widgets.Buttons.RadioButton.RadioButtonGroup.RadioButtonGroup import \
    RadioButtonGroup
from widgets.Buttons.RadioButton.RadioButton import RadioButton

from constants.gui import colors
from constants.main_settings import USER_NAMES
from constants.windows.profiles_menu_window.profiles_menu_window_settings \
    import PROFILES_LAYOUT_POS, PROFILES_LAYOUT_SPACING, \
    PROFILES_LAYOUT_NAME, PROFILES_LAYOUT_SIZE, PROFILE_IMAGE_PATH, \
    RADIO_BUTTON_SELECTION_LINE_WIDTH


class ProfilesMenuWindow(Window):
    def __init__(self, *args):
        super().__init__(*args)

        self.radio_buttons = []
        self.push_buttons = []

        self.add_radio_buttons()
        self.add_push_buttons()

    def add_radio_buttons(self) -> None:
        widgets, name, = \
            self.setup_radio_buttons(), PROFILES_LAYOUT_NAME

        spacing = self.convert_percent(PROFILES_LAYOUT_SPACING)
        pos = self.convert_percent(PROFILES_LAYOUT_POS)
        size = self.convert_percent(PROFILES_LAYOUT_SIZE)

        self.profiles_layout = \
            HorizontalLayout(widgets, spacing, name, pos, size)

    def add_push_buttons(self) -> None:
        pass

    def setup_radio_buttons(self) -> list:
        radio_buttons_group = RadioButtonGroup([])
        radio_buttons = []

        image = ImageHandler.load_image(PROFILE_IMAGE_PATH)

        selection_line_width = \
            self.convert_percent(RADIO_BUTTON_SELECTION_LINE_WIDTH)

        for user_name in USER_NAMES:
            radio_buttons.append(RadioButton(
                radio_buttons_group, selection_line_width, colors.RED,
                image, user_name, (0, 0), (0, 0)))

        radio_buttons[0].set_checked(True)

        return radio_buttons

    def setup_push_buttons(self) -> list:
        pass

    def reset_progress(self, user_name: str) -> None:
        pass

    def continue_game(self, user_name: str) -> None:
        pass

    def get_radio_buttons(self) -> list:
        return self.radio_buttons

    def get_push_buttons(self) -> list:
        return self.push_buttons

    def get_profiles_layout(self) -> HorizontalLayout:
        return self.profiles_layout

    def update(self, event: pygame.event.Event):
        for button in self.get_push_buttons():
            button.update(event)

        self.get_profiles_layout().update(event)

    def render(self, screen: pygame.Surface):
        self.get_profiles_layout().render(screen)
