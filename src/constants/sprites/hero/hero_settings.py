from constants.sprites.sprites_settings import DOOR_SPRITE_NAME, \
    BULLET_SPRITE_NAME


IMAGE_PATH = 'data/images/sprites/hero/hero.png'
STEP = 200  # Пикселей в секунду
ENEMIES = [BULLET_SPRITE_NAME]
DESTINATIONS = [DOOR_SPRITE_NAME]

set_index = 0
frame_set_start = set_index * 3
frame_set_end = frame_set_start + 2

speed = 5
dwell = 5

running_right = 2
running_left = 20
idle_right = 29
idle_left = 11
