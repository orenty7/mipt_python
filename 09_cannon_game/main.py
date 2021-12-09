from target.StaticTarget import StaticTarget
from target.BouncingTarget import BouncingTarget
from target.RoutedTarget import RoutedTarget
from target.Target import Target
from config import CONFIG
from Tank import Tank

import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(CONFIG['resolution'])

target = RoutedTarget(CONFIG['gaming rect'],
                      100,
                      20,
                      [(100, 100), (600, 100), (600, 400), (100, 400)]
                      )

balls = []
tank = Tank((0, CONFIG['resolution'][1] - 100))

dt = 1 / CONFIG['fps']
finished = False
while not finished:

    clock.tick(CONFIG['fps'])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.unicode == 'd':
                tank.start_moving(Tank.RIGHT)
            elif event.unicode == 'a':
                tank.start_moving(Tank.LEFT)
            elif event.unicode == 'w':
                tank.move_gun(Tank.UP)
            elif event.unicode == 's':
                tank.move_gun(Tank.DOWN)

            elif event.unicode == ' ':
                balls.append(tank.fire(target))
        elif event.type == pygame.KEYUP:
            if event.unicode == 'd' or event.unicode == 'a':
                tank.stop_moving()
            elif event.unicode == 'w' or event.unicode == 's':
                tank.stop_moving_gun()
    screen.fill('white')

    for ball in balls:
        if ball.is_hit(target):

            target.alive = False
            target = BouncingTarget(CONFIG['gaming rect'],
                                    (200, 100),
                                    (200, 0),
                                    20)
        if not ball.is_alive():
            balls.remove(ball)
        ball.move(dt)
        ball.draw(screen)

    target.move(dt)
    tank.move(dt)

    target.draw(screen)
    tank.draw(screen)
    pygame.display.update()
