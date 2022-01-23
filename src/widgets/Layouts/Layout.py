from abc import abstractmethod

import pygame

from widgets.Widget import Widget

from constants.widgets.Layouts.layout_settings import SHIFT


class Layout(Widget):
    def __init__(self, widgets: list, spacing: int, scrolling: bool, *args):
        super().__init__(*args)

        self.widgets = widgets
        self.spacing = spacing
        self.scrolling = scrolling

        self.shift = SHIFT

        self.position_widgets()

    def add_widget(self, widget: Widget):
        self.widgets.append(widget)

        self.position_widgets()

    def get_widgets(self) -> list:
        return self.widgets

    def get_spacing(self) -> int:
        return self.spacing

    def update(self, event: pygame.event.Event):
        for widget in self.get_widgets():
            widget.update(event)

        if self.get_scrolling():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.get_rect().collidepoint(event.pos):
                    if event.button == pygame.BUTTON_WHEELUP:
                        self.update_shift(self.get_shift())
                    elif event.button == pygame.BUTTON_WHEELDOWN:
                        self.update_shift(-self.get_shift())

    def get_shift(self) -> int:
        return self.shift

    def get_scrolling(self) -> bool:
        return self.scrolling

    def render(self, screen: pygame.Surface):
        for widget in self.get_widgets():
            widget.render(screen)

    @abstractmethod
    def update_shift(self, shift):
        pass

    @abstractmethod
    def position_widgets(self):
        pass
