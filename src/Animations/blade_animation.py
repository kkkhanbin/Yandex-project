import pygame
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.attack_animation = False
        self.sprites = []
        for i in range(1, 36):
            self.sprites.append(pygame.image.load(rf"Yandex-project-develop\src\data\images\animations\Blade_{i}.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def attack(self):
        self.attack_animation = True

    def update(self, speed):
        if self.attack_animation is True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

pygame.init()
clock = pygame.time.Clock()

screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

moving_sprites = pygame.sprite.Group()
player = Player(100, 100)
moving_sprites.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            player.attack()

    screen.fill((0, 0, 0))
    moving_sprites.draw(screen)
    moving_sprites.update(0.25)
    pygame.display.flip()
    clock.tick(120)
