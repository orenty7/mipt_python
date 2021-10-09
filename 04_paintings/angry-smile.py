import pygame
from pygame.draw import *
from math import sin, cos, radians, atan, pi

YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def rotate(center, point, angle=0):
    x0, y0 = center
    x, y = point
    r = ((x - x0) ** 2 + (y - y0) ** 2) ** 0.5
    phi = atan((y - y0) / (x - x0)) if x > x0 else pi + atan((y - y0) / (x - x0))
    return x0 + r * cos(phi + angle), y0 + r * sin(phi + angle)


def rotated_rect(center, color, dimentions, angle=0):
    x0, y0 = center
    lx, ly = dimentions
    dx = lx / 2
    dy = ly / 2
    polygon(screen, color, [
        rotate(center, (x, y), angle) for (x, y) in
        [(x0 + dx, y0 + dy), (x0 + dx, y0 - dy), (x0 - dx, y0 - dy), (x0 - dx, y0 + dy)]
    ])


def angry_smile(center, scale=1):
    x0, y0 = center

    circle(screen, YELLOW, (x0, y0), 100 * scale)
    circle(screen, BLACK, (x0, y0), 100 * scale, 1)

    rotated_rect((x0, y0 + 50 * scale), BLACK, (80 * scale, 12 * scale))

    circle(screen, RED, (x0 - 50 * scale, y0 - 20 * scale), 20 * scale)
    circle(screen, BLACK, (x0 - 50 * scale, y0 - 20 * scale), 20 * scale, 1)
    circle(screen, BLACK, (x0 - 50 * scale, y0 - 20 * scale), 8 * scale)
    rotated_rect((x0 - 50 * scale, y0 - 50 * scale), BLACK, (100 * scale, 10 * scale), radians(45))

    circle(screen, RED, (x0 + 50 * scale, y0 - 20 * scale), 17 * scale)
    circle(screen, BLACK, (x0 + 50 * scale, y0 - 20 * scale), 17 * scale, 1)
    circle(screen, BLACK, (x0 + 50 * scale, y0 - 20 * scale), 8 * scale)
    rotated_rect((x0 + 50 * scale, y0 - 50 * scale), BLACK, (100 * scale, 10 * scale), radians(-45))



pygame.init()
FPS = 30
screen = pygame.display.set_mode((400, 400))

# rotated_rect((400, 400), (100, 50), radians(60))
rotated_rect((200, 200), WHITE, (400, 400))

angry_smile((200, 200), 1.5)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()

pygame.quit()
