import pygame
from pygame.draw import *
from math import sin, cos, radians, atan, pi


def rotate(center, point, angle=0):
    x0, y0 = center
    x, y = point
    r = ((x - x0) ** 2 + (y - y0) ** 2) ** 0.5
    phi = atan((y - y0) / (x - x0)) if x > x0 else pi + atan((y - y0) / (x - x0))
    return x0 + r * cos(phi + angle), y0 + r * sin(phi + angle)


def rotated_rect(center, dimentions, angle=0):
    x0, y0 = center
    lx, ly = dimentions
    polygon(screen, (255, 255, 0), [
        rotate(center, (x, y), angle) for (x, y) in
        [(x0 + lx, y0 + ly), (x0 + lx, y0 - ly), (x0 - lx, y0 - ly), (x0 - lx, y0 + ly)]
    ])


pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 1000))

rotated_rect((400, 400), (100, 50), radians(45))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
