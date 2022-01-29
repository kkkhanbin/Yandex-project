import pygame

from handlers.ConvertHandler.ConvertHandler import ConvertHandler

from constants.windows.windows_names import STATISTICS_WINDOW_NAME
from constants.windows.level_window.level_window_settings import MAP_POS, \
    MAP_SIZE, HP_BAR_POS, HP_BAR_SIZE
from constants import events

from windows.Window import Window
from windows.LevelWindow.Map.Map import Map
from windows.LevelWindow.HpBar.HpBar import HpBar


class LevelWindow(Window):
    def __init__(self, level_path: str, user_name: str, *args):
        super(LevelWindow, self).__init__(*args)

        self.level_path = level_path
        self.user_name = user_name

        self.add_map()
        self.add_hp_bar()

        # Записываем время в секундах
        self.time_count = 0

    def add_map(self):
        self.map = Map(
            self, self.get_level_path(), *ConvertHandler.convert_percent(
            self.get_screen_size(), MAP_SIZE, MAP_POS))

    def add_hp_bar(self):
        self.hp_bar = HpBar(
            *ConvertHandler.convert_percent(
                self.get_screen_size(), HP_BAR_SIZE, HP_BAR_POS),
            self.get_map().get_hero())

    def tick(self, fps: int):
        self.get_map().tick(fps)
        self.add_time_count(1 / fps)

    def render(self, screen: pygame.Surface):
        super().render(screen)

        self.get_map().render(screen)
        self.get_hp_bar().render(screen)

    def update(self, event: pygame.event.Event):
        self.get_map().update(event)

        if event.type == events.GAME_OVER_EVENT:
            self.game_over()
        elif event.type == events.GAME_COMPLETED_EVENT:
            self.game_completed()

    def game_over(self):
        self.restart()

    def game_completed(self):
        window = self.get_parent().get_windows()\
            [STATISTICS_WINDOW_NAME](self, self.get_parent())
        self.flip_window(window)

    def restart(self):
        self.__init__(self.get_level_path(), self.get_user_name(),
                      self.get_parent())

    def get_map(self) -> Map:
        return self.map

    def get_level_path(self) -> str:
        return self.level_path

    def get_hp_bar(self) -> HpBar:
        return self.hp_bar

    def get_time_count(self) -> float:
        return self.time_count

    def add_time_count(self, time: float):
        self.time_count += time
        return self

    def get_user_name(self) -> str:
        return self.user_name
