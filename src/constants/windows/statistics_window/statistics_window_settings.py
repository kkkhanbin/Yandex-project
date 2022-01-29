import pygame

from constants.gui.colors import WHITE

CONFIRM_PUSH_BUTTON_NAME = 'confirm_push_button'
CONFIRM_PUSH_BUTTON_POS = 0.15, 0.7
CONFIRM_PUSH_BUTTON_SIZE = 0.3, 0.3
CONFIRM_PUSH_BUTTON_IMAGE_PATH = \
    'data/images/windows/statistics_window/confirm_push_button_image.jpg'

RESTART_PUSH_BUTTON_NAME = 'restart_push_button'
RESTART_PUSH_BUTTON_POS = 0.55, 0.7
RESTART_PUSH_BUTTON_SIZE = 0.3, 0.3
RESTART_PUSH_BUTTON_IMAGE_PATH = \
    'data/images/windows/statistics_window/restart_push_button_image.png'

STAR_IMAGE_PATH = 'data/images/windows/statistics_window/star.jpg'

STARS_POS = 0.1, 0.1
STARS_SIZE = 0.8, 0.5
STARS_SPACING = 0.01

TIME_COUNT_POS = 0.3, 0.6
TIME_COUNT_FONT = pygame.font.Font(None, 25)
TIME_COUNT_COLOR = WHITE
TIME_COUNT_MESSAGE = 'Ваше время прохождения: {} секунд!'

MIN_NUMBER_OF_STARS = 0
MAX_NUMBER_OF_STARS = 3
