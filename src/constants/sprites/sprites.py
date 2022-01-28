from Sprites.Hero.Hero import Hero
from Sprites.Cannon.Cannon import Cannon
from Sprites.Door.Door import Door
from Sprites.Ladder.Ladder import Ladder
from Sprites.Saws.Saws import Saws
from Sprites.Wall.Wall import Wall

from constants.sprites.sprites_settings import HERO_SPRITE_NAME, \
    CANNON_SPRITE_NAME, DOOR_SPRITE_NAME, LADDER_SPRITE_NAME, \
    SAWS_SPRITE_NAME, WALL_SPRITE_NAME

SPRITES = {HERO_SPRITE_NAME: Hero, CANNON_SPRITE_NAME: Cannon,
           DOOR_SPRITE_NAME: Door, LADDER_SPRITE_NAME: Ladder,
           SAWS_SPRITE_NAME: Saws, WALL_SPRITE_NAME: Wall}
