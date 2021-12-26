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


class CellSprite(Cell):
    def __init__(self, *arg):
        super(CellSprite, self).__init__()
        self.arg = arg


class Hero(CellSprite):
    pass


class Spikes(CellSprite):
    pass


class Enemy(CellSprite):
    pass


class Key(CellSprite):
    pass
