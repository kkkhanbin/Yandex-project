import pygame
import button

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Редактор")


# параметры
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 12


# загрузка заднего фона
background1_img = pygame.image.load("img/Background/background1.png").convert_alpha() 
background2_img = pygame.image.load("img/Background/background2.png").convert_alpha()
background3_img = pygame.image.load("img/Background/background3.png").convert_alpha()

# хранение плиток в списке
images_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f"img/tile/{x}.png").convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	images_list.append(img)


GREEN = (81, 197, 0)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
BLUE = (51, 133, 255)

font = pygame.font.SysFont("Futura", 30)

# список объектов
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

# генерация поверхности
for i in range(0, MAX_COLS):
	world_data[ROWS - 1][i] = 0


# функция для вывода текста на экран
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


# функция для рисования заднего фона
def draw_background():
	screen.fill(BLUE)
	width = background3_img.get_width()
	for i in range(3):
		screen.blit(background3_img, ((i * width) - scroll * 0.5, 0))
		screen.blit(background1_img, ((i * width) - scroll * 0.7, SCREEN_HEIGHT - background1_img.get_height() - 150))
		screen.blit(background2_img, ((i * width) - scroll * 0.8, SCREEN_HEIGHT - background2_img.get_height()))

# функция для рисовки клеток
def draw_grid():
	# вертикальные линии
	for i in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (i * TILE_SIZE - scroll, 0), (i * TILE_SIZE - scroll, SCREEN_HEIGHT))
	# горизонтальные линии
	for i in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, i * TILE_SIZE), (SCREEN_WIDTH, i * TILE_SIZE))


# функция для рисования объектов мира
def draw_world():
	for i, row in enumerate(world_data):
		for j, tile in enumerate(row):
			if tile >= 0:
				screen.blit(images_list[tile], (j * TILE_SIZE - scroll, i * TILE_SIZE))


# список кнопок
button_list = []
button_col = 0
button_row = 0

for i in range(len(images_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, images_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0

run = True
while run:
	clock.tick(FPS)
	draw_background()
	draw_grid()
	draw_world()
	draw_text(f"Уровень: {level}", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text("Нажмите вверх или вниз, чтобы изменить уровень", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	# прокрутка карты
	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

    # координаты курсора
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	# проверка координат которые находятся в пределах области объекта
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		# обновляем значение объекта
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1


	pygame.display.update()

pygame.quit()
