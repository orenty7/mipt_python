from BallInterface import BallInterface

from random import random
from math import sin, cos
import pygame


def random_between(min_: float, max_: float) -> float:
    return min_ + random() * (max_ - min_)


class LinearBall(BallInterface):
    def __init__(self,
                 rectangle: tuple[float, float, float, float],
                 cors: tuple[float, float],
                 velocity: tuple[float, float],
                 radius: float,
                 color: tuple[int, int, int]
                 ):
        self.color = color
        self.radius = radius

        self.rectangle = {
            'x_min': rectangle[0],
            'y_min': rectangle[1],
            'x_max': rectangle[2],
            'y_max': rectangle[3]
        }

        self.coordinates = {
            'x': cors[0],
            'y': cors[1]
        }
        self.velocity = {
            'x': velocity[0],
            'y': velocity[1],
        }

        self.reflects_to_live = 30

    def move(self, dt):
        self.coordinates['x'] += self.velocity['x'] * dt
        self.coordinates['y'] += self.velocity['y'] * dt

        if self.coordinates['x'] - self.radius < self.rectangle['x_min']:
            self.velocity['x'] = abs(self.velocity['x'])
            self.reflects_to_live -= 1

        if self.coordinates['x'] + self.radius > self.rectangle['x_max']:
            self.velocity['x'] = -abs(self.velocity['x'])
            self.reflects_to_live -= 1

        if self.coordinates['y'] - self.radius < self.rectangle['y_min']:
            self.velocity['y'] = abs(self.velocity['y'])
            self.reflects_to_live -= 1

        if self.coordinates['y'] + self.radius > self.rectangle['y_max']:
            self.velocity['y'] = -abs(self.velocity['y'])
            self.reflects_to_live -= 1

        if self.reflects_to_live < 0:
            self.reflects_to_live = 0

    def cors(self) -> tuple[float, float]:
        return self.coordinates['x'], self.coordinates['y']

    def radius(self) -> float:
        return self.radius

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, self.cors(), self.radius)

    def is_alive(self) -> bool:
        return self.reflects_to_live > 0
