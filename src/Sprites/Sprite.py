import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

    def update(self, event: pygame.event.Event):
        pass
