import math
from random import choice, randint
from time import time

rnd = randint

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.y <= 500:
            self.vy -= 1.2
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99
        else:
            if self.vx ** 2 + self.vy ** 2 > 10:
                self.vy = -self.vy / 2
                self.vx = self.vx / 2
                self.y = 499
            if self.live < 0:
                balls.pop(balls.index(self))
            else:
                self.live -= 1
        if self.x > 780:
            self.vx = -self.vx / 2
            self.x = 779

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if abs(obj.x - self.x) <= (self.r + obj.r) and abs(obj.y - self.y) <= (self.r + obj.r):
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, counter
        counter += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event is not None:
            if event.pos[0] != 20:
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # image = pygame.Surface((60, 15))
        # image.fill(WHITE)
        # pygame.draw.rect(image, self.color, ((1, 1), (60, 15)))
        #
        # pygame.draw.rect(image, BLUE, (20, 5, 20, 5))
        # new_image = pygame.transform.rotate(image, -math.degrees(self.an))
        # screen.blit(new_image, (20, 430))
        # # FIXIT don't know how to do it
        width = 10
        rect = ((20, 450),
                (20 + max(self.f2_power, 20) * math.cos(self.an),
                 450 + max(self.f2_power, 20) * math.sin(self.an)),
                (20 + (max(self.f2_power, 20)) * math.cos(self.an) - width * math.sin(self.an),
                 450 + (max(self.f2_power, 20) * math.sin(self.an) + width * math.cos(self.an))),
                (20 - width * math.sin(self.an),
                 450 + width * math.cos(self.an)))
        pygame.draw.polygon(self.screen, self.color, rect)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = RED

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r, 1
        )


def draw():
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    if in_new_game_offset():
        screen.blit(counter_image, (10, 15))
    pygame.display.update()


def process_events(events):
    global finished
    for event in events:
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)


def create_text(counter):
    text = 'Вы уничтожили цель за ' + str(counter) + ' выстрел'
    if 10 <= counter <= 20 or counter % 10 >= 5:
        return text + 'ов'
    elif counter % 10 == 1:
        return text
    else:
        return text + 'а'


def render_counter(counter):
    font = pygame.font.SysFont('', 50)
    return font.render(create_text(counter), True, BLACK, WHITE)


def in_new_game_offset():
    return time() - start_time < 2


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

gun = Gun(screen)
target = Target(screen)
finished = False
new_game = False
counter = 0
balls = []
start_time = 0
while not finished:
    if new_game:
        start_time = time()
        new_game = False
        counter = 0

    clock.tick(FPS)
    draw()
    process_events(pygame.event.get())

    for b in balls:
        b.move()
        if b.hittest(target) and not in_new_game_offset():
            target.hit()
            target.new_target()
            new_game = True
            counter_image = render_counter(counter)

    gun.power_up()

pygame.quit()
