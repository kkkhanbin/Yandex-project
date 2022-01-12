import pygame

from constants.gui import colors, fonts


class TextHandler:
    @staticmethod
    def draw_text(screen: pygame.Surface, text: str, pos: tuple,
                  color=colors.WHITE, font=fonts.DEFAULT_FONT):
        text = font.render(text, True, color)
        screen.blit(text, pos)
