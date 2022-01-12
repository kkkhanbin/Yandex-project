import pygame


class Cell(Map):
    def __init__(self, *group):
        super().__init__(*group)
        self.hero = hero
        self.wall = wall
        self.thorns = thorns
        self.key = key

    def update(self, *args):
        pass
