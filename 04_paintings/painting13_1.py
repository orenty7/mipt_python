import pygame
from pygame.draw import *
from math import sin, cos, radians, asin, pi

YELLOW = (212, 170, 0)
LIGHT_BROWN = (108, 93, 83)
BROWN = (72, 55, 55)
DARK_BROWN = (36, 28, 28)
GREEN = (44, 160, 90)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def rotate(center, point, angle=0):
    x0, y0 = center
    x, y = point
    if x == x0 and y == y0:
        return point

    r = ((x - x0) ** 2 + (y - y0) ** 2) ** 0.5
    phi = asin((y - y0) / r) if y <= y0 else pi + asin((y - y0) / r)
    return x0 + r * cos(phi + angle), y0 + r * sin(phi + angle)

def forest():
    rect(screen, YELLOW, [()])


def spikes(cors, angle=0):
    x0, y0 = cors
    return [rotate((x0, y0), (x, y), angle) for (x, y) in [(x0, y0), (x0, y0 - 100), (x0 + 10, y0),
                                                           (x0 + 10, y0), (x0 + 10, y0 - 100), (x0 + 20, y0)]]


pygame.init()
FPS = 30
screen = pygame.display.set_mode((800, 1125))

polygon(screen, DARK_BROWN, spikes((100, 100), radians(90)))

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
