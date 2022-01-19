from abc import abstractmethod

import pygame

from widgets.Widget import Widget


class Layout(Widget):
    def __init__(self, widgets: list, spacing: int, *args):
        super().__init__(*args)

        self.widgets = widgets
        self.spacing = spacing

        self.position_widgets()

    def add_widget(self, widget: Widget):
        self.widgets.append(widget)

        self.position_widgets()

    def get_widgets(self) -> list:
        return self.widgets

    def get_spacing(self) -> int:
        return self.spacing

    def render(self, screen: pygame.Surface):
        for widget in self.get_widgets():
            widget.render(screen)

    def update(self, event: pygame.event.Event):
        for widget in self.get_widgets():
            widget.update(event)

    @abstractmethod
    def position_widgets(self):
        pass
