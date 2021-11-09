from ball import *
from config import CONFIG
from colors import *

from math import sin, cos, pi
import pygame
import random


class Tank:
    STOP, LEFT, RIGHT, UP, DOWN = \
        "STOP, LEFT, RIGHT, UP, DOWN".split(', ')

    def __init__(self, cors: tuple[float, float]):
        self.coordinates = {
            'x': cors[0],
            'y': cors[1]
        }
        self.velocity = {
            'x': 0,
            'y': 0
        }
        self.move_direction = Tank.STOP
        self.gun_angle = pi / 2
        self.angular_velocity = 0

    def start_moving(self, direction) -> None:
        self.move_direction = direction
        if direction == Tank.RIGHT:
            self.velocity['x'] = 100
        elif direction == Tank.LEFT:
            self.velocity['x'] = -100

    def move_gun(self, direction):
        if direction == Tank.UP:
            self.angular_velocity = -10
        elif direction == Tank.DOWN:
            self.angular_velocity = 10

    def stop_moving_gun(self):
        self.angular_velocity = 0

    def stop_moving(self) -> None:
        self.velocity['x'] = 0

    def move(self, dt: float) -> None:
        self.coordinates['x'] += self.velocity['x'] * dt
        self.gun_angle += self.angular_velocity * dt
        if self.gun_angle > 2 * pi:
            self.gun_angle = 2 * pi
        elif self.gun_angle < pi:
            self.gun_angle = pi

    def fire(self, target):
        gun_x, gun_y = self.coordinates['x'] + 50 + 50*cos(self.gun_angle), self.coordinates['y'] + 50*sin(self.gun_angle)- 10

        v = random.randint(500, 1000)
        phi = self.gun_angle
        return AttackingBall(CONFIG['gaming rect'], (gun_x, gun_y), (v * cos(phi) + self.velocity['x'], v * sin(phi)), 20, random_dark_color(), target)

    def cors(self):
        return self.coordinates['x'], self.coordinates['y']

    def draw(self, screen: pygame.Surface) -> None:
        gun_x, gun_y = self.coordinates['x'] + 50, self.coordinates['y'] - 10
        gun_rect = (
            (gun_x, gun_y),
            (gun_x + 100 * cos(self.gun_angle), gun_y + 100 * sin(self.gun_angle)),

            (gun_x + 100 * cos(self.gun_angle) + 10 * sin(self.gun_angle),
             gun_y + 100 * sin(self.gun_angle) - 10 * cos(self.gun_angle)),

            (gun_x + 10 * sin(self.gun_angle),
             gun_y - 10 * cos(self.gun_angle)),
            (gun_x, gun_y))

        pygame.draw.polygon(screen, 'red', gun_rect)
        pygame.draw.rect(screen, 'gray', (self.coordinates['x'], self.coordinates['y'] - 20, 100, 20))
