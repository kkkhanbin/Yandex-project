import pygame

from handlers.TextHandler.TextHandler import TextHandler


class TimeCount:
    def __init__(self, text: str, pos: tuple, font: pygame.font.Font,
                 color: pygame.color.Color):
        self.text = text
        self.pos = pos
        self.font = font
        self.color = color

    def render(self, screen: pygame.Surface):
        TextHandler.draw_text(screen, self.get_text(), self.get_pos(),
                              self.get_color(), self.get_font())

    def get_pos(self) -> tuple:
        return self.pos

    def get_text(self) -> str:
        return self.text

    def get_font(self) -> pygame.font.Font:
        return self.font

    def get_color(self) -> pygame.color.Color:
        return self.color
