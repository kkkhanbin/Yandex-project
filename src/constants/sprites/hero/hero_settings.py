from Sprites.Wall.Wall import Wall
from Sprites.Cannon.Cannon import Cannon
from Sprites.Cannon.Bullet.Bullet import Bullet
from Sprites.Door.Door import Door

IMAGE_PATH = 'data/images/sprites/hero/hero.png'
STEP = 200  # Пикселей в секунду
OBSTACLES = [Wall, Cannon, Bullet]
ENEMIES = [Bullet]
DESTINATIONS = [Door]

set_index = 0
frame_set_start = set_index * 3
frame_set_end = frame_set_start + 2

speed = 5
dwell = 5

running_right = 2
running_left = 20
idle_right = 29
idle_left = 11
