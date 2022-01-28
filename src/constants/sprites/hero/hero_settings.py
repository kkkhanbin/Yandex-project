from Sprites.Wall.Wall import Wall
from Sprites.Cannon.Cannon import Cannon

from Sprites.Cannon.Bullet.Bullet import Bullet

IMAGE_PATH = 'data/images/sprites/hero/hero.png'
STEP = 200  # Пикселей в секунду
OBSTACLES = [Wall, Cannon, Bullet]
ENEMIES = [Bullet]
