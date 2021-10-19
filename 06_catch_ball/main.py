import pygame
from game_objects.circle import Circle
from game_objects.square import Square
from random import randint
from colors import *
from subclasses import Range, Cors

pygame.init()

dimentions = (400, 400)
FPS = 60
OBJECT_COUNT = 10

screen = pygame.display.set_mode(dimentions)
points = [(1, Circle), (2, Square)]

box = Cors(*dimentions)
velocity_range = Range(40, 100)
radius_range = Range(10, 50)
size_range = radius_range


def generate_object():
    ch = randint(0, 1)
    if ch == 0:
        return Circle(box, random_color(), velocity_range, radius_range)
    else:
        return Square(box, random_color(), velocity_range, size_range)


def tick():
    dt = 1 / FPS
    for gameobject in gameobjects:
        gameobject.move(dt)


def factory():
    global gameobjects
    for i in range(OBJECT_COUNT):
        gameobjects.append(generate_object())


def sort_game_objects():
    global gameobjects

    def key(gameobject):
        if type(gameobject) is Circle:
            return gameobject.r
        elif type(gameobject) is Square:
            return gameobject.size * 2

    gameobjects.sort(key=key, reverse=True)


def draw():
    for gameobject in gameobjects:
        gameobject.draw(screen)


def point_for_hit(gameobject):
    for (point, _type) in points:
        if type(gameobject) is _type:
            return point


def update_score_and_generate_new_objects(mouse):
    global score
    for i in range(len(gameobjects)):
        if gameobjects[i].is_point_in_object(mouse):
            score += point_for_hit(gameobjects[i])
            gameobjects[i] = generate_object()
    sort_game_objects()


def random_color():
    c = BLACK
    while sum(c) < 100:
        c = (randint(0, 255), randint(0, 255), randint(0, 255))
    return c


def print_score():
    cors = (10, 15)
    FONTSIZE = 50
    font = pygame.font.SysFont("", FONTSIZE)
    fontImage = font.render("Score: {score} ".format(score=score), True, CYAN, BLACK)
    screen.blit(fontImage, cors)


gameobjects = []
factory()
sort_game_objects()

pygame.display.update()
clock = pygame.time.Clock()
finished = False
score = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            point = Cors(*event.pos)
            update_score_and_generate_new_objects(point)

    pygame.display.update()
    screen.fill(BLACK)
    draw()
    print_score()
    tick()

pygame.quit()
