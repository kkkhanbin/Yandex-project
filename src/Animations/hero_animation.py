import pygame
pygame.init()

set_index = 0
frame_set_start = set_index * 3
frame_set_end = frame_set_start + 2

speed = 5
dwell = 5

running_right = 2
running_left = 20
idle_right = 29
idle_left = 11

class AnimatedSprite:
    def __init__(self, screen, x, y, frames):
        self.screen = screen
        self.x = x
        self.y = y
        self.index = 0
        self.frames = frames
        self.rect = self.frames[self.index].get_rect()
        self.dwell_countdown = dwell

    def advanceImage(self):
        self.dwell_countdown -= 1
        if self.dwell_countdown < 0:
            self.dwell_countdown = dwell
            self.index = (self.index+1)%(frame_set_end+1)
            if self.index<frame_set_start:
                self.index = frame_set_start

    def draw(self):
        self.screen.blit(self.frames[self.index],
                     ( int(self.x-self.rect.width/2),
                       int(self.y-self.rect.height/2) ))



def strip_from_sheet():
    sheet = pygame.image.load(r"Yandex-project-develop\src\data\images\animations\Hero_Move.png").convert()

    rectangle = sheet.get_rect()
    rows = 3
    columns = 6
    img_width = rectangle.w/columns
    img_height = rectangle.h/rows

    frames = []
    for row in range(rows):
        for col in range(columns):
            rect = pygame.Rect(col*img_width, row*img_height, img_width, img_height)
            frames.append(sheet.subsurface(rect))

    for row in range(rows):
        for col in range(columns):
            rect = pygame.Rect(col*img_width, row*img_height, img_width, img_height)
            frames.append(pygame.transform.flip(sheet.subsurface(rect), True, False))

    return frames



clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))

frames = strip_from_sheet()
dimensions = frames[0].get_rect()
scaling = 1
dimensions = (int(dimensions.w*scaling),int(dimensions.h*scaling))

for i in range(len(frames)):
    frames[i] = pygame.transform.scale(
                            frames[i],
                            dimensions)

sprite = AnimatedSprite(screen, 200, 300, frames)


image = pygame.image.load(r"Yandex-project-develop\src\data\images\animations\Hero_Move.png").convert()
rect = pygame.Rect(100, 100, 100, 100)
random_image = image.subsurface(rect)



done = False
while not done:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        sprite.x-=speed
    if pressed[pygame.K_RIGHT]:
        sprite.x+=speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_RIGHT:
                set_index = running_right
            elif event.key == pygame.K_LEFT:
                set_index = running_left
            elif event.key == pygame.K_UP:
                pass
            elif event.key == pygame.K_DOWN:
                pass
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                set_index = idle_right
            elif event.key == pygame.K_LEFT:
                set_index = idle_left
        frame_set_start = set_index*3
        frame_set_end = frame_set_start+2

    screen.fill((0,0,0))
    sprite.draw()
    sprite.advanceImage()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
