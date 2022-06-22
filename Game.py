import math
import pygame
from pygame import font, draw, K_SPACE, K_s, K_w, KEYDOWN, display
import Menu

Menu.screen

window_size_x = 20
window_size_y = 20
cells_size = 35

WIDTH = window_size_x * cells_size + 1
HEIGHT = window_size_y * cells_size + 1
Level_of_enemy = 1

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
dark_green = (0, 100, 0)
yellow = (255, 255, 0)
pink = (139, 0, 255)

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Стреляющие Башни")
clock = pygame.time.Clock()

ARIAL_30 = font.SysFont('arial', 50)

class Button:
    def __init__(self):
        self._options = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._options.append(ARIAL_30.render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._options):
            option_rect: pygame.Rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)

run = True
def quit_game():
    global running
    running = False

def Draw_Window():
    mouse_pos = pygame.mouse.get_pos()
    pos_x = math.floor(mouse_pos[0] / cells_size) * cells_size
    pos_y = math.floor(mouse_pos[1] / cells_size) * cells_size
    pygame.draw.rect(window, dark_green, [pos_x, pos_y, cells_size, cells_size])
    for Line in range(window_size_x + 1):
        pygame.draw.line(window, green, [Line * cells_size, 0], [Line * cells_size, HEIGHT * cells_size])
    for Line in range(window_size_y + 1):
        pygame.draw.line(window, green, [0, Line * cells_size], [WIDTH, Line * cells_size])


class Tower:
    def __init__(self, x, y, size, color, damage, fire_rate, price, radius):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.damage = damage
        self.fire_rate = fire_rate
        self.fire_rate_tick = 0
        self.price = price
        self.radius = radius

    def Draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)


class Gun_Tower(Tower):
    def Attacking(self):
        a = Calculating(self.x, self.y, enemies[0].x, enemies[0].y)
        if self.fire_rate_tick <= 0 and a[2] < self.radius:
            Creating_Bullet(self.x, self.y, 3, green, 5, 20)
            self.fire_rate_tick = self.fire_rate
        else:
            self.fire_rate_tick -= 1 / 30


class Rocket_Tower(Tower):
    def Attacking(self):
        a = Calculating(self.x, self.y, enemies[0].x, enemies[0].y)
        if self.fire_rate_tick <= 0 and a[2] < self.radius:
            Creating_Bullet(self.x, self.y, 6, yellow, 20, 8)
            self.fire_rate_tick = self.fire_rate
        else:
            self.fire_rate_tick -= 1 / 30


class Laser_Tower(Tower):
    def Attacking(self):
        a = Calculating(self.x, self.y, enemies[0].x, enemies[0].y)
        if a[2] <= self.radius:
            pygame.draw.line(window, red, [self.x, self.y], [enemies[0].x, enemies[0].y])
            enemies[0].health -= 2


class Bullet:
    def __init__(self, x, y, size, color, damage, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.damage = damage
        self.speed = speed

    def Move(self, norm_vec_x, norm_vec_y):
        self.x += self.speed * norm_vec_x
        self.y += self.speed * norm_vec_y

    def Draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)


class Enemy:
    def __init__(self, x, y, Health, speed, size, color, reward):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.health = Health
        self.speed = speed
        self.point = 0
        self.reward = reward

    def Draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)

    def Move(self):
        a = Calculating(self.x, self.y, enemy_points[self.point][0], enemy_points[self.point][1])
        self.x += self.speed * a[0]
        self.y += self.speed * a[1]
        if a[2] <= self.speed:
            self.point += 1
            if self.point == len(enemy_points):
                enemies.remove(self)
                player.health -= 1


class Player:
    def __init__(self, Money, Health):
        self.money = Money
        self.health = Health


Map = [
    [0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 6, 1, 1, 1, 1, 5, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 11, 1, 1, 1, 1, 12, 0, 0, 0, 0, 7, 1, 1, 1, 1, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

enemy_way = []
enemy_points = []
towers = []
enemies = []
bullets = []


def Create_enemy_way():
    for i in range(len(Map)):
        for j in range(len(Map[0])):
            if Map[i][j] != 0:
                enemy_way.append([j * cells_size, i * cells_size, cells_size, cells_size])


def Create_enemy_points(points_count):
    point = 2
    for k in range(points_count):
        for i in range(len(Map)):
            for j in range(len(Map[0])):
                if Map[i][j] == point:
                    enemy_points.append([j * cells_size + cells_size / 2, i * cells_size + cells_size / 2])
                    point += 1


def Draw_Enemy_way(color):
    for way in enemy_way:
        pygame.draw.rect(window, color, way)


def Creating_Tower():
    mouse_pos = pygame.mouse.get_pos()
    pos_x = math.floor(mouse_pos[0] / cells_size) * cells_size
    pos_y = math.floor(mouse_pos[1] / cells_size) * cells_size
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1] and Checking_Towers_Building(pos_x, pos_y) and player.money - 10 >= 0:
        towers.append(Gun_Tower(pos_x + cells_size / 2, pos_y + cells_size / 2, 10, green, 5, 0.5, 10, 150))
        player.money -= 10
    if keys[pygame.K_2] and Checking_Towers_Building(pos_x, pos_y) and player.money - 15 >= 0:
        towers.append(Rocket_Tower(pos_x + cells_size / 2, pos_y + cells_size / 2, 10, yellow, 5, 3, 15, 400))
        player.money -= 15
    if keys[pygame.K_3] and Checking_Towers_Building(pos_x, pos_y) and player.money - 20 >= 0:
        towers.append(Laser_Tower(pos_x + cells_size / 2, pos_y + cells_size / 2, 10, red, 5, 3, 20, 100))
        player.money -= 20


def Creating_Enemy(heal, speed, size, color, reward):
    for i in range(10):
        x = enemy_points[0][0] - 200 - i * 20 - 5
        y = enemy_points[0][1]
        enemies.append(Enemy(x, y, heal, speed, size, color, reward))


def Creating_Bullet(x, y, size, color, damage, speed):
    bullets.append(Bullet(x, y, size, color, damage, speed))


def Checking_Towers_Building(x, y):
    x += cells_size / 2
    y += cells_size / 2
    if len(towers) > 0:
        for tower in towers:
            if tower.x == x and tower.y == y:
                return False
    for way in enemy_way:
        if way[0] + cells_size / 2 == x and way[1] + cells_size / 2 == y:
            return False
    return True

def Checking_enemy_death():
    global Level_of_enemy
    for enemy in enemies:
        if enemy.health <= 0:
            enemies.remove(enemy)
            player.money += enemy.reward
    if len(enemies) == 0:
        Level_of_enemy += 1
        Creating_Enemy(100 * Level_of_enemy, 2 + Level_of_enemy / 10, 10, pink, 10 * Level_of_enemy)

def Checking_player_death():

     if player.health <= 0:
        pygame.display.set_caption("Конец игры!")
        window = pygame.display.set_mode((800, 600))
        window.fill((0, 0, 0))
        text1 = f2.render('Конец игры!', 1, (180, 0, 0))
        window.blit(text1, (300, 125))
        schet = f2.render("Вы смогли набрать очков:", False, yellow)
        window.blit(schet, (220, 175))
        window.blit(money, (375, 225))
        button.draw(window, 330, 300, 55)
        button.append_option('Закончить', exit)
        pygame.display.update()

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    button.select()

            button.draw(window, 315, 300, 45)

            display.flip()

def Calculating(x1, y1, x2, y2):
    vec_x = x2 - x1
    vec_y = y2 - y1
    dist = math.sqrt(vec_x ** 2 + vec_y ** 2)
    norm_vec_x = vec_x / dist
    norm_vec_y = vec_y / dist
    angle = math.atan2(norm_vec_y, norm_vec_x)
    return norm_vec_x, norm_vec_y, dist, angle


def Main():
    Draw_Window()
    Draw_Enemy_way(dark_green)
    Creating_Tower()
    for tower in towers:
        tower.Draw()
        tower.Attacking()
    for enemy in enemies:
        enemy.Move()
        enemy.Draw()
    Checking_enemy_death()
    for bullet in bullets:
        a = Calculating(bullet.x, bullet.y, enemies[0].x, enemies[0].y)
        bullet.Move(a[0], a[1])
        if a[2] <= bullet.speed:
            enemies[0].health -= bullet.damage
            bullets.remove(bullet)
        bullet.Draw()
    Checking_enemy_death()
    Checking_player_death()


f2 = pygame.font.SysFont('serif', 36)

Create_enemy_way()
Create_enemy_points(10)
Creating_Enemy(100, 3, 10, pink, 10)
player = Player(100, 10)

button = Button()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_w:
                button.switch(-1)
            elif event.key == K_s:
                button.switch(1)
            elif event.key == K_SPACE:
                button.select()


    window.fill(black)
    Main()
    monet = f2.render("Монеты:", False, yellow, black)
    window.blit(monet, (0, 0))
    lives = f2.render("Здоровье:", False, red, black)
    window.blit(lives, (520, 0))
    money = f2.render(str(player.money), False, yellow, black)
    health = f2.render(str(player.health), False, red, black)
    window.blit(money, (131, 0))
    window.blit(health, (665, 0))

    pygame.display.update()
    clock.tick(30)

pygame.quit()

