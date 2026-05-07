import pygame
import random
import sys
import os

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Константы
TILE_SIZE = 32  # Размер клетки в пикселях
MARGIN = 1      # Отступ между клетками
INFO_PANEL_HEIGHT = 150  # Высота информационной панели с кнопками

# Предустановленные уровни сложности
DIFFICULTY_LEVELS = {
    "Новичок": {"width": 8, "height": 8, "mines": 10},
    "Любитель": {"width": 12, "height": 12, "mines": 25},
    "Профессионал": {"width": 16, "height": 16, "mines": 40},
    "Эксперт": {"width": 20, "height": 16, "mines": 60}
}



# Цвета (RGB)
COLORS = {
    'BACKGROUND': (192, 192, 192),
    'HIDDEN': (128, 128, 128),
    'REVEALED': (160, 160, 160),
    'BORDER': (64, 64, 64),
    'FLAG': (255, 0, 0),
    'MINE': (0, 0, 0),
    'BUTTON': (100, 100, 100),
    'BUTTON_HOVER': (120, 120, 120),
    'BUTTON_ACTIVE': (80, 80, 80),
    'TEXT': (255, 255, 255),
    'INFO_BG': (200, 200, 200),
    'NUMBERS': {
        1: (0, 0, 255),      # Синий
        2: (0, 128, 0),      # Зеленый
        3: (255, 0, 0),      # Красный
        4: (0, 0, 128),      # Темно-синий
        5: (128, 0, 0),      # Темно-красный
        6: (0, 128, 128),    # Бирюзовый
        7: (0, 0, 0),        # Черный
        8: (128, 128, 128)   # Серый
    }
}
эта_папка = os.path.dirname(__file__)
путь_к_сох = os.path.join(эта_папка, "sonido-original-xatlasfb.mp3")
путь_к_со = os.path.join(эта_папка, "sonido-original.mp3")
путь_к_сох2 = os.path.join(эта_папка, "sonido-original-xatlasfb (2).mp3")
путь_к_сох4 = os.path.join(эта_папка, "sonido-original-xatlasfb (4).mp3")

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = COLORS['BUTTON']
        self.hover_color = COLORS['BUTTON_HOVER']
        self.active_color = COLORS['BUTTON_ACTIVE']
        self.is_hovered = False
        self.is_active = False
    
    def draw(self, screen):
        color = self.active_color if self.is_active else (self.hover_color if self.is_hovered else self.color)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLORS['BORDER'], self.rect, 2)
        
        text_surface = self.font.render(self.text, True, COLORS['TEXT'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                self.is_active = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_active = False
        return False

class Minesweeper:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = []
        self.revealed = []
        self.flags = []
        self.game_over = False
        self.won = False
        self.first_move = True
        
        # Инициализация массивов
        self.reset()
    
    def reset(self):
        # Сбрасывает игру
        self.board = []
        self.revealed = []
        self.flags = []
        self.game_over = False
        self.won = False
        self.first_move = True
        
        for i in range(self.height):
            self.board.append([0] * self.width)
            self.revealed.append([False] * self.width)
            self.flags.append([False] * self.width)
    
    def place_mines(self, first_x, first_y):
        # Размещает мины, гарантируя, что первая клетка не будет миной
        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Не размещаем мину на первой открытой клетке
            if (x == first_x and y == first_y):
                continue
                
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_placed += 1
        
        # Подсчет чисел вокруг мин
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    continue
                
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.board[ny][nx] == -1:
                                count += 1
                self.board[y][x] = count
    
    def reveal(self, x, y):
        # Открывает клетку
        if self.game_over or self.won:
            return False
        
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        
        # Нельзя открыть клетку с флажком
        if self.flags[y][x]:
            return False
        
        # Если уже открыта
        if self.revealed[y][x]:
            return False
        
        # Первый ход - размещаем мины
        if self.first_move:
            self.first_move = False
            self.place_mines(x, y)
        
        # Если наступили на мину
        if self.board[y][x] == -1:
            self.game_over = True
            self.reveal_all_mines()
            return False
        
        # Открываем клетку
        self.revealed[y][x] = True
        
        # Если пустая клетка, открываем соседние
        if self.board[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if not self.revealed[ny][nx] and not self.flags[ny][nx]:
                            self.reveal(nx, ny)
        
        # Проверка на победу
        self.check_win()
        return True
    
    def reveal_all_mines(self):
        # Открывает все мины при проигрыше
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    self.revealed[y][x] = True
    
    def toggle_flag(self, x, y):
        # Устанавливает/снимает флажок
        if self.game_over or self.won:
            return
        
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        
        # Нельзя ставить флажок на открытую клетку
        if self.revealed[y][x]:
            return
        
        self.flags[y][x] = not self.flags[y][x]
        self.check_win()
    
    def check_win(self):
        # Проверяет, выиграл ли игрок
        flagged_mines = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1 and self.flags[y][x]:
                    flagged_mines += 1
        
        if flagged_mines == self.mines:
            self.won = True
            self.game_over = True
            return True
        return False

class Game:
    def __init__(self):
        self.current_difficulty = "Любитель"
        self.scroll_y = 0  # Прокрутка по вертикали
        self.dragging = False
        self.drag_start_y = 0
        self.scroll_start = 0
        
        # Рассчитываем размер окна (фиксированный, но достаточно большой)
        self.window_width = 900
        self.window_height = 700
        
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Сапёр")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Инициализация игры
        self.init_game()
        self.create_buttons()
    
    def init_game(self):
        # Инициализирует игровое поле
        settings = DIFFICULTY_LEVELS[self.current_difficulty]
        self.game = Minesweeper(settings["width"], settings["height"], settings["mines"])
        
        # Рассчитываем размер игрового поля
        self.board_width = self.game.width * (TILE_SIZE + MARGIN) + MARGIN
        self.board_height = self.game.height * (TILE_SIZE + MARGIN) + MARGIN
        
        # Центрируем поле по горизонтали
        self.board_offset_x = (self.window_width - self.board_width) // 2
        
        # Область для прокрутки
        self.scroll_area = pygame.Rect(0, 0, self.window_width, self.window_height - INFO_PANEL_HEIGHT)
    
    def create_buttons(self):
        # Создает кнопки интерфейса
        self.buttons = []
        
        # Кнопка "Новая игра"
        new_game_btn = Button(
            self.window_width // 2 - 60,
            self.window_height - INFO_PANEL_HEIGHT + 10,
            120,
            40,
            "Новая игра",
            self.small_font
        )
        self.buttons.append(("new_game", new_game_btn))
        
        # Кнопки выбора сложности
        btn_width = 100
        btn_height = 35
        total_buttons_width = len(DIFFICULTY_LEVELS) * (btn_width + 10) - 10
        start_x = (self.window_width - total_buttons_width) // 2
        y_pos = self.window_height - INFO_PANEL_HEIGHT + 60
        
        for i, (level_name, settings) in enumerate(DIFFICULTY_LEVELS.items()):
            btn = Button(
                start_x + i * (btn_width + 10),
                y_pos,
                btn_width,
                btn_height,
                level_name,
                self.small_font
            )
            if level_name == self.current_difficulty:
                btn.is_active = True
            self.buttons.append((level_name, btn))
    
    def change_difficulty(self, level_name):
        # Изменяет сложность игры
        global путь_к_сох
        if level_name != self.current_difficulty:
            self.current_difficulty = level_name
            self.init_game()
        if level_name == DIFFICULTY_LEVELS.get("Любитель"):
            pygame.mixer.music.load(путь_к_сох)
            pygame.mixer.music.play(loops=-1)
            
            # Обновляем активное состояние кнопок
            for btn_id, btn in self.buttons:
                if btn_id in DIFFICULTY_LEVELS:
                    btn.is_active = (btn_id == level_name)
            
            self.scroll_y = 0  # Сбрасываем прокрутку
    
    def draw_board(self):
        # Отрисовывает игровое поле с учетом прокрутки
        for y in range(self.game.height):
            for x in range(self.game.width):
                rect_x = self.board_offset_x + x * (TILE_SIZE + MARGIN) + MARGIN
                rect_y = y * (TILE_SIZE + MARGIN) + MARGIN - self.scroll_y
                
                # Проверяем, видима ли клетка
                if rect_y + TILE_SIZE < 0 or rect_y > self.scroll_area.height:
                    continue
                
                rect = pygame.Rect(rect_x, rect_y, TILE_SIZE, TILE_SIZE)
                
                if self.game.revealed[y][x]:
                    # Открытая клетка
                    pygame.draw.rect(self.screen, COLORS['REVEALED'], rect)
                    pygame.draw.rect(self.screen, COLORS['BORDER'], rect, 1)
                    
                    if self.game.board[y][x] > 0:
                        # Рисуем число
                        text = self.small_font.render(str(self.game.board[y][x]), True, 
                                                     COLORS['NUMBERS'][self.game.board[y][x]])
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
                    elif self.game.board[y][x] == -1:
                        # Рисуем мину
                        pygame.draw.circle(self.screen, COLORS['MINE'], rect.center, TILE_SIZE // 3)
                else:
                    # Закрытая клетка
                    pygame.draw.rect(self.screen, COLORS['HIDDEN'], rect)
                    pygame.draw.rect(self.screen, COLORS['BORDER'], rect, 1)
                    
                    if self.game.flags[y][x]:
                        # Рисуем флажок
                        flag_points = [
                            (rect_x + 5, rect_y + 5),
                            (rect_x + TILE_SIZE - 10, rect_y + TILE_SIZE // 2),
                            (rect_x + 5, rect_y + TILE_SIZE - 5)
                        ]
                        pygame.draw.polygon(self.screen, COLORS['FLAG'], flag_points)
    
    def draw_info_panel(self):
        # Отрисовывает информационную панель внизу экрана
        panel_rect = pygame.Rect(0, self.window_height - INFO_PANEL_HEIGHT, 
                                 self.window_width, INFO_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, COLORS['INFO_BG'], panel_rect)
        pygame.draw.line(self.screen, COLORS['BORDER'], 
                        (0, self.window_height - INFO_PANEL_HEIGHT),
                        (self.window_width, self.window_height - INFO_PANEL_HEIGHT), 3)
        
        # Отображаем количество мин
        mines_text = self.font.render(f"Мины: {self.game.mines}", True, COLORS['BORDER'])
        self.screen.blit(mines_text, (20, self.window_height - INFO_PANEL_HEIGHT + 10))
        
        # Отображаем количество флажков
        flags_used = sum(sum(row) for row in self.game.flags)
        flags_text = self.font.render(f"Флажки: {flags_used}", True, COLORS['BORDER'])
        self.screen.blit(flags_text, (self.window_width - 150, self.window_height - INFO_PANEL_HEIGHT + 10))
        
        # Отображаем статус игры
        if self.game.game_over:
            if self.game.won:
                status = "ПОБЕДА!"
                color = (0, 255, 0)
            else:
                status = "ПРОИГРЫШ!"
                color = (255, 0, 0)
            status_text = self.font.render(status, True, color)
            text_rect = status_text.get_rect(center=(self.window_width // 2, self.window_height - INFO_PANEL_HEIGHT + 30))
            self.screen.blit(status_text, text_rect)
        
        # Рисуем полосу прокрутки, если нужно
        if self.board_height > self.scroll_area.height:
            scroll_bar_height = self.scroll_area.height
            scroll_thumb_height = max(50, (self.scroll_area.height / self.board_height) * self.scroll_area.height)
            scroll_thumb_y = (self.scroll_y / (self.board_height - self.scroll_area.height)) * (scroll_bar_height - scroll_thumb_height)
            
            scroll_bar_rect = pygame.Rect(self.window_width - 15, 0, 10, scroll_bar_height)
            scroll_thumb_rect = pygame.Rect(self.window_width - 15, scroll_thumb_y, 10, scroll_thumb_height)
            
            pygame.draw.rect(self.screen, COLORS['BORDER'], scroll_bar_rect, 1)
            pygame.draw.rect(self.screen, COLORS['BUTTON'], scroll_thumb_rect)
    
    def handle_click(self, pos):
        # Обрабатывает клики по игровому полю
        # Проверяем, что клик в области игрового поля
        if pos[1] > self.scroll_area.height:
            return None
        
        # Вычисление координат клетки с учетом прокрутки
        x = (pos[0] - self.board_offset_x - MARGIN) // (TILE_SIZE + MARGIN)
        y = (pos[1] + self.scroll_y - MARGIN) // (TILE_SIZE + MARGIN)
        
        if 0 <= x < self.game.width and 0 <= y < self.game.height:
            return (x, y)
        return None
    
    def run(self):
        # Главный игровой цикл
        running = True
        
        while running:
            self.screen.fill(COLORS['BACKGROUND'])
            
            # Отрисовка игрового поля
            self.draw_board()
            
            # Отрисовка информационной панели
            self.draw_info_panel()
            
            # Отрисовка кнопок
            for btn_id, btn in self.buttons:
                btn.draw(self.screen)
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Прокрутка колесиком мыши
                if event.type == pygame.MOUSEWHEEL:
                    if self.board_height > self.scroll_area.height:
                        self.scroll_y -= event.y * 30
                        # Ограничиваем прокрутку
                        max_scroll = max(0, self.board_height - self.scroll_area.height)
                        self.scroll_y = max(0, min(self.scroll_y, max_scroll))
                
                # Обработка перетаскивания для прокрутки
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and event.pos[1] <= self.scroll_area.height:
                        # Проверяем, не нажата ли кнопка
                        is_over_button = any(btn.rect.collidepoint(event.pos) for _, btn in self.buttons)
                        if not is_over_button:
                            self.dragging = True
                            self.drag_start_y = event.pos[1]
                            self.scroll_start = self.scroll_y
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                
                if event.type == pygame.MOUSEMOTION and self.dragging:
                    delta_y = event.pos[1] - self.drag_start_y
                    self.scroll_y = self.scroll_start - delta_y
                    max_scroll = max(0, self.board_height - self.scroll_area.height)
                    self.scroll_y = max(0, min(self.scroll_y, max_scroll))
                
                # Обработка кнопок
                for btn_id, btn in self.buttons:
                    if btn.handle_event(event):
                        if btn_id == "new_game":
                            self.game.reset()
                        elif btn_id in DIFFICULTY_LEVELS:
                            self.change_difficulty(btn_id)
                
                # Обработка кликов по игровому полю
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Проверяем, что клик не по кнопкам
                    is_over_button = any(btn.rect.collidepoint(event.pos) for _, btn in self.buttons)
                    
                    if not is_over_button and event.pos[1] <= self.scroll_area.height:
                        cell = self.handle_click(event.pos)
                        if cell:
                            x, y = cell
                            if event.button == 1:  # Левая кнопка - открыть
                                self.game.reveal(x, y)
                            elif event.button == 3:  # Правая кнопка - флажок
                                self.game.toggle_flag(x, y)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()