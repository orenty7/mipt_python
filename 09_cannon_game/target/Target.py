from ball.Ball import Ball
from config import CONFIG

import pygame


class Target(Ball):
    def __init__(self,
                 rectangle: tuple[float, float, float, float],
                 cors: tuple[float, float],
                 velocity: tuple[float, float],
                 radius: float,
                 ):
        super().__init__(rectangle, cors, velocity, radius, None)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, 'red', self.cors(), self.radius)
        pygame.draw.circle(screen, 'black', self.cors(), self.radius, 1)
