from ursina import *
import random

app = Ursina()
window.title = "Mewgenics Clone"
window.size = (800, 600)
window.color = color.rgb(30, 30, 50)

# Глобальные переменные
game_state = 'menu'
selected_cat = None
current_enemy = None
battle_elements = []
menu_elements = []

# Класс персонажа
class Character:
    def __init__(self, name, health, damage, abilities, color_val):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.abilities = abilities
        self.color = color_val
        self.entity = None
        self.health_text = None
        
    def create_entity(self, position, scale=(2, 2)):
        self.entity = Entity(
            model='quad',
            color=self.color,
            position=position,
            scale=scale,
            collider='box'
        )
        return self.entity
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        if self.health_text:
            self.update_health_text()
        return self.health <= 0
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        if self.health_text:
            self.update_health_text()
    
    def attack(self, target):
        damage = random.randint(self.damage - 3, self.damage + 3)
        if damage < 1:
            damage = 1
        is_dead = target.take_damage(damage)
        return damage, is_dead
    
    def update_health_text(self):
        if self.health_text:
            self.health_text.text = f"{self.name}\n❤️ {self.health}/{self.max_health}"

# Создание котов
cats = [
    Character("Сиамский воин", 50, 15, ["Царапка", "Сильный удар"], color.rgb(200, 180, 150)),
    Character("Персидский маг", 40, 12, ["Лечение", "Магический удар"], color.rgb(220, 200, 170)),
    Character("Британский танк", 70, 10, ["Защита", "Мощный удар"], color.rgb(150, 150, 160))
]

# Создание врагов
enemies = [
    Character("Злая собака", 45, 12, ["Укус", "Рывок"], color.rgb(100, 80, 60)),
    Character("Гигантская крыса", 35, 15, ["Укус", "Царапка"], color.rgb(80, 80, 90)),
    Character("Босс-кот", 80, 20, ["Сильный удар", "Рывок"], color.rgb(180, 100, 100))
]

def clear_elements(elements_list):
    for element in elements_list:
        if isinstance(element, Entity):
            destroy(element)
        elif isinstance(element, Text):
            destroy(element)
        elif isinstance(element, Button):
            destroy(element)
    elements_list.clear()

def create_menu():
    global game_state, menu_elements
    
    clear_elements(menu_elements)
    
    # Фон
    bg = Entity(model='quad', scale=(20, 12), color=color.rgb(30, 30, 50), z=1)
    menu_elements.append(bg)
    
    # Заголовок
    title = Text(
        "PYGENICS",
        position=(0, 0.35),
        scale=3,
        color=color.gold,
        origin=(0, 0)
    )
    menu_elements.append(title)
    
    # Подзаголовок
    subtitle = Text(
        "Выберите своего кота",
        position=(0, 0.25),
        scale=1.5,
        color=color.white,
        origin=(0, 0)
    )
    menu_elements.append(subtitle)
    
    # Создание кнопок для каждого кота
    for i, cat in enumerate(cats):
        x_pos = -3 + i * 3
        y_pos = 0
        
        # Кнопка
        btn = Button(
            text=cat.name,
            position=(x_pos, y_pos),
            scale=(2.5, 0.8),
            color=color.rgb(100, 100, 150),
            text_color=color.white,
            text_origin=(0, 0)
        )
        
        # Статистика
        stats = Text(
            f"❤️ {cat.max_health}  ⚔️ {cat.damage}",
            position=(x_pos, y_pos - 0.3),
            scale=1,
            color=color.white,
            origin=(0, 0)
        )
        
        menu_elements.append(btn)
        menu_elements.append(stats)
        
        def select_cat(c=cat):
            global selected_cat, game_state
            selected_cat = c
            clear_elements(menu_elements)
            start_battle()
        
        btn.on_click = Func(select_cat, cat)

def start_battle():
    global game_state, current_enemy, battle_elements
    
    game_state = 'battle'
    battle_elements = []
    
    # Выбор случайного врага
    current_enemy = random.choice(enemies)
    current_enemy.health = current_enemy.max_health
    
    # Создание игрока
    selected_cat.health = selected_cat.max_health
    cat_entity = selected_cat.create_entity((-5, -1))
    battle_elements.append(cat_entity)
    
    # Создание врага
    enemy_entity = current_enemy.create_entity((5, -1))
    battle_elements.append(enemy_entity)
    
    # Текст битвы
    battle_text = Text(
        "Битва началась!",
        position=(0, 0.4),
        scale=1.5,
        color=color.yellow,
        origin=(0, 0)
    )
    battle_elements.append(battle_text)
    
    # Имена персонажей
    cat_name = Text(
        selected_cat.name,
        position=(-0.6, 0.25),
        scale=1.2,
        color=color.white,
        origin=(0, 0)
    )
    enemy_name = Text(
        current_enemy.name,
        position=(0.4, 0.25),
        scale=1.2,
        color=color.orange,
        origin=(0, 0)
    )
    battle_elements.append(cat_name)
    battle_elements.append(enemy_name)
    
    # Здоровье игрока
    cat_health = Text(
        f"❤️ {selected_cat.health}/{selected_cat.max_health}",
        position=(-0.6, 0.15),
        scale=1,
        color=color.red,
        origin=(0, 0)
    )
    selected_cat.health_text = cat_health
    battle_elements.append(cat_health)
    
    # Здоровье врага
    enemy_health = Text(
        f"❤️ {current_enemy.health}/{current_enemy.max_health}",
        position=(0.4, 0.15),
        scale=1,
        color=color.orange,
        origin=(0, 0)
    )
    current_enemy.health_text = enemy_health
    battle_elements.append(enemy_health)
    
    # Кнопки действий
    actions = [
        ("Обычная атака", "basic"),
        ("Царапка", "scratch"),
        ("Лечение", "heal")
    ]
    
    action_buttons = []
    for i, (action_name, action_type) in enumerate(actions):
        btn = Button(
            text=action_name,
            position=(-0.5 + i * 0.5, -0.45),
            scale=(0.45, 0.12),
            color=color.rgb(80, 80, 120),
            text_color=color.white,
            text_origin=(0, 0)
        )
        
        def make_action(a_type=action_type):
            return lambda: player_action(a_type, battle_text, cat_health, enemy_health, action_buttons)
        
        btn.on_click = make_action()
        action_buttons.append(btn)
        battle_elements.append(btn)
    
    def player_action(action_type, battle_txt, cat_hp, enemy_hp, btns):
        if game_state != 'battle' or selected_cat.health <= 0 or current_enemy.health <= 0:
            return
        
        # Отключаем кнопки на время хода
        for btn in btns:
            btn.enabled = False
        
        damage = 0
        is_dead = False
        action_message = ""
        
        if action_type == "basic":
            damage, is_dead = selected_cat.attack(current_enemy)
            action_message = f"{selected_cat.name} наносит {damage} урона!"
            enemy_hp.text = f"❤️ {current_enemy.health}/{current_enemy.max_health}"
            
        elif action_type == "scratch":
            damage = random.randint(selected_cat.damage, selected_cat.damage + 5)
            is_dead = current_enemy.take_damage(damage)
            action_message = f"{selected_cat.name} царапает! {damage} урона!"
            enemy_hp.text = f"❤️ {current_enemy.health}/{current_enemy.max_health}"
            
        elif action_type == "heal":
            heal_amount = random.randint(10, 20)
            selected_cat.heal(heal_amount)
            action_message = f"{selected_cat.name} лечится на {heal_amount} ❤️"
            cat_hp.text = f"❤️ {selected_cat.health}/{selected_cat.max_health}"
        
        battle_txt.text = action_message
        battle_txt.color = color.white
        
        # Анимация урона
        if action_type != "heal":
            current_enemy.entity.color = color.red
            invoke(lambda: setattr(current_enemy.entity, 'color', current_enemy.color), delay=0.2)
        
        # Проверка смерти врага
        if is_dead:
            battle_txt.text = f"Победа! {current_enemy.name} повержен!"
            battle_txt.color = color.green
            end_battle(True, battle_txt, btns)
            return
        
        # Ход врага
        invoke(lambda: enemy_turn(battle_txt, cat_hp, enemy_hp, btns), delay=1)
    
    def enemy_turn(battle_txt, cat_hp, enemy_hp, btns):
        if game_state != 'battle' or selected_cat.health <= 0:
            for btn in btns:
                if btn and btn.enabled == False:
                    btn.enabled = True
            return
        
        damage, is_dead = current_enemy.attack(selected_cat)
        battle_txt.text = f"{current_enemy.name} атакует! {damage} урона!"
        battle_txt.color = color.red
        
        # Анимация урона
        selected_cat.entity.color = color.red
        invoke(lambda: setattr(selected_cat.entity, 'color', selected_cat.color), delay=0.2)
        
        cat_hp.text = f"❤️ {selected_cat.health}/{selected_cat.max_health}"
        
        if is_dead:
            battle_txt.text = f"Поражение... {selected_cat.name} пал в бою"
            end_battle(False, battle_txt, btns)
        else:
            # Включаем кнопки обратно
            for btn in btns:
                btn.enabled = True
    
    def end_battle(victory, battle_txt, btns):
        global game_state
        game_state = 'result'
        
        # Отключаем все кнопки
        for btn in btns:
            btn.enabled = False
        
        # Кнопка возврата в меню
        menu_btn = Button(
            text="Вернуться в меню",
            position=(0, -0.55),
            scale=(0.8, 0.15),
            color=color.green if victory else color.red,
            text_color=color.white,
            text_origin=(0, 0)
        )
        
        def back_to_menu():
            clear_elements(battle_elements)
            destroy(menu_btn)
            create_menu()
        
        menu_btn.on_click = back_to_menu
        battle_elements.append(menu_btn)

# Запуск игры
def update():
    pass

create_menu()
app.run()