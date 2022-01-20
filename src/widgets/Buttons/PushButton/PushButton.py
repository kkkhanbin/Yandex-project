import pygame

from widgets.Buttons.Button import Button


class PushButton(Button):
    def __init__(self, action_info: tuple, *args):
        super().__init__(*args)

        self.action = action_info[0]
        self.action_args = action_info[1]
        self.action_kwargs = action_info[2]

    def render(self, screen: pygame.Surface):
        image = pygame.transform.scale(self.get_image(), self.get_rect().size)
        screen.blit(image, self.get_rect())

    def click(self):
        action, args, kwargs = self.get_action_info()
        action(*args, **kwargs)

    def get_action_info(self) -> tuple:
        return self.action, self.action_args, self.action_kwargs
