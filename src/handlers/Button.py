import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, action: tuple, image: pygame.Surface,
                 *groups):
        super().__init__(*groups)

        self.pos = pos
        self.image = image

        self.action = action[0]
        self.action_args = action[1]
        self.action_kwargs = action[2]

        self.rect = self.get_image().get_rect()
        self.update_rect()

    def is_pos_inside(self, pos: tuple) -> bool:
        return self.get_rect().collidepoint(*pos)

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if self.is_pos_inside(event.pos):
                    action, args, kwargs = self.get_action_info()
                    action(*args, **kwargs)

    def update_rect(self):
        x, y = self.get_pos()
        self.get_rect().x = x
        self.get_rect().y = y

    def get_image(self) -> pygame.Surface:
        return self.image

    def get_pos(self) -> tuple:
        return self.pos

    def get_x(self) -> float:
        return self.pos[0]

    def get_y(self) -> float:
        return self.pos[1]

    def set_pos(self, pos: tuple):
        self.pos = pos
        self.update_rect()
        return self

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_action_info(self) -> tuple:
        return self.action, self.action_args, self.action_kwargs