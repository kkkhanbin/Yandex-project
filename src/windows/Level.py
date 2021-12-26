import pygame


class Level():
    def __init__(self, *args):
        super(Level, self).__init__(*args)

        self.parent = parent
        self.leve_map = level_map
        self.level_name = level_name
        self.step_counts = step_counts

    def render(self, screen: pygame.Surface):
        pass

    def update(self, *args):
        pass

    def get_parent(self):
        return self.parent