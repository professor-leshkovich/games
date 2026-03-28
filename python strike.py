from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

# Инициализация приложения
app = Ursina(borderless=False, fullscreen=False)

# Настройки окна
window.title = 'PS:GO - Mirage Clone'
window.size = (1920, 1080)
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Переменные игры
score = 0
money = 800
health = 100
max_health = 100
ammo = 30
max_ammo = 30
current_weapon = "AK-47"
reloading = False
enemies_killed = 0
can_shoot = True
game_active = True

# Словарь оружия
weapons = {
    "AK-47": {"price": 2700, "damage": 36, "ammo": 30, "color": color.rgb(50, 50, 50), "range": 100, "fire_rate": 0.1},
    "M4A4": {"price": 3100, "damage": 33, "ammo": 30, "color": color.rgb(80, 80, 80), "range": 100, "fire_rate": 0.09},
    "AWP": {"price": 4750, "damage": 115, "ammo": 10, "color": color.rgb(40, 40, 80), "range": 150, "fire_rate": 1.2},
    "Deagle": {"price": 700, "damage": 70, "ammo": 7, "color": color.gold, "range": 80, "fire_rate": 0.5},
    "P90": {"price": 2350, "damage": 26, "ammo": 50, "color": color.rgb(30, 30, 30), "range": 70, "fire_rate": 0.07}
}

# Создание интерфейса
def update_ui():
    if game_active:
        health_text.text = f'❤️ {int(health)}'
        money_text.text = f'💰 {money}$'
        ammo_text.text = f'{ammo} / {max_ammo}'
        weapon_text.text = f'🔫 {current_weapon}'
        score_text.text = f'🎯 Score: {score}'
        kill_text.text = f'💀 Kills: {enemies_killed}'

health_text = Text(text=f'❤️ {health}', position=(-0.85, 0.48), scale=2, color=color.red)
money_text = Text(text=f'💰 {money}$', position=(-0.85, 0.43), scale=2, color=color.green)
ammo_text = Text(text=f'{ammo} / {max_ammo}', position=(-0.85, 0.38), scale=2, color=color.white)
weapon_text = Text(text=f'🔫 {current_weapon}', position=(-0.85, 0.33), scale=2, color=color.orange)
score_text = Text(text=f'🎯 Score: {score}', position=(-0.85, 0.28), scale=2, color=color.white)
kill_text = Text(text=f'💀 Kills: {enemies_killed}', position=(-0.85, 0.23), scale=2, color=color.white)

# Текст защиты при спавне
protection_text = Text(text='🛡️ SPAWN PROTECTION', position=(0, 0.4), scale=2, color=color.yellow, origin=(0, 0))
protection_text.enabled = True
invoke(lambda: setattr(protection_text, 'enabled', False), delay=3)

# Меню покупки
buy_menu_visible = False
buy_menu = None

# Создание карты Mirage в песочных тонах
class MirageMap:
    def __init__(self):
        # Пол (песок)
        self.ground = Entity(model='cube', scale=(100, 0.5, 100), 
                            position=(0, -1, 0), collider='box', 
                            color=color.rgb(210, 180, 140))
        
        # Стены зданий (песочные цвета)
        self.building_a = Entity(model='cube', color=color.rgb(180, 120, 80), 
                                scale=(8, 5, 8), position=(-15, 1, -10), collider='box')
        self.building_b = Entity(model='cube', color=color.rgb(160, 110, 70), 
                                scale=(8, 5, 8), position=(15, 1, 10), collider='box')
        self.mid_building = Entity(model='cube', color=color.rgb(200, 150, 100), 
                                  scale=(6, 4, 6), position=(0, 0.5, 0), collider='box')
        self.underpass = Entity(model='cube', color=color.rgb(120, 80, 50), 
                               scale=(5, 3, 10), position=(-10, -0.5, 15), collider='box')
        self.stairs = Entity(model='cube', color=color.rgb(150, 130, 100), 
                            scale=(4, 2, 4), position=(12, -0.5, -12), collider='box')
        
        # Ящики для укрытий
        boxes_positions = [
            (5, -0.5, 5), (-5, -0.5, 5), (5, -0.5, -5), (-5, -0.5, -5),
            (3, -0.5, -3), (-3, -0.5, 3), (8, -0.5, -8), (-8, -0.5, 8),
            (0, -0.5, 8), (0, -0.5, -8), (8, -0.5, 0), (-8, -0.5, 0),
            (12, -0.5, 5), (-12, -0.5, 5), (12, -0.5, -5), (-12, -0.5, -5)
        ]
        
        self.boxes = []
        for pos in boxes_positions:
            box = Entity(model='cube', color=color.rgb(139, 90, 43), 
                        scale=(1.5, 1, 1.5), position=pos, collider='box')
            self.boxes.append(box)
        
        # Столбы
        pillars_positions = [
            (-5, 0, -5), (5, 0, -5), (-5, 0, 5), (5, 0, 5),
            (-10, 0, -10), (10, 0, -10), (-10, 0, 10), (10, 0, 10)
        ]
        
        self.pillars = []
        for pos in pillars_positions:
            pillar = Entity(model='cylinder', color=color.rgb(140, 120, 90), 
                          scale=(0.5, 3, 0.5), position=pos, collider='box')
            self.pillars.append(pillar)
        
        # Кактусы
        cactus_positions = [
            (-18, -1, -18), (18, -1, -18), (-18, -1, 18), (18, -1, 18),
            (-15, -1, -20), (15, -1, -20), (-20, -1, 15), (20, -1, -15),
            (-22, -1, -5), (22, -1, 5), (-5, -1, 22), (5, -1, -22)
        ]
        
        self.cacti = []
        for pos in cactus_positions:
            cactus_body = Entity(model='cylinder', color=color.rgb(60, 80, 40), 
                                scale=(0.6, 2, 0.6), position=pos, collider='box')
            cactus_arm1 = Entity(model='cylinder', color=color.rgb(60, 80, 40), 
                                scale=(0.4, 1, 0.4), position=(pos[0]+0.5, pos[1]+0.5, pos[2]), collider='box')
            cactus_arm2 = Entity(model='cylinder', color=color.rgb(60, 80, 40), 
                                scale=(0.4, 1, 0.4), position=(pos[0]-0.5, pos[1]+0.5, pos[2]), collider='box')
            self.cacti.extend([cactus_body, cactus_arm1, cactus_arm2])
        
        # Песочные дюны
        dune_positions = [
            (7, -0.8, 7), (-7, -0.8, 7), (7, -0.8, -7), (-7, -0.8, -7),
            (4, -0.9, 4), (-4, -0.9, 4), (11, -0.7, 11), (-11, -0.7, -11)
        ]
        
        self.dunes = []
        for pos in dune_positions:
            dune = Entity(model='sphere', color=color.rgb(200, 160, 110), 
                         scale=(2, 0.3, 2), position=pos)
            self.dunes.append(dune)

# Класс оружия
class WeaponModel(Entity):
    def __init__(self, weapon_type, position=(0.5, -0.5, 0.5)):
        super().__init__(parent=camera, position=position, rotation=(0, 0, 0))
        self.weapon_type = weapon_type
        self.create_weapon_model()
        
    def create_weapon_model(self):
        if self.weapon_type == "AK-47":
            self.body = Entity(model='cube', color=color.rgb(50, 50, 50), 
                              scale=(0.2, 0.1, 0.8), parent=self)
            self.grip = Entity(model='cube', color=color.rgb(100, 70, 30), 
                              scale=(0.15, 0.08, 0.4), position=(0, -0.08, -0.3), parent=self)
            self.barrel = Entity(model='cylinder', color=color.rgb(30, 30, 30), 
                                scale=(0.07, 0.07, 0.6), position=(0, 0.02, 0.5), parent=self)
            self.mag = Entity(model='cube', color=color.rgb(40, 40, 40), 
                             scale=(0.12, 0.15, 0.2), position=(0, -0.05, 0), parent=self)
            
        elif self.weapon_type == "AWP":
            self.body = Entity(model='cylinder', color=color.rgb(40, 40, 80), 
                              scale=(0.12, 0.12, 1.2), parent=self)
            self.scope = Entity(model='cylinder', color=color.black, 
                               scale=(0.15, 0.15, 0.2), position=(0, 0.1, 0.2), parent=self)
            self.barrel = Entity(model='cylinder', color=color.rgb(30, 30, 30), 
                                scale=(0.08, 0.08, 0.8), position=(0, 0, 0.7), parent=self)
            self.bipod = Entity(model='cube', color=color.rgb(60, 60, 60), 
                               scale=(0.2, 0.05, 0.3), position=(0, -0.1, 0.1), parent=self)
            
        elif self.weapon_type == "M4A4":
            self.body = Entity(model='cube', color=color.rgb(80, 80, 80), 
                              scale=(0.18, 0.1, 0.9), parent=self)
            self.suppressor = Entity(model='cylinder', color=color.rgb(60, 60, 60), 
                                    scale=(0.09, 0.09, 0.3), position=(0, 0, 0.55), parent=self)
            
        elif self.weapon_type == "Deagle":
            self.body = Entity(model='cube', color=color.gold, 
                              scale=(0.15, 0.12, 0.6), parent=self)
            
        elif self.weapon_type == "P90":
            self.body = Entity(model='cube', color=color.rgb(30, 30, 30), 
                              scale=(0.2, 0.12, 0.7), parent=self)
            self.mag_top = Entity(model='cylinder', color=color.rgb(50, 50, 50), 
                                 scale=(0.12, 0.12, 0.25), position=(0, 0.08, 0.1), parent=self)
    
    def shoot_animation(self):
        self.animate('position', (0.55, -0.55, 0.45), duration=0.05, curve=curve.out_quad)
        self.animate('position', (0.5, -0.5, 0.5), duration=0.1, delay=0.05)

# Класс врага
class EnemyBot(Entity):
    def __init__(self, position=(0, 0, 0), weapon_type="AK-47"):
        super().__init__(
            model='cube',
            color=color.rgb(220, 20, 20),
            scale=(0.8, 1.8, 0.8),
            position=position,
            collider='box'
        )
        self.health = 100
        self.max_health = 100
        self.speed = 2.5
        self.damage = weapons[weapon_type]["damage"]
        self.weapon = weapon_type
        self.shoot_cooldown = random.uniform(0.5, 1.5)
        self.attack_range = weapons[weapon_type]["range"]
        
        # Визуальное оружие для бота
        self.weapon_model = Entity(model='cube', color=color.rgb(80, 80, 80),
                                   scale=(0.3, 0.2, 0.8), position=(0.5, 0.5, 0.5), parent=self)
        
        # Патрулирование
        self.patrol_points = []
        self.current_target = None
        self.create_patrol_path()
        
    def create_patrol_path(self):
        # Исправлено: теперь кортежи с 3 значениями
        patrol_areas = [
            (-12, 0, -8), (-5, 0, -5), (0, 0, 0), (8, 0, 5), (12, 0, 8),
            (8, 0, -5), (-8, 0, 5), (-12, 0, 8), (12, 0, -8)
        ]
        self.patrol_points = [Vec3(x, y, z) for x, y, z in patrol_areas]
        
    def update(self):
        if self.health <= 0 or not game_active:
            return
        
        # Поиск игрока
        player_distance = distance(self.position, player.position)
        
        # Проверка защиты игрока
        if player.spawn_protection_active:
            self.patrol_behavior()
            return
        
        if player_distance < self.attack_range:
            # Атаковать игрока
            self.look_at(player.position)
            
            if self.shoot_cooldown <= 0:
                self.shoot_at_player()
                self.shoot_cooldown = weapons[self.weapon]["fire_rate"]
            else:
                self.shoot_cooldown -= time.dt
                
            # Двигаться к игроку или отступать
            if player_distance < 5:
                self.position -= (self.forward * self.speed * time.dt)
            else:
                self.position += (self.forward * self.speed * time.dt)
        else:
            self.patrol_behavior()
        
        # Ограничение движения
        self.x = max(-22, min(22, self.x))
        self.z = max(-22, min(22, self.z))
        self.y = 0
        
        # Обновление цвета
        if self.health > 0:
            health_percent = self.health / self.max_health
            red_intensity = 100 + (120 * health_percent)
            self.color = color.rgb(red_intensity, 20, 20)
    
    def patrol_behavior(self):
        if self.current_target is None or distance(self.position, self.current_target) < 1:
            self.current_target = random.choice(self.patrol_points)
        
        direction = (self.current_target - self.position).normalized()
        self.position += direction * self.speed * time.dt
        self.look_at(self.current_target)
    
    def shoot_at_player(self):
        global health, game_active
        if not game_active or player.spawn_protection_active:
            return
            
        distance_factor = max(0.5, 1 - (distance(self.position, player.position) / self.attack_range))
        damage = self.damage * distance_factor
        
        health -= damage
        update_ui()
        
        # Эффект выстрела
        muzzle_flash = Entity(model='quad', texture='circle', scale=0.1, 
                             position=self.weapon_model.world_position, color=color.yellow)
        destroy(muzzle_flash, delay=0.05)
        
        if health <= 0 and game_active:
            player.die()
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
        else:
            self.color = color.white
            invoke(self.reset_color, delay=0.1)
    
    def reset_color(self):
        if self.health > 0:
            health_percent = self.health / self.max_health
            red_intensity = 100 + (120 * health_percent)
            self.color = color.rgb(red_intensity, 20, 20)
    
    def die(self):
        global score, enemies_killed, money
        # Эффект взрыва
        explosion = Entity(model='sphere', color=color.orange, scale=0.5, position=self.position)
        explosion.animate_scale(2, duration=0.3)
        destroy(explosion, delay=0.3)
        
        destroy(self)
        score += 100
        enemies_killed += 1
        money += weapons[self.weapon]["price"] // 2
        update_ui()
        if self in enemies:
            enemies.remove(self)
        
        invoke(spawn_enemy, delay=3)

# Игрок
class Player(FirstPersonController):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.speed = 8
        self.position = (0, 1, 0)
        self.cursor.visible = False
        self.weapon_model = WeaponModel(current_weapon)
        self.spawn_protection_active = True
        self.protection_end_time = time.time() + 3
        
    def update(self):
        super().update()
        
        if self.spawn_protection_active and time.time() > self.protection_end_time:
            self.spawn_protection_active = False
            protection_text.enabled = False
            
        if game_active:
            health_text.text = f'❤️ {int(self.health)}'
    
    def die(self):
        global game_active, health
        game_active = False
        health = 0
        update_ui()
        self.disable()
        
        overlay = Entity(model='quad', scale=2, color=color.rgba(0, 0, 0, 0), parent=camera.ui)
        overlay.animate('color', color.rgba(0, 0, 0, 128), duration=1)
        
        game_over_text = Text(text='GAME OVER\nPress R to restart', 
                             origin=(0, 0), scale=3, color=color.red, parent=camera.ui)
        
        self.game_over_text = game_over_text
        self.overlay = overlay
    
    def restart_game(self):
        global game_active, health, money, score, enemies_killed, current_weapon, ammo, max_ammo
        
        game_active = True
        health = 100
        money = 800
        score = 0
        enemies_killed = 0
        current_weapon = "AK-47"
        ammo = weapons[current_weapon]["ammo"]
        max_ammo = weapons[current_weapon]["ammo"]
        
        self.enable()
        self.health = 100
        self.position = (0, 1, 0)
        self.spawn_protection_active = True
        self.protection_end_time = time.time() + 3
        protection_text.enabled = True
        
        update_ui()
        
        for enemy in enemies[:]:
            destroy(enemy)
        enemies.clear()
        for _ in range(4):
            spawn_enemy()
        
        if hasattr(self, 'game_over_text') and self.game_over_text:
            destroy(self.game_over_text)
        if hasattr(self, 'overlay') and self.overlay:
            destroy(self.overlay)

player = Player()

# Система покупки
def show_buy_menu():
    global buy_menu_visible, buy_menu
    if buy_menu_visible:
        if buy_menu:
            destroy(buy_menu)
        buy_menu_visible = False
        return
    
    if not game_active:
        return
        
    buy_menu_visible = True
    buy_menu = Entity(model='quad', scale=(0.6, 0.8), color=color.rgba(0, 0, 0, 200), position=(0, 0), parent=camera.ui)
    
    title = Text(text='BUY MENU', position=(0, 0.35), scale=2, color=color.gold, parent=buy_menu)
    money_display = Text(text=f'Money: ${money}', position=(0, 0.3), scale=1.5, color=color.green, parent=buy_menu)
    
    weapon_list = list(weapons.keys())
    y_pos = 0.2
    for i, weapon in enumerate(weapon_list):
        price = weapons[weapon]["price"]
        color_weapon = color.green if money >= price else color.red
        btn = Button(text=f'{weapon} - ${price}', 
                    position=(0, y_pos - i * 0.07), 
                    scale=(0.4, 0.05),
                    color=color_weapon,
                    parent=buy_menu)
        btn.weapon_name = weapon
        btn.on_click = Func(buy_weapon, weapon)

def buy_weapon(weapon_name):
    global money, current_weapon, ammo, max_ammo
    price = weapons[weapon_name]["price"]
    
    if money >= price:
        money -= price
        current_weapon = weapon_name
        ammo = weapons[weapon_name]["ammo"]
        max_ammo = weapons[weapon_name]["ammo"]
        update_ui()
        
        destroy(player.weapon_model)
        player.weapon_model = WeaponModel(current_weapon)
        
        notification = Text(text=f'Bought {weapon_name}!', position=(0, -0.4), 
                           scale=1.5, color=color.green, lifetime=2, parent=camera.ui)
        
        show_buy_menu()
    else:
        notification = Text(text='Not enough money!', position=(0, -0.4), 
                           scale=1.5, color=color.red, lifetime=2, parent=camera.ui)

# Функции стрельбы
def shoot():
    global ammo, reloading, can_shoot, game_active, score
    
    if not game_active or reloading or not can_shoot:
        return
    
    if ammo <= 0:
        reload_weapon()
        return
    
    player.weapon_model.shoot_animation()
    
    camera.rotation_x -= random.uniform(1, 3)
    camera.rotation_z += random.uniform(-0.5, 0.5)
    invoke(reset_camera_recoil, delay=0.1)
    
    ammo -= 1
    update_ui()
    
    hit_info = raycast(camera.world_position, camera.forward, 
                       distance=weapons[current_weapon]["range"], 
                       ignore=[player, player.weapon_model])
    
    if hit_info.hit:
        hit_effect = Entity(model='quad', texture='circle', scale=0.1, 
                           position=hit_info.world_point, color=color.yellow)
        hit_effect.animate_scale(0.3, duration=0.2)
        destroy(hit_effect, delay=0.2)
        
        if isinstance(hit_info.entity, EnemyBot):
            damage = weapons[current_weapon]["damage"]
            hit_info.entity.take_damage(damage)
            score += 10
            update_ui()
    
    can_shoot = False
    invoke(reset_shoot_cooldown, delay=weapons[current_weapon]["fire_rate"])

def reset_shoot_cooldown():
    global can_shoot
    can_shoot = True

def reset_camera_recoil():
    camera.rotation_x = 0
    camera.rotation_z = 0

def reload_weapon():
    global reloading, ammo
    if reloading or ammo == max_ammo or not game_active:
        return
    
    reloading = True
    ammo_text.text = '⟳ Reloading...'
    invoke(finish_reload, delay=2)

def finish_reload():
    global reloading, ammo
    ammo = max_ammo
    reloading = False
    update_ui()

# Создание врагов
enemies = []

def spawn_enemy():
    if len(enemies) < 6 and game_active:
        weapons_list = list(weapons.keys())
        enemy_weapon = random.choice(weapons_list)
        
        spawn_points = [
            (-15, 0, -12), (15, 0, 12), (-12, 0, 15), (12, 0, -15),
            (-8, 0, 8), (8, 0, -8), (0, 0, 12), (0, 0, -12),
            (-18, 0, -5), (18, 0, 5), (-5, 0, 18), (5, 0, -18)
        ]
        
        valid_spawns = [pos for pos in spawn_points if distance(Vec3(*pos), player.position) > 10]
        if not valid_spawns:
            valid_spawns = spawn_points
            
        spawn_pos = random.choice(valid_spawns)
        
        enemy = EnemyBot(position=spawn_pos, weapon_type=enemy_weapon)
        enemies.append(enemy)

# Создание карты
mirage_map = MirageMap()

# Добавляем свет и небо
Sky()
# Добавляем туман
scene.fog_color = color.rgb(210, 180, 140)
scene.fog_density = 0.02

# Свет с теплым оттенком
DirectionalLight(shadows=True, intensity=1.5, color=color.rgb(255, 240, 200))

# Создание врагов в начале
def spawn_initial_enemies():
    for _ in range(4):
        spawn_enemy()

invoke(spawn_initial_enemies, delay=0.5)

# Прицел
crosshair = Entity(model='quad', texture='circle', scale=0.02, color=color.white, parent=camera.ui)
crosshair.eternal = True

# Обработка ввода
def input(key):
    if key == 'left mouse down':
        shoot()
    elif key == 'r':
        if not game_active:
            player.restart_game()
        else:
            reload_weapon()
    elif key == 'b':
        if game_active:
            show_buy_menu()
    elif key == 'escape':
        application.quit()
    elif key == 'f' and game_active:
        hit_info = raycast(camera.world_position, camera.forward, distance=2)
        if hit_info.hit and hasattr(hit_info.entity, 'weapon'):
            global current_weapon, ammo, max_ammo
            current_weapon = hit_info.entity.weapon
            ammo = weapons[current_weapon]["ammo"] // 2
            max_ammo = weapons[current_weapon]["ammo"]
            update_ui()
            destroy(player.weapon_model)
            player.weapon_model = WeaponModel(current_weapon)
            notification = Text(text=f'Picked up {current_weapon}!', 
                               position=(0, -0.3), scale=1.5, lifetime=1, parent=camera.ui)

# Запуск игры
app.run()