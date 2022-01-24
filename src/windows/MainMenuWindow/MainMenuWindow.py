import pygame

from windows.Window import Window

from handlers.TextHandler.TextHandler import TextHandler
from handlers.ImageHandler.ImageHandler import ImageHandler
from handlers.ConvertHandler.ConvertHandler import ConvertHandler

from widgets.Buttons.PushButton.PushButton import PushButton

from constants.gui import colors
from constants.windows.windows_names import START_WINDOW_NAME, \
    SETTINGS_WINDOW_NAME, PROFILES_MENU_WINDOW_NAME, LEVEL_EDITOR_WINDOW_NAME
from constants.windows.main_menu_window.main_menu_window_settings \
    import DEFAULT_BUTTON_SIZE, OPEN_PROFILES_MENU_WINDOW_BUTTON_PATH, \
    OPEN_PROFILES_MENU_WINDOW_BUTTON_POS, OPEN_SETTINGS_WINDOW_BUTTON_PATH, \
    OPEN_SETTINGS_WINDOW_BUTTON_POS, OPEN_LEVEL_EDITOR_WINDOW_BUTTON_PATH, \
    OPEN_LEVEL_EDITOR_WINDOW_BUTTON_POS, TITLE_FONT_SIZE, TITLE_POS, \
    BACKGROUND_IMAGE_PATH, BACKGROUND_IMAGE_POS, \
    OPEN_PROFILES_MENU_WINDOW_BUTTON_NAME, OPEN_SETTINGS_WINDOW_BUTTON_NAME, \
    OPEN_LEVEL_EDITOR_WINDOW_BUTTON_NAME


class MainMenuWindow(Window):
    def __init__(self, *args):
        super().__init__(*args)

        self.push_buttons = []
        self.add_background()
        self.add_push_buttons()
        self.add_text()

    def add_push_buttons(self) -> None:
        buttons_args = self.setup_push_buttons()
        for buttons_arg in buttons_args:
            action, name, pos, image_path, size, colorkey = buttons_arg

            pos = ConvertHandler.convert_percent(self.get_screen_size(), pos)
            image = pygame.transform.scale(
                ImageHandler.load_image(image_path, colorkey), size)

            # action_info, image, enabled, name, pos, size
            button = PushButton(action, image, True, name, pos, size)
            self.get_push_buttons().append(button)

    def setup_push_buttons(self) -> list:
        default_button_size = ConvertHandler.convert_percent(
            self.get_screen_size(), DEFAULT_BUTTON_SIZE)

        buttons = [
            ((self.flip_window,
              (self.get_parent().get_windows()[SETTINGS_WINDOW_NAME]
               (self.get_parent()),), {}),
             OPEN_SETTINGS_WINDOW_BUTTON_NAME, OPEN_SETTINGS_WINDOW_BUTTON_POS,
             OPEN_SETTINGS_WINDOW_BUTTON_PATH, default_button_size, -1),

            ((self.flip_window,
              (self.get_parent().get_windows()[START_WINDOW_NAME]
               (self.get_parent()),), {}),
             OPEN_LEVEL_EDITOR_WINDOW_BUTTON_NAME,
             OPEN_LEVEL_EDITOR_WINDOW_BUTTON_POS,
             OPEN_LEVEL_EDITOR_WINDOW_BUTTON_PATH, default_button_size, -1),

            ((self.flip_window,
              (self.get_parent().get_windows()[PROFILES_MENU_WINDOW_NAME]
               (self.get_parent()),), {}),
             OPEN_PROFILES_MENU_WINDOW_BUTTON_NAME,
             OPEN_PROFILES_MENU_WINDOW_BUTTON_POS,
             OPEN_PROFILES_MENU_WINDOW_BUTTON_PATH, default_button_size, -1)
        ]

        return buttons

    def add_text(self):
        # Добавляем название программы на экран
        title = self.get_parent().get_title()
        title_pos = ConvertHandler.convert_percent(
            self.get_screen_size(), TITLE_POS)
        title_size = TITLE_FONT_SIZE
        title_font = pygame.font.Font(None, title_size)

        TextHandler.draw_text(self.get_screen(), title, title_pos,
                              font=title_font, color=colors.RED)

    def add_background(self):
        self.get_screen().blit(pygame.transform.scale(
            ImageHandler.load_image(BACKGROUND_IMAGE_PATH),
            self.get_parent().get_screen_size()), BACKGROUND_IMAGE_POS)

    def render(self, screen: pygame.Surface):
        self.render_buttons(self.get_screen())

        super().render(screen)

    def render_buttons(self, screen: pygame.Surface):
        for button in self.get_push_buttons():
            button.render(screen)

    def update(self, event: pygame.event.Event):
        for button in self.get_push_buttons():
            button.update(event)

    def get_push_buttons(self) -> list:
        return self.push_buttons

    def get_button_size(self) -> tuple:
        return self.button_size

    def get_button_width(self) -> float:
        return self.get_button_size()[0]

    def get_button_height(self) -> float:
        return self.get_button_size()[1]
