import pygame

from constants.windows.level_window.hp_bar.hp_bar_settings import \
    BORDER_COLOR, BORDER_WIDTH, FILL_COLOR


# Класс для отображения очков здоровья привязанного игрока
class HpBar:
    def __init__(self, size: tuple, pos: tuple, target):
        self.rect = pygame.Rect(*pos, *size)

        # Спрайт игрока к которому "привязан" HpBar
        self.target = target

        self.border_color = BORDER_COLOR
        self.border_width = BORDER_WIDTH

        self.fill_color = FILL_COLOR

    def render(self, screen: pygame.Surface):
        min_hp, hp, max_hp = self.get_target().get_hp_info()
        rect = self.get_rect()

        # Кол-во ОЗ
        hp_amount = max_hp - min_hp
        fill_coeff = hp / hp_amount

        pygame.draw.rect(screen, self.get_fill_color(), pygame.Rect(
            rect.x, rect.y, rect.width * fill_coeff, rect.height))

        # Рамка
        pygame.draw.rect(screen, self.get_border_color(), rect,
                         self.get_border_width())

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_target(self):
        return self.target

    def set_view(self, border_color: pygame.Color, border_width: int,
                 fill_color: pygame.Color):
        self.border_color = border_color
        self.border_width = border_width
        self.fill_color = fill_color

    def get_border_color(self) -> pygame.Color:
        return self.border_color

    def get_border_width(self) -> int:
        return self.border_width

    def get_fill_color(self) -> pygame.Color:
        return self.fill_color
