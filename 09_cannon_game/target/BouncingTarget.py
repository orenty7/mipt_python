import pygame

from TargetInterface import TargetInterface
from ..ball import BallInterface
from ..config import CONFIG


class BouncingTarget(TargetInterface):

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

    def move(self, dt: float) -> None:

        self.coordinates['x'] += self.velocity['x'] * dt
        self.coordinates['y'] += self.velocity['y'] * dt
        self.velocity['y'] += CONFIG['gravity'] * dt

        if self.coordinates['x'] - self.radius < self.rectangle['x_min']:
            self.velocity['x'] = abs(self.velocity['x'])

        if self.coordinates['x'] + self.radius > self.rectangle['x_max']:
            self.velocity['x'] = -abs(self.velocity['x'])

        if self.coordinates['y'] - self.radius < self.rectangle['y_min']:
            self.velocity['y'] = abs(self.velocity['y'])

        if self.coordinates['y'] + self.radius > self.rectangle['y_max']:
            self.velocity['y'] = -abs(self.velocity['y'])

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, 'red', self.cors(), self.radius)
        pygame.draw.circle(screen, 'black', self.cors(), self.radius, 1)


    def cors(self):
        return self.coordinates['x'], self.coordinates['y']

    def is_alive(self) -> bool:
        return True
