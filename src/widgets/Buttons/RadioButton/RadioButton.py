import pygame

from widgets.Buttons.Button import Button

from constants.gui import colors


class RadioButton(Button):
    def __init__(self, group, selection_line_width: int,
                 selection_color: pygame.color=colors.RED, *args):
        super().__init__(*args)

        self.selection_line_width = selection_line_width
        self.selection_color = selection_color
        self.group = group
        self.checked = False

        group.add_radio_button(self)

    def render(self, screen: pygame.Surface):
        image = pygame.transform.scale(self.get_image(), self.get_rect().size)

        if self.get_checked():
            pygame.draw.rect(
                image, self.get_selection_color(),
                pygame.Rect(0, 0, *self.get_rect().size),
                self.get_selection_line_width())

        screen.blit(image, self.get_rect())

    def click(self):
        self.set_checked(True)
        self.get_group().normalize_number_of_checked_buttons(self)

    def get_group(self):
        return self.group

    def get_checked(self) -> bool:
        return self.checked

    def set_checked(self, checked: bool):
        self.checked = checked
        return self

    def get_selection_color(self) -> pygame.Color:
        return self.selection_color

    def get_selection_line_width(self) -> int:
        return self.selection_line_width
