from abc import abstractmethod

import pygame

from widgets.Widget import Widget


class Layout(Widget):
    def __init__(self, widgets: list, spacing: int, *args):
        super().__init__(*args)

        self.widgets = widgets
        self.spacing = spacing

    def add_widget(self, widget: Widget):
        self.widgets.append(widget)

    def get_widgets(self) -> list:
        return self.widgets

    def get_spacing(self) -> int:
        return self.spacing

    def render(self, screen: pygame.Surface):
        for widget in self.get_widgets():
            widget.render(screen)

    @abstractmethod
    def position_widgets(self):
        pass
