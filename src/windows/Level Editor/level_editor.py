import pygame
import csv
import button
from constants.main_settings import FPS, SIZE
from constants.level_editor.level_editor_settings import TITLE, LOWER_MARGIN, SIDE_MARGIN, ROWS, MAX_COLS, TILE_TYPES, TILE_SIZE, RED, GREEN, BLUE, WHITE
from constants.level_editor.level_editor_settings import SCREEN_WIDTH, SCREEN_HEIGHT
from windows.Window import Window

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Редактор")


class Editor(Window):
	def __init__(self) -> None:
		self.fps = FPS
		self.screen = pygame.display.set_mode(SIZE)
		self.running = True

		self.screen = pygame.display.set_mode(SIZE)
		self.clock = pygame.time.Clock()
		self.red = RED
		self.green = GREEN
		self.blue = BLUE
		self.white = WHITE
		self.title = TITLE
		
		self.rows = ROWS
		self.max_cols = MAX_COLS
		self.tile_size = TILE_SIZE
		self.tile_type = TILE_TYPES

		self.level = 0
		self.current_tile = 0
		self.scroll_left = False
		self.scroll_right = False
		self.scroll = 0
		self.scroll_speed = 1

		# загрузка заднего фона
		self.background1_img = pygame.image.load("img/Background/background1.png").convert_alpha() 
		self.background2_img = pygame.image.load("img/Background/background2.png").convert_alpha()
		self.background3_img = pygame.image.load("img/Background/background3.png").convert_alpha()

		# загрузка кнопок сохранения и загрузки уровня
		save_img = pygame.image.load("images/save_button.png").convert_alpha()
		load_img = pygame.image.load("images/load_button.png").convert_alpha()

		# хранение плиток в списке
		self.images_list = []
		for x in range(TILE_TYPES):
			img = pygame.image.load(f"img/tile/{x}.png").convert_alpha()
			img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
			self.images_list.append(img)


		self.font = pygame.font.SysFont("Futura", 30)

		# список объектов
		self.world_data = []
		for row in range(ROWS):
			r = [-1] * MAX_COLS
			self.world_data.append(r)

		# генерация поверхности
		for i in range(0, MAX_COLS):
			self.world_data[ROWS - 1][i] = 0


		self.self.save_button = button.Button(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT + LOWER_MARGIN - 75, save_img, 1)
		self.load_button = button.Button(SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT + LOWER_MARGIN - 75, load_img, 1)

		# список кнопок
		button_list = []
		button_col = 0
		button_row = 0

		for i in range(len(self.images_list)):
			tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, self.images_list[i], 1)
			button_list.append(tile_button)
			button_col += 1
			if button_col == 3:
				button_row += 1
				button_col = 0

	def get_screen_size(self) -> tuple:
		return self.get_screen().get_size()

	def get_screen(self) -> pygame.Surface:
		return self.screen

	def get_title(self) -> str:
		return self.title

	def set_running(self, running: bool):
		self.running = running
		return self

	def get_running(self) -> bool:
		return self.running

	def tick_current_windows(self, fps):
		for current_window in self.get_current_windows():
			current_window.tick(fps)

	def render_current_windows(self, screen: pygame.Surface):
		for current_window in self.get_current_windows():
			current_window.render(screen)

	def get_clock(self) -> pygame.time.Clock:
		return self.clock

	def get_fps(self) -> float:
		return self.fps

	# функция для вывода текста на экран
	def draw_text(self, text, font, text_col, x, y):
		img = font.render(text, True, text_col)
		screen.blit(img, (x, y))


	# функция для рисования заднего фона
	def draw_background(self):
		screen.fill(BLUE)
		width = self.background3_img.get_width()
		for i in range(3):
			screen.blit(self.background3_img, ((i * width) - self.scroll * 0.5, 0))
			screen.blit(self.background1_img, ((i * width) - self.scroll * 0.7, SCREEN_HEIGHT - self.background1_img.get_height() - 150))
			screen.blit(self.background2_img, ((i * width) - self.scroll * 0.8, SCREEN_HEIGHT - self.background2_img.get_height()))

	# функция для рисовки клеток
	def draw_grid(self):
		# вертикальные линии
		for i in range(MAX_COLS + 1):
			pygame.draw.line(screen, WHITE, (i * TILE_SIZE - self.scroll, 0), (i * TILE_SIZE - self.scroll, SCREEN_HEIGHT))
		# горизонтальные линии
		for i in range(ROWS + 1):
			pygame.draw.line(screen, WHITE, (0, i * TILE_SIZE), (SCREEN_WIDTH, i * TILE_SIZE))


	# функция для рисования объектов мира
	def draw_world(self):
		for i, row in enumerate(self.world_data):
			for j, tile in enumerate(row):
				if tile >= 0:
					screen.blit(self.images_list[tile], (j * TILE_SIZE - self.scroll, i * TILE_SIZE))

	def run(self):
		while self.get_running():
			self.get_clock().tick(round(self.get_fps()))
			pygame.display.set_caption(self.get_title())
			self.draw_background()
			self.draw_grid()
			self.draw_world()
			self.draw_text(f"Уровень: {self.level}", self.font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
			self.draw_text("Нажмите вверх или вниз, чтобы изменить уровень", self.font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

			# сохранение и загрузка данных
			if self.save_button.draw(screen):
				# сохранение данных об уровне
				with open(f"level{self.level}_data.csv", "w", newline="") as csvfile:
					writer = csv.writer(csvfile, delimiter = ",")
					for row in self.world_data:
						writer.writerow(row)
		    # загрузка данных об уровне
			if self.load_button.draw(screen):
				self.scroll = 0
				with open(f"level{self.level}_data.csv", newline="") as csvfile:
					reader = csv.reader(csvfile, delimiter = ",")
					for x, row in enumerate(reader):
						for y, tile in enumerate(row):
							self.world_data[x][y] = int(tile)


			pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

			button_count = 0
			for button_count, i in enumerate(self.button_list):
				if i.draw(screen):
					current_tile = button_count

			pygame.draw.rect(screen, RED, self.button_list[current_tile].rect, 3)

			# прокрутка карты
			if self.scroll_left == True and self.scroll > 0:
				self.scroll -= 5 * self.scroll_speed
			if self.scroll_right == True and self.scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
				self.scroll += 5 * self.scroll_speed

		    # координаты курсора
			pos = pygame.mouse.get_pos()
			x = (pos[0] + self.scroll) // TILE_SIZE
			y = pos[1] // TILE_SIZE

			# проверка координат которые находятся в пределах области объекта
			if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
				# обновляем значение объекта
				if pygame.mouse.get_pressed()[0] == 1:
					if self.world_data[y][x] != current_tile:
						self.world_data[y][x] = current_tile
				if pygame.mouse.get_pressed()[2] == 1:
					self.world_data[y][x] = -1

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.level += 1
					if event.key == pygame.K_DOWN and self.level > 0:
						self.level -= 1
					if event.key == pygame.K_LEFT:
						self.scroll_left = True
					if event.key == pygame.K_RIGHT:
						self.scroll_right = True
					if event.key == pygame.K_RSHIFT:
						self.scroll_speed = 5

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						self.scroll_left = False
					if event.key == pygame.K_RIGHT:
						self.scroll_right = False
					if event.key == pygame.K_RSHIFT:
						self.scroll_speed = 1

			pygame.display.flip()
			pygame.display.update()


def open_editor():
    editor = Editor()
    editor.run()

open_editor()