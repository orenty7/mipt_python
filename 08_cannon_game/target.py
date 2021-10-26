from random import randint
from colors import *
import pygame


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.vy = randint(50, 100)
        self.r = randint(5, 50)
        self.color = RED

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r, 1
        )

    def move(self, dt):
        if self.y + self.r > 500:
            self.vy = -abs(self.vy)
        elif self.y - self.r < 0:
            self.vy = abs(self.vy)
        self.y += self.vy * dt
