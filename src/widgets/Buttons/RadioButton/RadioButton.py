import pygame

from widgets.Buttons.Button import Button

from constants.gui import colors


class RadioButton(Button):
    def __init__(self, group, selection_color: pygame.color=colors.RED, *args):
        super().__init__(*args)

        self.selection_color = selection_color
        self.group = group
        self.checked = False

    def render(self, screen: pygame.Surface):
        image = self.get_image()

        if self.get_checked():
            pygame.draw.rect(
                image, self.get_selection_color(), self.get_rect(), 5)

        screen.blit(image, self.get_rect(), self.get_selection_color())

    def update(self, *args):
        event = args[0]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if self.is_pos_inside(event.pos):
                    self.set_checked(True)
                    self.get_group().update(self)

    def get_group(self):
        return self.group

    def get_checked(self) -> bool:
        return self.checked

    def set_checked(self, checked: bool):
        self.checked = checked
        return self

    def get_selection_color(self) -> pygame.Color:
        return self.selection_color
