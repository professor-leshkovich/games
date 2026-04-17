import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Базовые константы
BASE_WIDTH = 800
BASE_HEIGHT = 600
CELL_SIZE = 20
FPS = 10

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
GRAY = (128, 128, 128)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 150, 255)
YELLOW = (255, 255, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Варианты размеров поля
FIELD_SIZES = {
    "Маленькое": (600, 400),
    "Среднее": (800, 600),
    "Большое": (1000, 800),
    "Огромное": (1200, 900)
}

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class Snake:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        # Начальная позиция змейки
        self.body = [
            [window_width // 2, window_height // 2],
            [window_width // 2 - CELL_SIZE, window_height // 2],
            [window_width // 2 - 2 * CELL_SIZE, window_height // 2]
        ]
        self.direction = RIGHT
        self.grow = False
        
    def move(self):
        head = self.body[0].copy()
        
        # Перемещаем голову
        head[0] += self.direction[0] * CELL_SIZE
        head[1] += self.direction[1] * CELL_SIZE
        
        # Вставляем новую голову
        self.body.insert(0, head)
        
        # Удаляем хвост если не нужно расти
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
    def change_direction(self, new_direction):
        # Запрещаем разворот на 180 градусов
        if (new_direction[0] != -self.direction[0] and 
            new_direction[1] != -self.direction[1]):
            self.direction = new_direction
            
    def check_collision(self):
        head = self.body[0]
        
        # Проверка столкновения со стенами
        if (head[0] < 0 or head[0] >= self.window_width or
            head[1] < 0 or head[1] >= self.window_height):
            return True
            
        # Проверка столкновения с собственным телом
        for segment in self.body[1:]:
            if head[0] == segment[0] and head[1] == segment[1]:
                return True
                
        return False
        
    def draw(self, screen):
        for i, segment in enumerate(self.body):
            # Голова немного светлее
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, 
                           (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            # Контур сегментов
            pygame.draw.rect(screen, BLACK, 
                           (segment[0], segment[1], CELL_SIZE, CELL_SIZE), 1)

class Food:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.position = [0, 0]
        self.spawn()
        
    def spawn(self):
        # Создаем еду в случайной позиции
        self.position[0] = random.randrange(0, self.window_width, CELL_SIZE)
        self.position[1] = random.randrange(0, self.window_height, CELL_SIZE)
        
    def draw(self, screen):
        # Рисуем еду как яблоко
        center = (self.position[0] + CELL_SIZE // 2, self.position[1] + CELL_SIZE // 2)
        pygame.draw.circle(screen, RED, center, CELL_SIZE // 2 - 2)
        pygame.draw.circle(screen, BLACK, center, CELL_SIZE // 2 - 2, 1)
        # Листик
        leaf_pos = (center[0], center[1] - CELL_SIZE // 2 + 2)
        pygame.draw.circle(screen, DARK_GREEN, leaf_pos, 4)

class Game:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        self.reset_game()
        
    def reset_game(self):
        self.snake = Snake(self.window_width, self.window_height)
        self.food = Food(self.window_width, self.window_height)
        self.score = 0
        self.game_over = False
        self.paused = False
        self.won = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            if event.type == pygame.KEYDOWN:
                if self.game_over or self.won:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"
                        
        return "continue"
        
    def update(self):
        if self.game_over or self.paused or self.won:
            return
            
        self.snake.move()
        
        # Проверка съедания еды
        if (self.snake.body[0][0] == self.food.position[0] and 
            self.snake.body[0][1] == self.food.position[1]):
            self.snake.grow = True
            self.score += 10
            self.food.spawn()
            
            # Проверяем, не появилась ли еда на змейке
            while self.food.position in self.snake.body:
                self.food.spawn()
                
            # Проверка на победу (змейка заполнила все поле)
            if len(self.snake.body) >= (self.window_width // CELL_SIZE) * (self.window_height // CELL_SIZE):
                self.won = True
        
        # Проверка столкновений
        if self.snake.check_collision():
            self.game_over = True
            
    def draw_grid(self):
        for x in range(0, self.window_width, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.window_height), 1)
        for y in range(0, self.window_height, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.window_width, y), 1)
            
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Отображение счета и размера поля
        score_text = self.font.render(f"Счет: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        size_text = self.small_font.render(f"Поле: {self.window_width}x{self.window_height}", True, WHITE)
        self.screen.blit(size_text, (10, 50))
        
        # Сообщения о состоянии игры
        if self.paused and not self.game_over and not self.won:
            pause_text = self.large_font.render("ПАУЗА", True, YELLOW)
            text_rect = pause_text.get_rect(center=(self.window_width//2, self.window_height//2))
            self.screen.blit(pause_text, text_rect)
            
            continue_text = self.small_font.render("Нажмите P для продолжения", True, WHITE)
            continue_rect = continue_text.get_rect(center=(self.window_width//2, self.window_height//2 + 50))
            self.screen.blit(continue_text, continue_rect)
            
        if self.game_over:
            # Затемнение экрана
            overlay = pygame.Surface((self.window_width, self.window_height))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.large_font.render("ИГРА ОКОНЧЕНА!", True, RED)
            text_rect = game_over_text.get_rect(center=(self.window_width//2, self.window_height//2 - 40))
            self.screen.blit(game_over_text, text_rect)
            
            final_score_text = self.font.render(f"Финальный счет: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(self.window_width//2, self.window_height//2))
            self.screen.blit(final_score_text, score_rect)
            
            restart_text = self.small_font.render("ПРОБЕЛ - новая игра | ESC - меню", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.window_width//2, self.window_height//2 + 50))
            self.screen.blit(restart_text, restart_rect)
            
        if self.won:
            # Затемнение экрана
            overlay = pygame.Surface((self.window_width, self.window_height))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            win_text = self.large_font.render("ПОБЕДА!", True, YELLOW)
            text_rect = win_text.get_rect(center=(self.window_width//2, self.window_height//2 - 40))
            self.screen.blit(win_text, text_rect)
            
            final_score_text = self.font.render(f"Ваш счет: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(self.window_width//2, self.window_height//2))
            self.screen.blit(final_score_text, score_rect)
            
            restart_text = self.small_font.render("ПРОБЕЛ - новая игра | ESC - меню", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.window_width//2, self.window_height//2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            action = self.handle_events()
            if action == "quit":
                return "quit"
            elif action == "menu":
                return "menu"
                
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        return "quit"

class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
        pygame.display.set_caption("Змейка - Главное меню")
        self.clock = pygame.time.Clock()
        
        # Шрифты
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 42)
        self.info_font = pygame.font.Font(None, 24)
        
        # Создаем кнопки выбора размера
        button_width = 200
        button_height = 50
        start_y = 250
        spacing = 70
        
        self.size_buttons = {}
        for i, (size_name, size) in enumerate(FIELD_SIZES.items()):
            x = BASE_WIDTH // 2 - button_width // 2
            y = start_y + i * spacing
            self.size_buttons[size_name] = Button(
                x, y, button_width, button_height,
                f"{size_name} ({size[0]}x{size[1]})",
                BLUE, LIGHT_BLUE
            )
            
        # Кнопка выхода
        self.quit_button = Button(
            BASE_WIDTH // 2 - 100, BASE_HEIGHT - 80,
            200, 50, "Выход", RED, (255, 100, 100)
        )
        
        self.selected_size = None
        
    def draw(self):
        self.screen.fill(BLACK)
        
        # Заголовок
        title_text = self.title_font.render("ЗМЕЙКА", True, GREEN)
        title_rect = title_text.get_rect(center=(BASE_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Подзаголовок
        subtitle_text = self.button_font.render("Выберите размер поля:", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(BASE_WIDTH // 2, 180))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Рисуем кнопки
        mouse_pos = pygame.mouse.get_pos()
        for button in self.size_buttons.values():
            button.check_hover(mouse_pos)
            button.draw(self.screen, self.button_font)
            
        self.quit_button.check_hover(mouse_pos)
        self.quit_button.draw(self.screen, self.button_font)
        
        # Инструкция
        info_text = self.info_font.render("Управление: стрелки | P - пауза | ESC - меню", True, GRAY)
        info_rect = info_text.get_rect(center=(BASE_WIDTH // 2, BASE_HEIGHT - 30))
        self.screen.blit(info_text, info_rect)
        
        pygame.display.flip()
        
    def run(self):
        while True:
            mouse_click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click = True
                        
            mouse_pos = pygame.mouse.get_pos()
            
            # Проверяем нажатия на кнопки
            for size_name, button in self.size_buttons.items():
                if button.is_clicked(mouse_pos, mouse_click):
                    return "start_game", FIELD_SIZES[size_name]
                    
            if self.quit_button.is_clicked(mouse_pos, mouse_click):
                return "quit", None
                
            self.draw()
            self.clock.tick(FPS)

def main():
    while True:
        # Показываем главное меню
        menu = MainMenu()
        action, field_size = menu.run()
        
        if action == "quit":
            break
        elif action == "start_game" and field_size:
            # Запускаем игру с выбранным размером поля
            game = Game(field_size[0], field_size[1])
            pygame.display.set_caption(f"Змейка - Поле {field_size[0]}x{field_size[1]}")
            game_result = game.run()
            
            if game_result == "quit":
                break
            # Если вернулись в меню, продолжаем цикл
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()