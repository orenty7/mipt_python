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


pygame.init()
FPS = 30
screen = pygame.display.set_mode((400, 400))

# rotated_rect((400, 400), (100, 50), radians(60))
rotated_rect((200, 200), WHITE, (400, 400))

circle(screen, YELLOW, (200, 200), 100)
circle(screen, BLACK, (200, 200), 100, 1)

rotated_rect((200, 250), BLACK, (80, 12))

circle(screen, RED, (150, 180), 20)
circle(screen, BLACK, (150, 180), 20, 1)
circle(screen, BLACK, (150, 180), 8)
rotated_rect((150, 150), BLACK, (100, 10), radians(45))



circle(screen, RED, (250, 180), 17)
circle(screen, BLACK, (250, 180), 17, 1)
circle(screen, BLACK, (250, 180), 8)
rotated_rect((250, 150), BLACK, (100, 10), radians(-45))




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
