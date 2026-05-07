# Counter-Strike 2.5D - Улучшенная версия с случайной генерацией карт
# Особенности:
# 1. Случайная генерация карт
# 2. Боты-террористы
# 3. Разное оружие
# 4. Покупка оружия
# 5. Бомба и её установка
# 6. Зоны для команд

import pygame
import sys
import math
import random
from enum import Enum

# Инициализация
pygame.init()
pygame.mixer.init()
pygame.font.init()  # Добавляем инициализацию шрифтов

WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 120

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
DARK_GRAY = (50, 50, 50)
DARK_BROWN = (101, 67, 33)
STEEL = (192, 192, 192)
LIGHT_BROWN = (210, 180, 140)
DARK_GREEN = (0, 100, 0)

class WeaponType(Enum):
    KNIFE = 1
    PISTOL = 2
    SHOTGUN = 3
    RIFLE = 4
    SNIPER = 5

class Weapon:
    def __init__(self, weapon_type, name, damage, range_dist, fire_rate, ammo, price, color, size):
        self.type = weapon_type
        self.name = name
        self.damage = damage
        self.range = range_dist
        self.fire_rate = fire_rate
        self.ammo = ammo
        self.max_ammo = ammo
        self.price = price
        self.last_shot = 0
        self.color = color
        self.size = size  # (width, height)
        
    def draw(self, surface, x, y, scale=1.0):
        # 2д моделька оружия
        width, height = self.size
        width = int(width * scale)
        height = int(height * scale)
        
        if self.type == WeaponType.KNIFE:
            # Нож - увеличенная моделька
            # Лезвие
            pygame.draw.polygon(surface, STEEL, [
                (x, y + height//2),
                (x + width//2, y),
                (x + width, y + height//2),
                (x + width//2, y + height)
            ])
            # Рукоятка
            pygame.draw.rect(surface, DARK_BROWN, 
                           (x + width//2 - 3, y + height//2 - 3, 6, height//2 + 3))
            
        elif self.type == WeaponType.PISTOL:
            # глок - светло-коричневый
            # Основа
            pygame.draw.rect(surface, LIGHT_BROWN, (x, y + height//3, width, height//3))
            # Ствол
            pygame.draw.rect(surface, (150, 120, 90), (x + width, y + height//3 - 2, width//3, height//3 + 4))
            # Рукоятка
            pygame.draw.rect(surface, (120, 90, 60), (x - width//6, y + height//3, width//3, height*2//3))
            # Курок
            pygame.draw.circle(surface, (90, 90, 90), (x + width//4, y + height//3), 3)
            # Спусковой крючок
            pygame.draw.rect(surface, (60, 60, 60), (x - width//8, y + height*2//3, width//4, 2))
            
        elif self.type == WeaponType.SHOTGUN:
            # Дробовик - черный
            # Ствол (толстый)
            pygame.draw.rect(surface, BLACK, (x, y, width, height))
            # Затвор
            pygame.draw.rect(surface, (40, 40, 40), (x - width//4, y, width//4, height))
            # Рукоятка
            pygame.draw.rect(surface, (30, 30, 30), (x - width//3, y + height, width//3, height))
            # Приклад
            pygame.draw.rect(surface, (20, 20, 20), (x - width//2, y + height, width//4, height*2))
            # Цевье
            pygame.draw.rect(surface, (50, 50, 50), (x + width//2, y, width//3, height))
            
        elif self.type == WeaponType.RIFLE:
            # калаш
            # Ствол
            pygame.draw.rect(surface, (60, 40, 20), (x, y + height//3, width, height//3))
            # Магазин
            pygame.draw.rect(surface, STEEL, (x + width//3, y + height//2, width//4, height))
            # Приклад
            pygame.draw.rect(surface, DARK_BROWN, (x - width//3, y, width//3, height))
            # Цевье
            pygame.draw.rect(surface, BROWN, (x + width//2, y + height//3, width//3, height//3))
            # Рукоятка
            pygame.draw.rect(surface, (40, 40, 40), (x + width*2//3, y + height, width//6, height//2))
            # Прицел
            pygame.draw.rect(surface, (80, 80, 80), (x + width//4, y, width//8, height//4))
            
        elif self.type == WeaponType.SNIPER:
            # авик - зеленый
            # Ствол (очень длинный)
            pygame.draw.rect(surface, DARK_GREEN, (x, y + height//3, width, height//3))
            # Прицел
            pygame.draw.rect(surface, BLACK, (x + width//2, y, width//6, height//3))
            pygame.draw.circle(surface, RED, (x + width//2 + width//12, y + height//6), 3)
            # Приклад
            pygame.draw.rect(surface, (0, 80, 0), (x - width//3, y, width//3, height))
            # Сошки
            pygame.draw.line(surface, STEEL, (x + width, y + height*2//3), 
                           (x + width + width//6, y + height), 2)
            pygame.draw.line(surface, STEEL, (x + width, y + height//3), 
                           (x + width + width//6, y), 2)
            # Затвор
            pygame.draw.rect(surface, (0, 120, 0), (x - width//4, y + height//3, width//4, height//3))

WEAPONS = {
    WeaponType.KNIFE: Weapon(WeaponType.KNIFE, "Knife", 25, 1, 500, 1, 0, DARK_GRAY, (25, 10)),
    WeaponType.PISTOL: Weapon(WeaponType.PISTOL, "Glock-18", 15, 15, 300, 20, 300, LIGHT_BROWN, (30, 15)),
    WeaponType.SHOTGUN: Weapon(WeaponType.SHOTGUN, "XM1014", 40, 8, 1000, 8, 1200, BLACK, (40, 20)),
    WeaponType.RIFLE: Weapon(WeaponType.RIFLE, "AK-47", 25, 25, 150, 30, 2700, (60, 40, 20), (50, 15)),
    WeaponType.SNIPER: Weapon(WeaponType.SNIPER, "AWP", 100, 40, 1500, 10, 4750, DARK_GREEN, (60, 15))
}

class Team(Enum):
    CT = 1  # Контр-террористы
    T = 2   # Террористы

class Difficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3

class Player:
    def __init__(self, x, y, team, name="Player"):
        self.x = x
        self.y = y
        self.team = team
        self.name = name
        self.health = 100
        self.armor = 0
        self.money = 800
        self.current_weapon = WEAPONS[WeaponType.PISTOL]
        self.weapons = [WEAPONS[WeaponType.KNIFE], self.current_weapon]
        self.kills = 0
        self.deaths = 0
        self.angle = 0
        self.speed = 0.05
        self.normal_speed = 0.05
        self.crouch_speed = 0.02
        self.is_crouching = False
        self.has_bomb = (team == Team.T)  # Только террористы могут нести бомбу
        self.planting_bomb = False
        self.plant_time = 0
        self.is_bot = False
        self.last_killer = None  # Кто последний убил игрока
        self.last_killer_weapon = None  # Каким оружием убили
        
    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Проверка столкновений со стенами
        if not game_map.is_wall(int(new_x), int(new_y)):
            self.x = new_x
            self.y = new_y
            
    def take_damage(self, damage, attacker=None, weapon=None):
        if self.armor > 0:
            damage = int(damage * 0.66)
            self.armor -= damage // 2
            if self.armor < 0:
                self.armor = 0
                
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            if attacker:
                self.last_killer = attacker.name
                self.last_killer_weapon = weapon.name if weapon else "Unknown"
            return True
        return False
        
    def shoot(self, game):
        current_time = pygame.time.get_ticks()
        if (self.current_weapon.ammo > 0 and 
            current_time - self.current_weapon.last_shot > self.current_weapon.fire_rate):
            
            self.current_weapon.ammo -= 1
            self.current_weapon.last_shot = current_time
            
            # Расчет направления выстрела
            end_x = self.x + math.cos(self.angle) * self.current_weapon.range
            end_y = self.y + math.sin(self.angle) * self.current_weapon.range
            
            # Проверка попадания
            hit_enemy = False
            for enemy in game.enemies:
                if enemy.team != self.team and enemy.health > 0:
                    # Простая проверка дистанции и направления
                    dx = enemy.x - self.x
                    dy = enemy.y - self.y
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance < self.current_weapon.range:
                        angle_to_enemy = math.atan2(dy, dx)
                        angle_diff = abs(self.angle - angle_to_enemy)
                        
                        if angle_diff < 0.3:  # ~17 градусов
                            # Проверка, нет ли стены между
                            if not game.map.check_wall_between(self.x, self.y, enemy.x, enemy.y):
                                killed = enemy.take_damage(self.current_weapon.damage, self, self.current_weapon)
                                if killed:
                                    self.kills += 1
                                    self.money += 300
                                    if self.team == Team.CT:
                                        game.ct_kills += 1
                                    else:
                                        game.t_kills += 1
                                    # Добавляем в киллфид
                                    game.add_killfeed(f"{self.name} killed {enemy.name} with {self.current_weapon.name}")
                                hit_enemy = True
                                
            # Эффект отдачи при выстреле
            if hit_enemy:
                # Дополнительные деньги за попадание
                self.money += 50
            return hit_enemy
        return False
        
    def buy_weapon(self, weapon_type):
        weapon = WEAPONS[weapon_type]
        if self.money >= weapon.price:
            self.money -= weapon.price
            # Создаем новую копию оружия, чтобы у каждого игрока был свой экземпляр
            new_weapon = Weapon(
                weapon.type, weapon.name, weapon.damage, weapon.range,
                weapon.fire_rate, weapon.ammo, weapon.price,
                weapon.color, weapon.size
            )
            self.weapons.append(new_weapon)
            self.current_weapon = new_weapon
            return True
        return False
        
    def switch_weapon(self, index):
        if 0 <= index < len(self.weapons):
            self.current_weapon = self.weapons[index]
            
    def reload(self):
        if hasattr(self.current_weapon, 'max_ammo'):
            needed = self.current_weapon.max_ammo - self.current_weapon.ammo
            # В реальной игре была бы система магазинов
            self.current_weapon.ammo = self.current_weapon.max_ammo
            
    def start_planting_bomb(self, game):
        if (self.team == Team.T and self.has_bomb and 
            game.map.is_bomb_site(int(self.x), int(self.y)) and
            not game.bomb_planted):
            self.planting_bomb = True
            self.plant_time = pygame.time.get_ticks()
            
    def update_planting(self, game):
        if self.planting_bomb:
            current_time = pygame.time.get_ticks()
            if current_time - self.plant_time > 3000:  # 3 секунды на установку
                game.plant_bomb(self.x, self.y)
                self.has_bomb = False
                self.planting_bomb = False
                return True
        return False
        
    def crouch(self):
        # Присесть/встать
        self.is_crouching = not self.is_crouching
        if self.is_crouching:
            self.speed = self.crouch_speed
        else:
            self.speed = self.normal_speed
            
    def draw(self, surface, is_main_player=True):
        # Рисуем игрока
        color = BLUE if self.team == Team.CT else RED
        screen_x = int(self.x * 20) if is_main_player else int(self.x * 20)
        screen_y = int(self.y * 20) if is_main_player else int(self.y * 20)
        
        # Если игрок присел, рисуем его ниже и меньше
        player_radius = 6 if self.is_crouching else 8
        player_y_offset = 2 if self.is_crouching else 0
        
        pygame.draw.circle(surface, color, (screen_x, screen_y + player_y_offset), player_radius)
        
        # Линия направления взгляда
        line_length = 10 if self.is_crouching else 15
        end_x = screen_x + math.cos(self.angle) * line_length
        end_y = screen_y + player_y_offset + math.sin(self.angle) * line_length
        pygame.draw.line(surface, WHITE, (screen_x, screen_y + player_y_offset), (end_x, end_y), 2)
        
        # Бомба над головой
        if self.has_bomb:
            bomb_y = screen_y + player_y_offset - 12 if self.is_crouching else screen_y - 15
            pygame.draw.circle(surface, YELLOW, (screen_x, bomb_y), 5)
            
        # Оружие в руках (для ботов)
        if self.is_bot and hasattr(self, 'current_weapon'):
            # Рисуем оружие рядом с ботом (увеличенное)
            weapon_x = screen_x + 15
            weapon_y = screen_y + 10
            self.current_weapon.draw(surface, weapon_x, weapon_y, scale=0.8)
            
        # Имя игрока
        if not is_main_player or self.is_bot:
            name_font = pygame.font.Font(None, 20)
            name_text = name_font.render(self.name, True, WHITE)
            name_rect = name_text.get_rect(center=(screen_x, screen_y - 20))
            surface.blit(name_text, name_rect)

class Bot(Player):
    def __init__(self, x, y, team, difficulty=Difficulty.EASY, bot_number=1):
        bot_name = f"BOT_{bot_number}"
        super().__init__(x, y, team, bot_name)
        self.is_bot = True
        self.ai_state = "patrol"  # patrol, chase, attack, flee
        self.target_x = x
        self.target_y = y
        self.last_decision = 0
        self.patrol_points = []
        self.last_shot_time = 0
        self.difficulty = difficulty
        self.bot_number = bot_number
        
        # Настройки в зависимости от сложности
        if difficulty == Difficulty.EASY:
            self.armor = 0
            self.accuracy = 0.5
            self.reaction_time = 800
            self.detection_range = 8
            self.crouch_chance = 0.1  # 10% шанс присесть
        elif difficulty == Difficulty.NORMAL:
            self.armor = 100
            self.accuracy = 0.7
            self.reaction_time = 500
            self.detection_range = 10
            self.crouch_chance = 0.2  # 20% шанс присесть
        else:  # HARD
            self.armor = 200
            self.accuracy = 0.9
            self.reaction_time = 300
            self.detection_range = 12
            self.crouch_chance = 0.3  # 30% шанс присесть
            
        # Случайное оружие из доступных в магазине
        self.assign_random_weapon()
        
    def assign_random_weapon(self):
        # Назначает боту случайное оружие из доступных в магазине
        available_weapons = [
            WeaponType.PISTOL,
            WeaponType.SHOTGUN,
            WeaponType.RIFLE,
            WeaponType.SNIPER
        ]
        
        # В зависимости от сложности, разный шанс получить лучшее оружие
        if self.difficulty == Difficulty.EASY:
            weights = [0.4, 0.3, 0.2, 0.1]  # Чаще пистолеты
        elif self.difficulty == Difficulty.NORMAL:
            weights = [0.2, 0.3, 0.3, 0.2]  # Более сбалансированно
        else:  # HARD
            weights = [0.1, 0.2, 0.4, 0.3]  # Чаще винтовки и снайперки
            
        weapon_type = random.choices(available_weapons, weights=weights)[0]
        # Создаем новую копию оружия для бота
        weapon_template = WEAPONS[weapon_type]
        self.current_weapon = Weapon(
            weapon_template.type, weapon_template.name, weapon_template.damage,
            weapon_template.range, weapon_template.fire_rate, weapon_template.ammo,
            weapon_template.price, weapon_template.color, weapon_template.size
        )
        self.weapons = [WEAPONS[WeaponType.KNIFE], self.current_weapon]
        
    def update(self, game):
        current_time = pygame.time.get_ticks()
        
        # Боты могут случайно присесть в зависимости от сложности
        if random.random() < self.crouch_chance and current_time - self.last_decision > 2000:
            self.crouch()
        
        # Принимаем решение в зависимости от сложности
        if current_time - self.last_decision > self.reaction_time:
            self.last_decision = current_time
            
            # Ищем ближайшего врага (игрока)
            nearest_enemy = game.player if game.player.team != self.team and game.player.health > 0 else None
            min_distance = float('inf')
            
            if nearest_enemy:
                dx = game.player.x - self.x
                dy = game.player.y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Если игрок присел, его сложнее заметить
                detection_modifier = 1.0
                if game.player.is_crouching:
                    detection_modifier = 0.6  # На 40% сложнее заметить присевшего игрока
                    
                if distance < self.detection_range * detection_modifier:
                    min_distance = distance
                else:
                    nearest_enemy = None
                        
            if nearest_enemy:
                # Дальний бой для снайперов
                if self.current_weapon.type == WeaponType.SNIPER:
                    # Снайперы стараются держать дистанцию
                    if min_distance < 8:
                        self.ai_state = "flee"
                        # Отступаем от врага
                        self.target_x = self.x - (nearest_enemy.x - self.x) / min_distance * 5
                        self.target_y = self.y - (nearest_enemy.y - self.y) / min_distance * 5
                    elif min_distance < 25:
                        self.ai_state = "attack"
                        self.target_x = nearest_enemy.x
                        self.target_y = nearest_enemy.y
                        
                        # Стрелять с большей дистанции
                        if current_time - self.last_shot_time > self.current_weapon.fire_rate:
                            self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)
                            if self.shoot_at_player(game, nearest_enemy):
                                self.last_shot_time = current_time
                
                # Обычное поведение для другого оружия
                elif min_distance < 3:  # Ближний бой
                    self.ai_state = "attack"
                    self.target_x = nearest_enemy.x
                    self.target_y = nearest_enemy.y
                    
                    # Стрелять
                    if current_time - self.last_shot_time > self.current_weapon.fire_rate:
                        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)
                        if self.shoot_at_player(game, nearest_enemy):
                            self.last_shot_time = current_time
                elif min_distance < self.detection_range:  # Преследовать
                    self.ai_state = "chase"
                    self.target_x = nearest_enemy.x
                    self.target_y = nearest_enemy.y
                else:
                    self.ai_state = "patrol"
            else:
                # Патрулирование
                if self.ai_state == "patrol":
                    if not self.patrol_points:
                        # Генерируем случайные точки патрулирования
                        for _ in range(3):
                            px = random.randint(1, game.map.width - 2)
                            py = random.randint(1, game.map.height - 2)
                            self.patrol_points.append((px, py))
                    
                    # Достигли точки - берем следующую
                    dx = self.target_x - self.x
                    dy = self.target_y - self.y
                    if math.sqrt(dx*dx + dy*dy) < 1:
                        if self.patrol_points:
                            self.target_x, self.target_y = self.patrol_points.pop(0)
                            self.patrol_points.append((self.target_x, self.target_y))
                else:
                    self.ai_state = "patrol"
                    # Сброс цели патрулирования
                    if not self.patrol_points:
                        self.target_x = random.randint(1, game.map.width - 2)
                        self.target_y = random.randint(1, game.map.height - 2)
                    
        # Движение к цели
        if self.ai_state in ["chase", "patrol", "flee"]:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0.5:
                self.angle = math.atan2(dy, dx)
                move_x = math.cos(self.angle) * self.speed
                move_y = math.sin(self.angle) * self.speed
                
                # Если отступаем, двигаемся в противоположном направлении
                if self.ai_state == "flee":
                    move_x = -move_x
                    move_y = -move_y
                    
                self.move(move_x, move_y, game.map)
    
    def shoot_at_player(self, game, target):
        # Бот стреляет в цель с учетом сложности
        if self.current_weapon.ammo > 0:
            self.current_weapon.ammo -= 1
            
            # Проверка попадания
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.current_weapon.range:
                # Проверка, нет ли стены между ботом и целью
                if not game.map.check_wall_between(self.x, self.y, target.x, target.y):
                    # Шанс попадания зависит от дистанции и сложности
                    base_chance = self.accuracy
                    distance_penalty = distance * 0.02  # 2% снижение за каждую единицу дистанции
                    hit_chance = max(0.1, base_chance - distance_penalty)
                    
                    # Если цель присела, снижаем шанс попадания
                    if hasattr(target, 'is_crouching') and target.is_crouching:
                        hit_chance *= 0.7  # На 30% сложнее попасть в присевшего
                    
                    if random.random() < hit_chance:
                        killed = target.take_damage(self.current_weapon.damage, self, self.current_weapon)
                        if killed and isinstance(target, Player):
                            target.deaths += 1
                            # Бот получает деньги за убийство
                            self.money += 300
                        return True
                        
            # Перезарядка при необходимости
            if self.current_weapon.ammo == 0:
                self.current_weapon.ammo = self.current_weapon.max_ammo
        return False

class MapGenerator:
    def __init__(self, width=40, height=30):
        self.width = width
        self.height = height
        self.grid = []
        self.ct_spawn = []
        self.t_spawn = []
        self.bomb_sites = []
        
    def generate_map(self):
        # Генерация случайной карты
        # Инициализация сетки
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Создаем основные комнаты
        rooms = []
        for _ in range(8):
            room_width = random.randint(5, 10)
            room_height = random.randint(5, 8)
            room_x = random.randint(1, self.width - room_width - 1)
            room_y = random.randint(1, self.height - room_height - 1)
            rooms.append((room_x, room_y, room_width, room_height))
            
            # Выкапываем комнату
            for y in range(room_y, room_y + room_height):
                for x in range(room_x, room_x + room_width):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.grid[y][x] = 0
                        
        # Соединяем комнаты коридорами
        for i in range(len(rooms) - 1):
            x1, y1, w1, h1 = rooms[i]
            x2, y2, w2, h2 = rooms[i + 1]
            
            center1_x = x1 + w1 // 2
            center1_y = y1 + h1 // 2
            center2_x = x2 + w2 // 2
            center2_y = y2 + h2 // 2
            
            # Горизонтальный коридор
            start_x = min(center1_x, center2_x)
            end_x = max(center1_x, center2_x)
            for x in range(start_x, end_x + 1):
                if 0 <= x < self.width and 0 <= center1_y < self.height:
                    self.grid[center1_y][x] = 0
                    
            # Вертикальный коридор
            start_y = min(center1_y, center2_y)
            end_y = max(center1_y, center2_y)
            for y in range(start_y, end_y + 1):
                if 0 <= center2_x < self.width and 0 <= y < self.height:
                    self.grid[y][center2_x] = 0
        
        # Добавляем случайные стены внутри комнат
        for _ in range(15):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            if self.grid[y][x] == 0:
                wall_type = random.choice(["pillar", "wall", "corner"])
                
                if wall_type == "pillar":
                    self.grid[y][x] = 1
                elif wall_type == "wall":
                    length = random.randint(2, 4)
                    direction = random.choice(["h", "v"])
                    for i in range(length):
                        if direction == "h" and x + i < self.width:
                            self.grid[y][x + i] = 1
                        elif direction == "v" and y + i < self.height:
                            self.grid[y + i][x] = 1
                            
        # Определяем зоны спавна
        # CT спавн - левая часть карты
        self.ct_spawn = []
        for y in range(self.height):
            for x in range(self.width // 4):
                if self.grid[y][x] == 0:
                    self.ct_spawn.append((x, y))
                    
        # T спавн - правая часть карты
        self.t_spawn = []
        for y in range(self.height):
            for x in range(self.width * 3 // 4, self.width):
                if self.grid[y][x] == 0:
                    self.t_spawn.append((x, y))
                    
        # Если списки спавнов пустые, добавляем хотя бы по одной точке
        if not self.ct_spawn:
            for y in range(1, 4):
                for x in range(1, 4):
                    if y < self.height and x < self.width:
                        self.ct_spawn.append((x, y))
                        self.grid[y][x] = 0
                        
        if not self.t_spawn:
            for y in range(self.height-4, self.height-1):
                for x in range(self.width-4, self.width-1):
                    if 0 <= y < self.height and 0 <= x < self.width:
                        self.t_spawn.append((x, y))
                        self.grid[y][x] = 0
                    
        # Bomb sites - центральные комнаты
        self.bomb_sites = []
        for room in rooms[2:4]:  # Берем 2 центральные комнаты
            x, y, w, h = room
            center_x = x + w // 2
            center_y = y + h // 2
            self.bomb_sites.append((center_x, center_y))
            
        return self.grid
        
    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == 1
        return True
        
    def is_bomb_site(self, x, y):
        for bx, by in self.bomb_sites:
            if abs(x - bx) < 3 and abs(y - by) < 3:
                return True
        return False
        
    def check_wall_between(self, x1, y1, x2, y2):
        # Проверка, есть ли стена между двумя точками
        steps = 50
        for i in range(steps):
            x = x1 + (x2 - x1) * i / steps
            y = y1 + (y2 - y1) * i / steps
            if self.is_wall(int(x), int(y)):
                return True
        return False
        
    def draw_minimap(self, surface, player_x, player_y):
        # Отрисовка миникарты
        map_scale = 5
        map_width = self.width * map_scale
        map_height = self.height * map_scale
        map_surface = pygame.Surface((map_width, map_height))
        map_surface.set_alpha(200)
        
        # Рисуем карту
        for y in range(self.height):
            for x in range(self.width):
                color = BLACK if self.grid[y][x] == 0 else GRAY
                pygame.draw.rect(map_surface, color, 
                               (x * map_scale, y * map_scale, map_scale, map_scale))
                
        # Bomb sites
        for bx, by in self.bomb_sites:
            pygame.draw.rect(map_surface, YELLOW,
                           (bx * map_scale - 2, by * map_scale - 2,
                            map_scale + 4, map_scale + 4), 2)
                            
        # CT spawn
        for x, y in self.ct_spawn[:10]:  # Только несколько точек для скорости
            pygame.draw.circle(map_surface, BLUE,
                             (x * map_scale, y * map_scale), 2)
                             
        # T spawn
        for x, y in self.t_spawn[:10]:
            pygame.draw.circle(map_surface, RED,
                             (x * map_scale, y * map_scale), 2)
                             
        # Игрок
        pygame.draw.circle(map_surface, GREEN,
                         (int(player_x * map_scale), int(player_y * map_scale)), 3)
                         
        # Отображаем миникарту
        surface.blit(map_surface, (WIDTH - map_width - 10, 10))

class Game:
    def __init__(self, player_team=Team.CT, difficulty=Difficulty.EASY):
        self.player_team = player_team
        self.difficulty = difficulty
        self.map = MapGenerator()
        
        # Генерируем карту пока не получим валидные спавны
        valid_map = False
        attempts = 0
        while not valid_map and attempts < 10:
            self.map.generate_map()
            valid_map = len(self.map.ct_spawn) > 0 and len

# Инициализация
pygame.init()
pygame.mixer.init()
pygame.font.init()  # Добавляем инициализацию шрифтов

WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
DARK_GRAY = (50, 50, 50)
DARK_BROWN = (101, 67, 33)
STEEL = (192, 192, 192)

class WeaponType(Enum):
    KNIFE = 1
    PISTOL = 2
    SHOTGUN = 3
    RIFLE = 4
    SNIPER = 5

class Weapon:
    def __init__(self, weapon_type, name, damage, range_dist, fire_rate, ammo, price, color, size):
        self.type = weapon_type
        self.name = name
        self.damage = damage
        self.range = range_dist
        self.fire_rate = fire_rate
        self.ammo = ammo
        self.max_ammo = ammo
        self.price = price
        self.last_shot = 0
        self.color = color
        self.size = size  # (width, height)
        
    def draw(self, surface, x, y, scale=1.0):
        # Рисует 2D модельку оружия
        width, height = self.size
        width = int(width * scale)
        height = int(height * scale)
        
        if self.type == WeaponType.KNIFE:
            # Нож - увеличенная моделька
            # Лезвие
            pygame.draw.polygon(surface, STEEL, [
                (x, y + height//2),
                (x + width//2, y),
                (x + width, y + height//2),
                (x + width//2, y + height)
            ])
            # Рукоятка
            pygame.draw.rect(surface, DARK_BROWN, 
                           (x + width//2 - 3, y + height//2 - 3, 6, height//2 + 3))
            
        elif self.type == WeaponType.PISTOL:
            # Пистолет Glock-18 - увеличенная моделька
            # Основа
            pygame.draw.rect(surface, DARK_GRAY, (x, y + height//3, width, height//3))
            # Ствол
            pygame.draw.rect(surface, (70, 70, 70), (x + width, y + height//3 - 2, width//3, height//3 + 4))
            # Рукоятка
            pygame.draw.rect(surface, (40, 40, 40), (x - width//6, y + height//3, width//3, height*2//3))
            # Курок
            pygame.draw.circle(surface, (90, 90, 90), (x + width//4, y + height//3), 3)
            
        elif self.type == WeaponType.SHOTGUN:
            # Дробовик XM1014 - увеличенная моделька
            # Ствол (толстый)
            pygame.draw.rect(surface, (80, 60, 40), (x, y, width, height))
            # Затвор
            pygame.draw.rect(surface, (60, 40, 20), (x - width//4, y, width//4, height))
            # Рукоятка
            pygame.draw.rect(surface, DARK_BROWN, (x - width//3, y + height, width//3, height))
            # Приклад
            pygame.draw.rect(surface, BROWN, (x - width//2, y + height, width//4, height*2))
            
        elif self.type == WeaponType.RIFLE:
            # Винтовка AK-47 - увеличенная моделька
            # Ствол
            pygame.draw.rect(surface, (60, 40, 20), (x, y + height//3, width, height//3))
            # Магазин
            pygame.draw.rect(surface, STEEL, (x + width//3, y + height//2, width//4, height))
            # Приклад
            pygame.draw.rect(surface, DARK_BROWN, (x - width//3, y, width//3, height))
            # Цевье
            pygame.draw.rect(surface, BROWN, (x + width//2, y + height//3, width//3, height//3))
            # Рукоятка
            pygame.draw.rect(surface, (40, 40, 40), (x + width*2//3, y + height, width//6, height//2))
            
        elif self.type == WeaponType.SNIPER:
            # Снайперка AWP - увеличенная моделька
            # Ствол (очень длинный)
            pygame.draw.rect(surface, (40, 40, 60), (x, y + height//3, width, height//3))
            # Прицел
            pygame.draw.rect(surface, BLACK, (x + width//2, y, width//6, height//3))
            pygame.draw.circle(surface, RED, (x + width//2 + width//12, y + height//6), 3)
            # Приклад
            pygame.draw.rect(surface, DARK_BROWN, (x - width//3, y, width//3, height))
            # Сошки
            pygame.draw.line(surface, STEEL, (x + width, y + height*2//3), 
                           (x + width + width//6, y + height), 2)
            pygame.draw.line(surface, STEEL, (x + width, y + height//3), 
                           (x + width + width//6, y), 2)

WEAPONS = {
    WeaponType.KNIFE: Weapon(WeaponType.KNIFE, "Knife", 25, 1, 500, 1, 0, DARK_GRAY, (25, 10)),
    WeaponType.PISTOL: Weapon(WeaponType.PISTOL, "Glock-18", 15, 15, 300, 20, 300, DARK_GRAY, (30, 15)),
    WeaponType.SHOTGUN: Weapon(WeaponType.SHOTGUN, "XM1014", 40, 8, 1000, 8, 1200, (80, 60, 40), (40, 20)),
    WeaponType.RIFLE: Weapon(WeaponType.RIFLE, "AK-47", 25, 25, 150, 30, 2700, (60, 40, 20), (50, 15)),
    WeaponType.SNIPER: Weapon(WeaponType.SNIPER, "AWP", 100, 40, 1500, 10, 4750, (40, 40, 60), (60, 15))
}

class Team(Enum):
    CT = 1  # Контр-террористы
    T = 2   # Террористы

class Difficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3

class Player:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.health = 100
        self.armor = 0
        self.money = 800
        self.current_weapon = WEAPONS[WeaponType.PISTOL]
        self.weapons = [WEAPONS[WeaponType.KNIFE], self.current_weapon]
        self.kills = 0
        self.deaths = 0
        self.angle = 0
        self.speed = 0.05
        self.has_bomb = (team == Team.T)  # Только террористы могут нести бомбу
        self.planting_bomb = False
        self.plant_time = 0
        self.is_bot = False
        
    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Проверка столкновений со стенами
        if not game_map.is_wall(int(new_x), int(new_y)):
            self.x = new_x
            self.y = new_y
            
    def take_damage(self, damage):
        if self.armor > 0:
            damage = int(damage * 0.66)
            self.armor -= damage // 2
            if self.armor < 0:
                self.armor = 0
                
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return self.health <= 0
        
    def shoot(self, game):
        current_time = pygame.time.get_ticks()
        if (self.current_weapon.ammo > 0 and 
            current_time - self.current_weapon.last_shot > self.current_weapon.fire_rate):
            
            self.current_weapon.ammo -= 1
            self.current_weapon.last_shot = current_time
            
            # Расчет направления выстрела
            end_x = self.x + math.cos(self.angle) * self.current_weapon.range
            end_y = self.y + math.sin(self.angle) * self.current_weapon.range
            
            # Проверка попадания
            hit_enemy = False
            for enemy in game.enemies:
                if enemy.team != self.team and enemy.health > 0:
                    # Простая проверка дистанции и направления
                    dx = enemy.x - self.x
                    dy = enemy.y - self.y
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance < self.current_weapon.range:
                        angle_to_enemy = math.atan2(dy, dx)
                        angle_diff = abs(self.angle - angle_to_enemy)
                        
                        if angle_diff < 0.3:  # ~17 градусов
                            # Проверка, нет ли стены между
                            if not game.map.check_wall_between(self.x, self.y, enemy.x, enemy.y):
                                enemy.take_damage(self.current_weapon.damage)
                                if enemy.health <= 0:
                                    self.kills += 1
                                    self.money += 300
                                    if self.team == Team.CT:
                                        game.ct_kills += 1
                                    else:
                                        game.t_kills += 1
                                hit_enemy = True
                                
            # Эффект отдачи при выстреле
            if hit_enemy:
                # Дополнительные деньги за попадание
                self.money += 50
            return hit_enemy
        return False
        
    def buy_weapon(self, weapon_type):
        weapon = WEAPONS[weapon_type]
        if self.money >= weapon.price:
            self.money -= weapon.price
            # Создаем новую копию оружия, чтобы у каждого игрока был свой экземпляр
            new_weapon = Weapon(
                weapon.type, weapon.name, weapon.damage, weapon.range,
                weapon.fire_rate, weapon.ammo, weapon.price,
                weapon.color, weapon.size
            )
            self.weapons.append(new_weapon)
            self.current_weapon = new_weapon
            return True
        return False
        
    def switch_weapon(self, index):
        if 0 <= index < len(self.weapons):
            self.current_weapon = self.weapons[index]
            
    def reload(self):
        if hasattr(self.current_weapon, 'max_ammo'):
            needed = self.current_weapon.max_ammo - self.current_weapon.ammo
            # В реальной игре была бы система магазинов
            self.current_weapon.ammo = self.current_weapon.max_ammo
            
    def start_planting_bomb(self, game):
        if (self.team == Team.T and self.has_bomb and 
            game.map.is_bomb_site(int(self.x), int(self.y)) and
            not game.bomb_planted):
            self.planting_bomb = True
            self.plant_time = pygame.time.get_ticks()
            
    def update_planting(self, game):
        if self.planting_bomb:
            current_time = pygame.time.get_ticks()
            if current_time - self.plant_time > 3000:  # 3 секунды на установку
                game.plant_bomb(self.x, self.y)
                self.has_bomb = False
                self.planting_bomb = False
                return True
        return False
        
    def draw(self, surface, is_main_player=True):
        # Рисуем игрока
        color = BLUE if self.team == Team.CT else RED
        screen_x = int(self.x * 20) if is_main_player else int(self.x * 20)
        screen_y = int(self.y * 20) if is_main_player else int(self.y * 20)
        
        pygame.draw.circle(surface, color, (screen_x, screen_y), 8)
        
        # Линия направления взгляда
        end_x = screen_x + math.cos(self.angle) * 15
        end_y = screen_y + math.sin(self.angle) * 15
        pygame.draw.line(surface, WHITE, (screen_x, screen_y), (end_x, end_y), 2)
        
        # Бомба над головой
        if self.has_bomb:
            pygame.draw.circle(surface, YELLOW, (screen_x, screen_y - 15), 5)
            
        # Оружие в руках (для ботов)
        if self.is_bot and hasattr(self, 'current_weapon'):
            # Рисуем оружие рядом с ботом (увеличенное)
            weapon_x = screen_x + 15
            weapon_y = screen_y + 10
            self.current_weapon.draw(surface, weapon_x, weapon_y, scale=0.8)

class Bot(Player):
    def __init__(self, x, y, team, difficulty=Difficulty.EASY):
        super().__init__(x, y, team)
        self.is_bot = True
        self.ai_state = "patrol"  # patrol, chase, attack, flee
        self.target_x = x
        self.target_y = y
        self.last_decision = 0
        self.patrol_points = []
        self.last_shot_time = 0
        self.difficulty = difficulty
        
        # Настройки в зависимости от сложности
        if difficulty == Difficulty.EASY:
            self.armor = 0
            self.accuracy = 0.5
            self.reaction_time = 800
            self.detection_range = 8
        elif difficulty == Difficulty.NORMAL:
            self.armor = 100
            self.accuracy = 0.7
            self.reaction_time = 500
            self.detection_range = 10
        else:  # HARD
            self.armor = 200
            self.accuracy = 0.9
            self.reaction_time = 300
            self.detection_range = 12
            
        # Случайное оружие из доступных в магазине
        self.assign_random_weapon()
        
    def assign_random_weapon(self):
        # Назначает боту случайное оружие из доступных в магазине
        available_weapons = [
            WeaponType.PISTOL,
            WeaponType.SHOTGUN,
            WeaponType.RIFLE,
            WeaponType.SNIPER
        ]
        
        # В зависимости от сложности, разный шанс получить лучшее оружие
        if self.difficulty == Difficulty.EASY:
            weights = [0.4, 0.3, 0.2, 0.1]  # Чаще пистолеты
        elif self.difficulty == Difficulty.NORMAL:
            weights = [0.2, 0.3, 0.3, 0.2]  # Более сбалансированно
        else:  # HARD
            weights = [0.1, 0.2, 0.4, 0.3]  # Чаще винтовки и снайперки
            
        weapon_type = random.choices(available_weapons, weights=weights)[0]
        # Создаем новую копию оружия для бота
        weapon_template = WEAPONS[weapon_type]
        self.current_weapon = Weapon(
            weapon_template.type, weapon_template.name, weapon_template.damage,
            weapon_template.range, weapon_template.fire_rate, weapon_template.ammo,
            weapon_template.price, weapon_template.color, weapon_template.size
        )
        self.weapons = [WEAPONS[WeaponType.KNIFE], self.current_weapon]
        
    def update(self, game):
        current_time = pygame.time.get_ticks()
        
        # Принимаем решение в зависимости от сложности
        if current_time - self.last_decision > self.reaction_time:
            self.last_decision = current_time
            
            # Ищем ближайшего врага (игрока)
            nearest_enemy = game.player if game.player.team != self.team and game.player.health > 0 else None
            min_distance = float('inf')
            
            if nearest_enemy:
                dx = game.player.x - self.x
                dy = game.player.y - self.y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < self.detection_range:
                    min_distance = distance
                else:
                    nearest_enemy = None
                        
            if nearest_enemy:
                # Дальний бой для снайперов
                if self.current_weapon.type == WeaponType.SNIPER:
                    # Снайперы стараются держать дистанцию
                    if min_distance < 8:
                        self.ai_state = "flee"
                        # Отступаем от врага
                        self.target_x = self.x - (nearest_enemy.x - self.x) / min_distance * 5
                        self.target_y = self.y - (nearest_enemy.y - self.y) / min_distance * 5
                    elif min_distance < 25:
                        self.ai_state = "attack"
                        self.target_x = nearest_enemy.x
                        self.target_y = nearest_enemy.y
                        
                        # Стрелять с большей дистанции
                        if current_time - self.last_shot_time > self.current_weapon.fire_rate:
                            self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)
                            if self.shoot_at_player(game, nearest_enemy):
                                self.last_shot_time = current_time
                
                # Обычное поведение для другого оружия
                elif min_distance < 3:  # Ближний бой
                    self.ai_state = "attack"
                    self.target_x = nearest_enemy.x
                    self.target_y = nearest_enemy.y
                    
                    # Стрелять
                    if current_time - self.last_shot_time > self.current_weapon.fire_rate:
                        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)
                        if self.shoot_at_player(game, nearest_enemy):
                            self.last_shot_time = current_time
                elif min_distance < self.detection_range:  # Преследовать
                    self.ai_state = "chase"
                    self.target_x = nearest_enemy.x
                    self.target_y = nearest_enemy.y
                else:
                    self.ai_state = "patrol"
            else:
                # Патрулирование
                if self.ai_state == "patrol":
                    if not self.patrol_points:
                        # Генерируем случайные точки патрулирования
                        for _ in range(3):
                            px = random.randint(1, game.map.width - 2)
                            py = random.randint(1, game.map.height - 2)
                            self.patrol_points.append((px, py))
                    
                    # Достигли точки - берем следующую
                    dx = self.target_x - self.x
                    dy = self.target_y - self.y
                    if math.sqrt(dx*dx + dy*dy) < 1:
                        if self.patrol_points:
                            self.target_x, self.target_y = self.patrol_points.pop(0)
                            self.patrol_points.append((self.target_x, self.target_y))
                else:
                    self.ai_state = "patrol"
                    # Сброс цели патрулирования
                    if not self.patrol_points:
                        self.target_x = random.randint(1, game.map.width - 2)
                        self.target_y = random.randint(1, game.map.height - 2)
                    
        # Движение к цели
        if self.ai_state in ["chase", "patrol", "flee"]:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0.5:
                self.angle = math.atan2(dy, dx)
                move_x = math.cos(self.angle) * self.speed
                move_y = math.sin(self.angle) * self.speed
                
                # Если отступаем, двигаемся в противоположном направлении
                if self.ai_state == "flee":
                    move_x = -move_x
                    move_y = -move_y
                    
                self.move(move_x, move_y, game.map)
    
    def shoot_at_player(self, game, target):
        # Бот стреляет в цель с учетом сложности
        if self.current_weapon.ammo > 0:
            self.current_weapon.ammo -= 1
            
            # Проверка попадания
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.current_weapon.range:
                # Проверка, нет ли стены между ботом и целью
                if not game.map.check_wall_between(self.x, self.y, target.x, target.y):
                    # Шанс попадания зависит от дистанции и сложности
                    base_chance = self.accuracy
                    distance_penalty = distance * 0.02  # 2% снижение за каждую единицу дистанции
                    hit_chance = max(0.1, base_chance - distance_penalty)
                    
                    if random.random() < hit_chance:
                        target.take_damage(self.current_weapon.damage)
                        if isinstance(target, Player) and target.health <= 0:
                            target.deaths += 1
                            # Бот получает деньги за убийство
                            self.money += 300
                        return True
                        
            # Перезарядка при необходимости
            if self.current_weapon.ammo == 0:
                self.current_weapon.ammo = self.current_weapon.max_ammo
        return False

class MapGenerator:
    def __init__(self, width=40, height=30):
        self.width = width
        self.height = height
        self.grid = []
        self.ct_spawn = []
        self.t_spawn = []
        self.bomb_sites = []
        
    def generate_map(self):
        # Генерация случайной карты
        # Инициализация сетки
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Создаем основные комнаты
        rooms = []
        for _ in range(8):
            room_width = random.randint(5, 10)
            room_height = random.randint(5, 8)
            room_x = random.randint(1, self.width - room_width - 1)
            room_y = random.randint(1, self.height - room_height - 1)
            rooms.append((room_x, room_y, room_width, room_height))
            
            # Выкапываем комнату
            for y in range(room_y, room_y + room_height):
                for x in range(room_x, room_x + room_width):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.grid[y][x] = 0
                        
        # Соединяем комнаты коридорами
        for i in range(len(rooms) - 1):
            x1, y1, w1, h1 = rooms[i]
            x2, y2, w2, h2 = rooms[i + 1]
            
            center1_x = x1 + w1 // 2
            center1_y = y1 + h1 // 2
            center2_x = x2 + w2 // 2
            center2_y = y2 + h2 // 2
            
            # Горизонтальный коридор
            start_x = min(center1_x, center2_x)
            end_x = max(center1_x, center2_x)
            for x in range(start_x, end_x + 1):
                if 0 <= x < self.width and 0 <= center1_y < self.height:
                    self.grid[center1_y][x] = 0
                    
            # Вертикальный коридор
            start_y = min(center1_y, center2_y)
            end_y = max(center1_y, center2_y)
            for y in range(start_y, end_y + 1):
                if 0 <= center2_x < self.width and 0 <= y < self.height:
                    self.grid[y][center2_x] = 0
        
        # Добавляем случайные стены внутри комнат
        for _ in range(15):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            if self.grid[y][x] == 0:
                wall_type = random.choice(["pillar", "wall", "corner"])
                
                if wall_type == "pillar":
                    self.grid[y][x] = 1
                elif wall_type == "wall":
                    length = random.randint(2, 4)
                    direction = random.choice(["h", "v"])
                    for i in range(length):
                        if direction == "h" and x + i < self.width:
                            self.grid[y][x + i] = 1
                        elif direction == "v" and y + i < self.height:
                            self.grid[y + i][x] = 1
                            
        # Определяем зоны спавна
        # CT спавн - левая часть карты
        self.ct_spawn = []
        for y in range(self.height):
            for x in range(self.width // 4):
                if self.grid[y][x] == 0:
                    self.ct_spawn.append((x, y))
                    
        # T спавн - правая часть карты
        self.t_spawn = []
        for y in range(self.height):
            for x in range(self.width * 3 // 4, self.width):
                if self.grid[y][x] == 0:
                    self.t_spawn.append((x, y))
                    
        # Если списки спавнов пустые, добавляем хотя бы по одной точке
        if not self.ct_spawn:
            for y in range(1, 4):
                for x in range(1, 4):
                    if y < self.height and x < self.width:
                        self.ct_spawn.append((x, y))
                        self.grid[y][x] = 0
                        
        if not self.t_spawn:
            for y in range(self.height-4, self.height-1):
                for x in range(self.width-4, self.width-1):
                    if 0 <= y < self.height and 0 <= x < self.width:
                        self.t_spawn.append((x, y))
                        self.grid[y][x] = 0
                    
        # Bomb sites - центральные комнаты
        self.bomb_sites = []
        for room in rooms[2:4]:  # Берем 2 центральные комнаты
            x, y, w, h = room
            center_x = x + w // 2
            center_y = y + h // 2
            self.bomb_sites.append((center_x, center_y))
            
        return self.grid
        
    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == 1
        return True
        
    def is_bomb_site(self, x, y):
        for bx, by in self.bomb_sites:
            if abs(x - bx) < 3 and abs(y - by) < 3:
                return True
        return False
        
    def check_wall_between(self, x1, y1, x2, y2):
        # Проверка есть ли стена между двумя точками
        steps = 50
        for i in range(steps):
            x = x1 + (x2 - x1) * i / steps
            y = y1 + (y2 - y1) * i / steps
            if self.is_wall(int(x), int(y)):
                return True
        return False
        
    def draw_minimap(self, surface, player_x, player_y):
        # Отрисовка миникарты
        map_scale = 5
        map_width = self.width * map_scale
        map_height = self.height * map_scale
        map_surface = pygame.Surface((map_width, map_height))
        map_surface.set_alpha(200)
        
        # Рисуем карту
        for y in range(self.height):
            for x in range(self.width):
                color = BLACK if self.grid[y][x] == 0 else GRAY
                pygame.draw.rect(map_surface, color, 
                               (x * map_scale, y * map_scale, map_scale, map_scale))
                
        # Bomb sites
        for bx, by in self.bomb_sites:
            pygame.draw.rect(map_surface, YELLOW,
                           (bx * map_scale - 2, by * map_scale - 2,
                            map_scale + 4, map_scale + 4), 2)
                            
        # CT spawn
        for x, y in self.ct_spawn[:10]:  # Только несколько точек для скорости
            pygame.draw.circle(map_surface, BLUE,
                             (x * map_scale, y * map_scale), 2)
                             
        # T spawn
        for x, y in self.t_spawn[:10]:
            pygame.draw.circle(map_surface, RED,
                             (x * map_scale, y * map_scale), 2)
                             
        # Игрок
        pygame.draw.circle(map_surface, GREEN,
                         (int(player_x * map_scale), int(player_y * map_scale)), 3)
                         
        # Отображаем миникарту
        surface.blit(map_surface, (WIDTH - map_width - 10, 10))

class Game:
    def __init__(self, player_team=Team.CT, difficulty=Difficulty.EASY):
        self.player_team = player_team
        self.difficulty = difficulty
        self.map = MapGenerator()
        
        # Генерируем карту пока не получим валидные спавны
        valid_map = False
        attempts = 0
        while not valid_map and attempts < 10:
            self.map.generate_map()
            valid_map = len(self.map.ct_spawn) > 0 and len(self.map.t_spawn) > 0
            attempts += 1
            
        # Выбор команды игрока
        if player_team == Team.CT:
            spawn_point = random.choice(self.map.ct_spawn)
            enemy_team = Team.T
            enemy_spawn_list = self.map.t_spawn  # Боты спавнятся на T спавне
        else:
            spawn_point = random.choice(self.map.t_spawn)
            enemy_team = Team.CT
            enemy_spawn_list = self.map.ct_spawn  # Боты спавнятся на CT спавне
            
        self.player = Player(spawn_point[0] + 0.5, spawn_point[1] + 0.5, player_team)
        
        # Боты противоположной команды с указанной сложностью
        self.enemies = []
        num_enemies = 5 if difficulty == Difficulty.EASY else 6 if difficulty == Difficulty.NORMAL else 7
        
        for _ in range(num_enemies):
            if enemy_spawn_list:
                spawn_point = random.choice(enemy_spawn_list)
            else:
                # Резервные точки спавна
                if enemy_team == Team.T:
                    spawn_point = (self.map.width - 2, self.map.height - 2)
                else:
                    spawn_point = (2, 2)
                
            bot = Bot(spawn_point[0] + 0.5, spawn_point[1] + 0.5, enemy_team, difficulty)
            self.enemies.append(bot)
            
        # Состояние игры
        self.round_time = 180  # 3 минуты в секундах
        self.start_time = pygame.time.get_ticks()
        self.bomb_planted = False
        self.bomb_x = 0
        self.bomb_y = 0
        self.bomb_timer = 45  # 45 секунд на разминирование
        self.round_active = True
        self.ct_kills = 0
        self.t_kills = 0
        self.rounds_won_ct = 0
        self.rounds_won_t = 0
        self.current_round = 1
        self.show_team_select = False
        self.show_settings = False
        self.mouse_locked = True  # Мышь заблокирована по умолчанию
        self.waiting_for_next_round = False
        self.round_end_time = 0
        self.round_winner = None  # Кто выиграл раунд
        
        # Шрифты
        try:
            self.font = pygame.font.SysFont(None, 36)
            self.big_font = pygame.font.SysFont(None, 72)
        except:
            self.font = pygame.font.Font(None, 36)
            self.big_font = pygame.font.Font(None, 72)
        
    def plant_bomb(self, x, y):
        self.bomb_planted = True
        self.bomb_x = x
        self.bomb_y = y
        self.bomb_timer = 45
        
    def defuse_bomb(self):
        if self.bomb_planted:
            self.bomb_planted = False
            # CT выигрывают раунд
            self.round_winner = Team.CT
            self.rounds_won_ct += 1
            self.waiting_for_next_round = True
            self.round_end_time = pygame.time.get_ticks()
            self.round_active = False
            
    def check_round_end(self):
        # Если уже ждем следующий раунд, проверяем время задержки
        if self.waiting_for_next_round:
            current_time = pygame.time.get_ticks()
            if current_time - self.round_end_time > 3000:  # 3 секунды задержки
                self.start_new_round()
                self.waiting_for_next_round = False
            return
            
        # Проверяем условия окончания раунда только если раунд активен
        if not self.round_active:
            return
            
        # Проверка смерти всех террористов
        t_alive = any(e.health > 0 for e in self.enemies if e.team == Team.T)
        
        # Проверка смерти всех CT (игрока и ботов CT если они есть)
        player_alive = self.player.health > 0
        ct_alive = player_alive  # Пока только игрок
        
        # Определяем победителя
        winner = None
        
        # Если игрок умер
        if not player_alive:
            if self.player_team == Team.CT:
                winner = Team.T  # T выигрывают
            else:
                winner = Team.CT  # CT выигрывают
                
        # Если все террористы мертвы
        elif not t_alive:
            winner = Team.CT  # CT выигрывают
            
        # Проверка таймера бомбы
        elif self.bomb_planted:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            if elapsed > self.bomb_timer:
                winner = Team.T  # Бомба взорвалась, T выигрывают
                
        # Проверка времени раунда
        else:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            if elapsed > self.round_time:
                winner = Team.CT  # Время вышло, CT выигрывают
        
        # Если есть победитель, заканчиваем раунд
        if winner:
            self.round_winner = winner
            if winner == Team.CT:
                self.rounds_won_ct += 1
            else:
                self.rounds_won_t += 1
                
            self.waiting_for_next_round = True
            self.round_end_time = pygame.time.get_ticks()
            self.round_active = False
            
    def start_new_round(self):
        self.current_round += 1
        
        # Генерируем новую карту
        valid_map = False
        attempts = 0
        while not valid_map and attempts < 10:
            self.map.generate_map()
            valid_map = len(self.map.ct_spawn) > 0 and len(self.map.t_spawn) > 0
            attempts += 1
        
        # Респавн игрока
        if self.player_team == Team.CT:
            spawn_point = random.choice(self.map.ct_spawn)
            enemy_team = Team.T
            enemy_spawn_list = self.map.t_spawn
        else:
            spawn_point = random.choice(self.map.t_spawn)
            enemy_team = Team.CT
            enemy_spawn_list = self.map.ct_spawn
            
        self.player.x = spawn_point[0] + 0.5
        self.player.y = spawn_point[1] + 0.5
        self.player.health = 100
        self.player.armor = 0
        self.player.has_bomb = (self.player_team == Team.T)
        
        # Респавн ботов
        self.enemies = []
        
        num_enemies = 5 if self.difficulty == Difficulty.EASY else 6 if self.difficulty == Difficulty.NORMAL else 7
        
        for _ in range(num_enemies):
            if enemy_spawn_list:
                spawn_point = random.choice(enemy_spawn_list)
            else:
                # Резервные точки спавна
                if enemy_team == Team.T:
                    spawn_point = (self.map.width - 2, self.map.height - 2)
                else:
                    spawn_point = (2, 2)
                
            bot = Bot(spawn_point[0] + 0.5, spawn_point[1] + 0.5, enemy_team, self.difficulty)
            self.enemies.append(bot)
            
        # Сброс состояния бомбы
        self.bomb_planted = False
        self.start_time = pygame.time.get_ticks()
        self.round_active = True
        self.waiting_for_next_round = False
        self.round_winner = None
        
    def draw_raycaster_view(self, surface):
        # Фон
        surface.fill((100, 150, 200))  # Небо
        pygame.draw.rect(surface, (50, 50, 50),  # Пол
                        (0, HEIGHT//2, WIDTH, HEIGHT//2))
        
        # Raycasting для стен
        for ray in range(WIDTH):
            ray_angle = (self.player.angle - math.pi/6) + (ray/WIDTH) * (math.pi/3)
            
            # Бросок луча
            distance = 0
            hit_wall = False
            while distance < 20 and not hit_wall:
                distance += 0.1
                test_x = self.player.x + math.cos(ray_angle) * distance
                test_y = self.player.y + math.sin(ray_angle) * distance
                
                if self.map.is_wall(int(test_x), int(test_y)):
                    hit_wall = True
                    
            # Исправление рыбьего глаза
            distance *= math.cos(ray_angle - self.player.angle)
            
            # Высота стены
            wall_height = min(int(HEIGHT / (distance + 0.0001)), HEIGHT * 2)
            
            # Цвет стены (темнее для дальних стен)
            darken = min(1.0, distance / 10)
            wall_color = (
                int(150 * (1 - darken)),
                int(100 * (1 - darken)),
                int(50 * (1 - darken))
            )
            
            # Рисуем стену
            wall_top = HEIGHT//2 - wall_height//2
            wall_bottom = HEIGHT//2 + wall_height//2
            pygame.draw.line(surface, wall_color,
                           (ray, wall_top), (ray, wall_bottom))
            
            # Враги в поле зрения
            for enemy in self.enemies:
                if enemy.health > 0:
                    # Проверяем, находится ли враг на этом луче
                    dx = enemy.x - self.player.x
                    dy = enemy.y - self.player.y
                    enemy_dist = math.sqrt(dx*dx + dy*dy)
                    enemy_angle = math.atan2(dy, dx)
                    
                    # Проверка угла и расстояния
                    angle_diff = abs(ray_angle - enemy_angle)
                    ray_width = 0.01  # Ширина луча
                    
                    if angle_diff < ray_width and enemy_dist < distance:
                        # Проверка видимости (нет ли стены между)
                        if not self.map.check_wall_between(self.player.x, self.player.y, enemy.x, enemy.y):
                            # Рисуем врага
                            enemy_height = min(int(HEIGHT / (enemy_dist + 0.0001)), HEIGHT * 2)
                            enemy_top = HEIGHT//2 - enemy_height//2
                            enemy_bottom = HEIGHT//2 + enemy_height//2
                            
                            # Цвет врага в зависимости от команды
                            if enemy.team == Team.T:
                                enemy_color = (min(255, int(200 * (1 - darken))), 
                                             min(100, int(50 * (1 - darken))), 
                                             min(100, int(50 * (1 - darken))))
                            else:
                                enemy_color = (min(100, int(50 * (1 - darken))), 
                                             min(100, int(50 * (1 - darken))), 
                                             min(255, int(200 * (1 - darken))))
                            
                            # Рисуем врага как вертикальную линию
                            pygame.draw.line(surface, enemy_color,
                                           (ray, enemy_top), (ray, enemy_bottom), 3)
        
        # Прицел
        pygame.draw.circle(surface, RED, (WIDTH//2, HEIGHT//2), 5, 2)
        pygame.draw.line(surface, RED, (WIDTH//2-15, HEIGHT//2),
                        (WIDTH//2-5, HEIGHT//2), 2)
        pygame.draw.line(surface, RED, (WIDTH//2+5, HEIGHT//2),
                        (WIDTH//2+15, HEIGHT//2), 2)
        pygame.draw.line(surface, RED, (WIDTH//2, HEIGHT//2-15),
                        (WIDTH//2, HEIGHT//2-5), 2)
        pygame.draw.line(surface, RED, (WIDTH//2, HEIGHT//2+5),
                        (WIDTH//2, HEIGHT//2+15), 2)
        
    def draw_hud(self, surface):
        # Отрисовка HUD
        # Статус игрока
        hp_text = self.font.render(f"HP: {self.player.health}", True, 
                                 GREEN if self.player.health > 50 else RED)
        surface.blit(hp_text, (10, 10))
        
        armor_text = self.font.render(f"Armor: {self.player.armor}", True, BLUE)
        surface.blit(armor_text, (10, 50))
        
        money_text = self.font.render(f"${self.player.money}", True, YELLOW)
        surface.blit(money_text, (10, 90))
        
        ammo_text = self.font.render(
            f"{self.player.current_weapon.name}: {self.player.current_weapon.ammo}", 
            True, WHITE)
        surface.blit(ammo_text, (10, 130))
        
        # Информация о раунде
        round_text = self.font.render(f"Round: {self.current_round}", True, WHITE)
        surface.blit(round_text, (WIDTH//2 - 100, 10))
        
        score_text = self.font.render(f"CT: {self.rounds_won_ct} | T: {self.rounds_won_t}", 
                                    True, WHITE)
        surface.blit(score_text, (WIDTH//2 - 100, 50))
        
        # Таймер раунда
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        time_left = max(0, self.round_time - elapsed)
        minutes = int(time_left) // 60
        seconds = int(time_left) % 60
        
        time_color = GREEN if time_left > 30 else RED
        time_text = self.font.render(f"Time: {minutes:02d}:{seconds:02d}", 
                                   True, time_color)
        surface.blit(time_text, (WIDTH//2 - 100, 90))
        
        # Статистика
        kills_text = self.font.render(f"K/D: {self.player.kills}/{self.player.deaths}", 
                                    True, WHITE)
        surface.blit(kills_text, (WIDTH - 200, 10))
        
        # Таймер бомбы
        if self.bomb_planted:
            bomb_time = max(0, self.bomb_timer - elapsed)
            bomb_text = self.font.render(f"BOMB: {bomb_time:.1f}s", True, RED)
            surface.blit(bomb_text, (WIDTH//2 - 100, 130))
            
            # Индикатор бомбы
            pygame.draw.circle(surface, YELLOW, (WIDTH//2, 160), 10)
            
        # Сообщение о покупке
        buy_text = self.font.render("B: Buy Menu | 1-5: Switch Weapon | R: Reload | T: Switch Team | C: Settings", 
                                  True, WHITE)
        surface.blit(buy_text, (10, HEIGHT - 40))
        
        # Информация о команде и сложности
        team_text = self.font.render(f"Team: {'CT' if self.player_team == Team.CT else 'T'}", 
                                   True, BLUE if self.player_team == Team.CT else RED)
        surface.blit(team_text, (WIDTH - 200, 50))
        
        diff_text = self.font.render(f"Diff: {self.difficulty.name}", 
                                   True, GREEN if self.difficulty == Difficulty.EASY else YELLOW if self.difficulty == Difficulty.NORMAL else RED)
        surface.blit(diff_text, (WIDTH - 200, 90))
        
        # Оружие игрока в правом нижнем углу
        weapon_x = WIDTH - 120
        weapon_y = HEIGHT - 120
        self.player.current_weapon.draw(surface, weapon_x, weapon_y, scale=1.2)
        
        weapon_name = self.font.render(self.player.current_weapon.name, True, WHITE)
        surface.blit(weapon_name, (weapon_x - 10, weapon_y + 40))
        
    def draw_round_end_screen(self, surface):
        # Отрисовка экрана окончания раунда
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        surface.blit(overlay, (0, 0))
        
        if self.round_winner:
            winner_text = "CT WIN!" if self.round_winner == Team.CT else "T WIN!"
            color = BLUE if self.round_winner == Team.CT else RED
            
            result_text = self.big_font.render(winner_text, True, color)
            surface.blit(result_text, (WIDTH//2 - 150, HEIGHT//2 - 100))
            
            round_text = self.font.render(f"Round {self.current_round - 1} completed", True, WHITE)
            surface.blit(round_text, (WIDTH//2 - 120, HEIGHT//2 - 30))
            
            score_text = self.font.render(f"Score: CT {self.rounds_won_ct} - {self.rounds_won_t} T", True, WHITE)
            surface.blit(score_text, (WIDTH//2 - 120, HEIGHT//2 + 10))
            
            # Таймер до следующего раунда
            time_left = max(0, 3000 - (pygame.time.get_ticks() - self.round_end_time))
            timer_text = self.font.render(f"Next round in: {time_left//1000 + 1}", True, YELLOW)
            surface.blit(timer_text, (WIDTH//2 - 120, HEIGHT//2 + 50))
        
    def draw_team_select(self, surface):
        # команды
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        surface.blit(overlay, (0, 0))
        
        title = self.big_font.render("SELECT TEAM", True, YELLOW)
        surface.blit(title, (WIDTH//2 - 150, HEIGHT//2 - 150))
        
        # Кнопка CT
        ct_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 50, 400, 80)
        pygame.draw.rect(surface, BLUE, ct_rect)
        pygame.draw.rect(surface, WHITE, ct_rect, 3)
        
        ct_text = self.big_font.render("COUNTER-TERRORISTS", True, WHITE)
        surface.blit(ct_text, (WIDTH//2 - 190, HEIGHT//2 - 30))
        
        # Кнопка T
        t_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 50, 400, 80)
        pygame.draw.rect(surface, RED, t_rect)
        pygame.draw.rect(surface, WHITE, t_rect, 3)
        
        t_text = self.big_font.render("TERRORISTS", True, WHITE)
        surface.blit(t_text, (WIDTH//2 - 100, HEIGHT//2 + 70))
        
        info_text = self.font.render("Click to select team", True, WHITE)
        surface.blit(info_text, (WIDTH//2 - 100, HEIGHT//2 + 150))
        
        return ct_rect, t_rect
        
    def draw_settings_menu(self, surface):
        # меню и сложность
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        surface.blit(overlay, (0, 0))
        
        title = self.big_font.render("DIFFICULTY SETTINGS", True, YELLOW)
        surface.blit(title, (WIDTH//2 - 250, HEIGHT//2 - 200))
        
        # Кнопка Easy
        easy_color = GREEN if self.difficulty == Difficulty.EASY else (30, 100, 30)
        easy_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 100, 400, 80)
        pygame.draw.rect(surface, easy_color, easy_rect)
        pygame.draw.rect(surface, WHITE, easy_rect, 3)
        
        easy_text = self.big_font.render("EASY", True, WHITE)
        surface.blit(easy_text, (WIDTH//2 - 50, HEIGHT//2 - 80))
        
        easy_desc = self.font.render("Enemies: No armor, low accuracy", True, WHITE)
        surface.blit(easy_desc, (WIDTH//2 - 180, HEIGHT//2 - 40))
        
        # Кнопка Normal
        normal_color = YELLOW if self.difficulty == Difficulty.NORMAL else (100, 100, 30)
        normal_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2, 400, 80)
        pygame.draw.rect(surface, normal_color, normal_rect)
        pygame.draw.rect(surface, WHITE, normal_rect, 3)
        
        normal_text = self.big_font.render("NORMAL", True, WHITE)
        surface.blit(normal_text, (WIDTH//2 - 70, HEIGHT//2 + 20))
        
        normal_desc = self.font.render("Enemies: 100 armor, medium accuracy", True, WHITE)
        surface.blit(normal_desc, (WIDTH//2 - 190, HEIGHT//2 + 60))
        
        # Кнопка Hard
        hard_color = RED if self.difficulty == Difficulty.HARD else (100, 30, 30)
        hard_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 100, 400, 80)
        pygame.draw.rect(surface, hard_color, hard_rect)
        pygame.draw.rect(surface, WHITE, hard_rect, 3)
        
        hard_text = self.big_font.render("HARD", True, WHITE)
        surface.blit(hard_text, (WIDTH//2 - 50, HEIGHT//2 + 120))
        
        hard_desc = self.font.render("Enemies: 200 armor, high accuracy", True, WHITE)
        surface.blit(hard_desc, (WIDTH//2 - 190, HEIGHT//2 + 160))
        
        info_text = self.font.render("Click to select difficulty | C to close", True, WHITE)
        surface.blit(info_text, (WIDTH//2 - 180, HEIGHT//2 + 220))
        
        return easy_rect, normal_rect, hard_rect
        
    def draw_buy_menu(self, surface):
        # Отрисовка меню покупки
        menu_surface = pygame.Surface((500, 400))
        menu_surface.fill((40, 40, 40))
        menu_surface.set_alpha(240)
        
        title = self.font.render("BUY MENU (B to close)", True, YELLOW)
        menu_surface.blit(title, (10, 10))
        
        y_offset = 60
        weapons_to_show = [
            (WeaponType.PISTOL, "1. Glock-18 ($300)"),
            (WeaponType.SHOTGUN, "2. XM1014 ($1200)"),
            (WeaponType.RIFLE, "3. AK-47 ($2700)"),
            (WeaponType.SNIPER, "4. AWP ($4750)")
        ]
        
        for weapon_type, text in weapons_to_show:
            weapon = WEAPONS[weapon_type]
            can_afford = self.player.money >= weapon.price
            color = GREEN if can_afford else RED
            
            weapon_text = self.font.render(text, True, color)
            menu_surface.blit(weapon_text, (10, y_offset))
            
            # Рисуем большую модельку оружия рядом
            weapon.draw(menu_surface, 250, y_offset - 20, scale=1.5)
            
            # Показываем характеристики оружия
            stats_text = self.font.render(f"DMG: {weapon.damage} | RNG: {weapon.range} | ROF: {weapon.fire_rate}ms", 
                                        True, WHITE)
            menu_surface.blit(stats_text, (10, y_offset + 30))
            
            y_offset += 80
            
        # Броня
        armor_y = y_offset + 20
        armor_text = self.font.render("5. Kevlar Vest ($650)", True, 
                                    GREEN if self.player.money >= 650 else RED)
        menu_surface.blit(armor_text, (10, armor_y))
        
        # Рисуем бронежилет
        pygame.draw.rect(menu_surface, (100, 100, 150), (250, armor_y - 10, 40, 50))
        pygame.draw.rect(menu_surface, (150, 150, 200), (255, armor_y - 5, 30, 40))
        
        # Информация о деньгах
        money_text = self.font.render(f"Your money: ${self.player.money}", True, YELLOW)
        menu_surface.blit(money_text, (10, armor_y + 40))
        
        surface.blit(menu_surface, (WIDTH//2 - 250, HEIGHT//2 - 200))
        
    def run(self):
        running = True
        show_buy_menu = False
        
        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
                    elif event.key == pygame.K_b:
                        show_buy_menu = not show_buy_menu
                        if show_buy_menu:
                            # Разблокируем мышь в меню покупки
                            pygame.mouse.set_visible(True)
                            self.mouse_locked = False
                        else:
                            # Блокируем мышь обратно
                            pygame.mouse.set_visible(False)
                            pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
                            self.mouse_locked = True
                        
                    elif event.key == pygame.K_r:
                        self.player.reload()
                        
                    elif event.key == pygame.K_t:
                        # Смена команды через меню
                        self.show_team_select = True
                        pygame.mouse.set_visible(True)
                        self.mouse_locked = False
                        
                    elif event.key == pygame.K_c:
                        # Меню настроек сложности
                        self.show_settings = not self.show_settings
                        if self.show_settings:
                            pygame.mouse.set_visible(True)
                            self.mouse_locked = False
                        else:
                            pygame.mouse.set_visible(False)
                            pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
                            self.mouse_locked = True
                        
                    elif event.key == pygame.K_e:
                        # Взаимодействие (установка/разминирование бомбы)
                        if self.player.team == Team.T and not self.waiting_for_next_round:
                            self.player.start_planting_bomb(self)
                        elif self.bomb_planted and not self.waiting_for_next_round:
                            # Проверка рядом с бомбой
                            dx = self.player.x - self.bomb_x
                            dy = self.player.y - self.bomb_y
                            if math.sqrt(dx*dx + dy*dy) < 2:
                                self.defuse_bomb()
                                
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, 
                                      pygame.K_4, pygame.K_5] and not self.waiting_for_next_round:
                        index = event.key - pygame.K_1
                        if index == 4:  # Клавиша 5 - покупка брони
                            if self.player.money >= 650:
                                self.player.money -= 650
                                self.player.armor = 100
                        elif index < len(self.player.weapons):
                            self.player.switch_weapon(index)
                        
                    elif show_buy_menu and not self.waiting_for_next_round:
                        # Покупка в меню (только если не ждем следующий раунд)
                        if event.key == pygame.K_1:
                            if self.player.buy_weapon(WeaponType.PISTOL):
                                print(f"Куплен {WEAPONS[WeaponType.PISTOL].name}")
                        elif event.key == pygame.K_2:
                            if self.player.buy_weapon(WeaponType.SHOTGUN):
                                print(f"Куплен {WEAPONS[WeaponType.SHOTGUN].name}")
                        elif event.key == pygame.K_3:
                            if self.player.buy_weapon(WeaponType.RIFLE):
                                print(f"Куплен {WEAPONS[WeaponType.RIFLE].name}")
                        elif event.key == pygame.K_4:
                            if self.player.buy_weapon(WeaponType.SNIPER):
                                print(f"Куплен {WEAPONS[WeaponType.SNIPER].name}")
                        elif event.key == pygame.K_5:
                            if self.player.money >= 650:
                                self.player.money -= 650
                                self.player.armor = 100
                                print("Куплен бронежилет")
                                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # ЛКМ - стрельба
                        if not self.show_team_select and not self.show_settings and not show_buy_menu and not self.waiting_for_next_round:
                            self.player.shoot(self)
                        elif self.show_team_select:
                            # Обработка выбора команды
                            mouse_pos = pygame.mouse.get_pos()
                            ct_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 50, 400, 80)
                            t_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 50, 400, 80)
                            
                            if ct_rect.collidepoint(mouse_pos):
                                self.player_team = Team.CT
                                self.__init__(Team.CT, self.difficulty)
                                self.show_team_select = False
                                pygame.mouse.set_visible(False)
                                pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
                                self.mouse_locked = True
                            elif t_rect.collidepoint(mouse_pos):
                                self.player_team = Team.T
                                self.__init__(Team.T, self.difficulty)
                                self.show_team_select = False
                                pygame.mouse.set_visible(False)
                                pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
                                self.mouse_locked = True
                        elif self.show_settings:
                            # Обработка выбора сложности
                            mouse_pos = pygame.mouse.get_pos()
                            easy_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 100, 400, 80)
                            normal_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2, 400, 80)
                            hard_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 100, 400, 80)
                            
                            if easy_rect.collidepoint(mouse_pos):
                                self.difficulty = Difficulty.EASY
                                self.__init__(self.player_team, Difficulty.EASY)
                                self.show_settings = False
                                pygame.mouse.set_visible(False)
                                pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
                                self.mouse_locked = True
                            elif normal_rect.collidepoint(mouse_pos):
                                self.difficulty = Difficulty.NORMAL
                                self.__init__(self.player_team, Difficulty.NORMAL)
                                self.show_settings = False
                                pygame.mouse.set_visible(False)
                                pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
                                self.mouse_locked = True
                            elif hard_rect.collidepoint(mouse_pos):
                                self.difficulty = Difficulty.HARD
                                self.__init__(self.player_team, Difficulty.HARD)
                                self.show_settings = False
                                pygame.mouse.set_visible(False)
                                pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
                                self.mouse_locked = True
            
            if self.show_team_select:
                # Показываем меню выбора команды
                screen.fill(BLACK)
                self.draw_team_select(screen)
                pygame.display.flip()
                clock.tick(FPS)
                continue
                
            if self.show_settings:
                # Показываем меню настроек
                screen.fill(BLACK)
                self.draw_settings_menu(screen)
                pygame.display.flip()
                clock.tick(FPS)
                continue
                        
            # Управление движением - ИСПРАВЛЕННОЕ (правильные A/D)
            if not self.waiting_for_next_round:  # Только если раунд активен
                keys = pygame.key.get_pressed()
                move_x = 0
                move_y = 0
                
                if keys[pygame.K_w]:  # W - вперед
                    move_x += math.cos(self.player.angle) * self.player.speed
                    move_y += math.sin(self.player.angle) * self.player.speed
                if keys[pygame.K_s]:  # S - назад
                    move_x -= math.cos(self.player.angle) * self.player.speed
                    move_y -= math.sin(self.player.angle) * self.player.speed
                if keys[pygame.K_a]:  # A - влево (движение влево)
                    # ПРАВИЛЬНАЯ ФОРМУЛА для движения влево
                    move_x += math.cos(self.player.angle - math.pi/2) * self.player.speed
                    move_y += math.sin(self.player.angle - math.pi/2) * self.player.speed
                if keys[pygame.K_d]:  # D - вправо (движение вправо)
                    # ПРАВИЛЬНАЯ ФОРМУЛА для движения вправо
                    move_x += math.cos(self.player.angle + math.pi/2) * self.player.speed
                    move_y += math.sin(self.player.angle + math.pi/2) * self.player.speed
                    
                if move_x != 0 or move_y != 0:
                    self.player.move(move_x, move_y, self.map)
                    
                # Управление камерой мышью (только если мышь заблокирована)
                if self.mouse_locked and not show_buy_menu:
                    mouse_dx, mouse_dy = pygame.mouse.get_rel()
                    self.player.angle += mouse_dx * 0.005
                    # Центрируем курсор
                    pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
                
                # Обновление ботов
                for enemy in self.enemies:
                    if enemy.health > 0:
                        enemy.update(self)
                        
                # Обновление установки бомбы
                self.player.update_planting(self)
            
            # Проверка конца раунда
            self.check_round_end()
            
            # Отрисовка
            self.draw_raycaster_view(screen)
            self.draw_hud(screen)
            
            # Миникарта
            self.map.draw_minimap(screen, self.player.x, self.player.y)
            
            # Враги на миникарте
            map_scale = 5
            for enemy in self.enemies:
                if enemy.health > 0:
                    screen_x = WIDTH - self.map.width * map_scale - 10 + int(enemy.x * map_scale)
                    screen_y = 10 + int(enemy.y * map_scale)
                    color = RED if enemy.team == Team.T else BLUE
                    pygame.draw.circle(screen, color, (screen_x, screen_y), 2)
                    
            # Меню покупки
            if show_buy_menu:
                self.draw_buy_menu(screen)
                
            # Экран конца раунда
            if self.waiting_for_next_round:
                self.draw_round_end_screen(screen)
                
            pygame.display.flip()
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

def show_main_menu():
    # Показывает главное меню с выбором команды и сложности
    menu_font = pygame.font.Font(None, 48)
    title_font = pygame.font.Font(None, 72)
    
    menu_active = True
    selected_team = Team.CT
    selected_difficulty = Difficulty.EASY
    
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_1:
                    selected_team = Team.CT
                elif event.key == pygame.K_2:
                    selected_team = Team.T
                elif event.key == pygame.K_e:
                    selected_difficulty = Difficulty.EASY
                elif event.key == pygame.K_n:
                    selected_difficulty = Difficulty.NORMAL
                elif event.key == pygame.K_h:
                    selected_difficulty = Difficulty.HARD
                elif event.key == pygame.K_RETURN:
                    menu_active = False
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Проверка клика по кнопкам
                ct_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 150, 400, 80)
                t_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 50, 400, 80)
                easy_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 50, 400, 80)
                normal_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 140, 400, 80)
                hard_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 230, 400, 80)
                start_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 320, 200, 60)
                
                if ct_rect.collidepoint(mouse_pos):
                    selected_team = Team.CT
                elif t_rect.collidepoint(mouse_pos):
                    selected_team = Team.T
                elif easy_rect.collidepoint(mouse_pos):
                    selected_difficulty = Difficulty.EASY
                elif normal_rect.collidepoint(mouse_pos):
                    selected_difficulty = Difficulty.NORMAL
                elif hard_rect.collidepoint(mouse_pos):
                    selected_difficulty = Difficulty.HARD
                elif start_rect.collidepoint(mouse_pos):
                    menu_active = False
        
        # Отрисовка меню
        screen.fill((20, 20, 40))
        
        # Заголовок
        title = title_font.render("COUNTER-STRIKE 2D", True, YELLOW)
        screen.blit(title, (WIDTH//2 - 250, 50))
        
        # Подзаголовок
        subtitle = menu_font.render("Select your team:", True, WHITE)
        screen.blit(subtitle, (WIDTH//2 - 120, 150))
        
        # Кнопка CT
        ct_color = BLUE if selected_team == Team.CT else (30, 30, 100)
        ct_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 150, 400, 80)
        pygame.draw.rect(screen, ct_color, ct_rect)
        pygame.draw.rect(screen, WHITE, ct_rect, 3)
        
        ct_text = menu_font.render("COUNTER-TERRORISTS (Press 1)", True, WHITE)
        screen.blit(ct_text, (WIDTH//2 - 190, HEIGHT//2 - 130))
        
        # Кнопка T
        t_color = RED if selected_team == Team.T else (100, 30, 30)
        t_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 50, 400, 80)
        pygame.draw.rect(screen, t_color, t_rect)
        pygame.draw.rect(screen, WHITE, t_rect, 3)
        
        t_text = menu_font.render("TERRORISTS (Press 2)", True, WHITE)
        screen.blit(t_text, (WIDTH//2 - 140, HEIGHT//2 - 30))
        
        # Выбор сложности
        diff_title = menu_font.render("Select difficulty:", True, WHITE)
        screen.blit(diff_title, (WIDTH//2 - 120, HEIGHT//2 + 40))
        
        # Кнопка Easy
        easy_color = GREEN if selected_difficulty == Difficulty.EASY else (30, 100, 30)
        easy_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 50, 400, 80)
        pygame.draw.rect(screen, easy_color, easy_rect)
        pygame.draw.rect(screen, WHITE, easy_rect, 3)
        
        easy_text = menu_font.render("EASY (Press E)", True, WHITE)
        screen.blit(easy_text, (WIDTH//2 - 80, HEIGHT//2 + 70))
        
        # Кнопка Normal
        normal_color = YELLOW if selected_difficulty == Difficulty.NORMAL else (100, 100, 30)
        normal_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 140, 400, 80)
        pygame.draw.rect(screen, normal_color, normal_rect)
        pygame.draw.rect(screen, WHITE, normal_rect, 3)
        
        normal_text = menu_font.render("NORMAL (Press N)", True, WHITE)
        screen.blit(normal_text, (WIDTH//2 - 100, HEIGHT//2 + 160))
        
        # Кнопка Hard
        hard_color = RED if selected_difficulty == Difficulty.HARD else (100, 30, 30)
        hard_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 230, 400, 80)
        pygame.draw.rect(screen, hard_color, hard_rect)
        pygame.draw.rect(screen, WHITE, hard_rect, 3)
        
        hard_text = menu_font.render("HARD (Press H)", True, WHITE)
        screen.blit(hard_text, (WIDTH//2 - 80, HEIGHT//2 + 250))
        
        # Кнопка старта
        start_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 320, 200, 60)
        pygame.draw.rect(screen, GREEN, start_rect)
        pygame.draw.rect(screen, WHITE, start_rect, 3)
        
        start_text = menu_font.render("START GAME", True, WHITE)
        screen.blit(start_text, (WIDTH//2 - 80, HEIGHT//2 + 335))
        
        # Инструкции
        instructions = [
            "Controls:",
            "W - Forward",
            "S - Backward",
            "A - Strafe Left",
            "D - Strafe Right",
            "Mouse - Aim",
            "Left Click - Shoot",
            "R - Reload",
            "B - Buy Menu (free mouse)",
            "1-5 - Switch Weapons / Buy",
            "E - Plant/Defuse Bomb",
            "T - Switch Team",
            "C - Difficulty Settings",
            "ESC - Exit"
        ]
        
        for i, line in enumerate(instructions):
            inst_text = pygame.font.Font(None, 28).render(line, True, WHITE)
            screen.blit(inst_text, (50, 400 + i * 30))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return selected_team, selected_difficulty

if __name__ == "__main__":
    print("Запуск Counter-Strike 2D...")
    
    # Показываем меню выбора команды и сложности
    selected_team, selected_difficulty = show_main_menu()
    
    print(f"\nВы выбрали команду: {'CT' if selected_team == Team.CT else 'T'}")
    print(f"Сложность: {selected_difficulty.name}")
    print("Игра начинается...")
    
    # Запускаем игру с выбранной командой и сложностью
    game = Game(selected_team, selected_difficulty)
    game.run()