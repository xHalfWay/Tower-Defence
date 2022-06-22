from pygame import *

init()

size = (800, 600)
screen = display.set_mode(size)
ARIAL_30 = font.SysFont('arial', 50)

class Menu:
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
            option_rect: Rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)

running = True

def quit_game():
    global running
    running = False

white = (255, 255, 255)

menu = Menu()
menu.append_option('Играть', quit_game)
menu.append_option('Выход', exit)
upr1 = font.SysFont('arial', 25).render("Управление в меню:",1 , white)
upr2 = font.SysFont('arial', 20).render("«W» - Вверх ; «S» - Вниз ; «Space» - Выбрать",1 , white)
upr3 = font.SysFont('arial', 25).render("Управление в игре:",1 , white)
text = font.SysFont('arial', 20).render('Построить башню – навестись курсором мыши в пустой черный квадрат',1 , white)
text1 = font.SysFont('arial', 20).render('и нажать клавишу на клавиатуре «1», «2» или «3»;',1,white)
pravila = font.SysFont('arial', 25).render("Цель игры: ",1 , white)
pravila1 = font.SysFont('arial', 20).render('Не дать противникам достичь конца игрового поля, строя оборонные башни.', 1, white)
pravila2 = font.SysFont('arial', 20).render('Количество здоровья уменьшается на единицу за каждого прошедшего противника.', 1, white)
pravila3 = font.SysFont('arial',20).render('Игра завершается тогда, когда у игрока закончилось здоровье.',1,white)
while running:
    for e in event.get():
        if e.type == QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_w:
                menu.switch(-1)
            elif e.key == K_s:
                menu.switch(1)
            elif e.key == K_SPACE:
                menu.select()

    screen.fill((0, 0, 0))
    display.set_caption("Меню игры")
    menu.draw(screen, 330, 200, 75)
    screen.blit(pravila, (5,495))
    screen.blit(pravila1, (5, 525))
    screen.blit(pravila2, (5, 550))
    screen.blit(pravila3, (5, 575))
    screen.blit(text, (5, 435))
    screen.blit(text1, (5, 455))
    screen.blit(upr1, (5,350))
    screen.blit(upr2, (5, 380))
    screen.blit(upr3, (5, 405))

    display.flip()

