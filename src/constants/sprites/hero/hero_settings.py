from Sprites.Wall.Wall import Wall
from Sprites.Cannon.Cannon import Cannon
from Sprites.Cannon.Bullet.Bullet import Bullet
from Sprites.Door.Door import Door

IMAGE_PATH = 'data/images/sprites/hero/hero.png'
STEP = 200  # Пикселей в секунду
OBSTACLES = [Wall, Cannon]
ENEMIES = [Bullet]
DESTINATIONS = [Door]
