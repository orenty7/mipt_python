from colors import *
from random import randint
from time import time
import pygame

from target import Target
from gun import Gun

rnd = randint

FPS = 30

WIDTH = 800
HEIGHT = 600




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
    global finished, counter
    for event in events:
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event, balls)
            counter += 1
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
dt = 1 / FPS
while not finished:
    if new_game:
        start_time = time()
        new_game = False
        counter = 0

    clock.tick(FPS)
    draw()
    process_events(pygame.event.get())
    if not in_new_game_offset():
        target.move(dt)
    for b in balls:
        b.move(dt)
        if b.live <= 0:
            balls.remove(b)
        if b.hittest(target) and not in_new_game_offset():
            target.hit()
            target.new_target()
            new_game = True
            counter_image = render_counter(counter)

    gun.power_up()

pygame.quit()
