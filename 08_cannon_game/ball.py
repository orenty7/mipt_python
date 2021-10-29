from random import choice
from math import hypot
import pygame

from colors import *


class Ball:
    MIN_SPEED = 5
    GRAVITY = 300
    RESISTANCE = 0.3
    REFLECT_COEFFICIENT = 0.5

    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self, dt):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.y <= 500:
            self.vy -= Ball.GRAVITY * dt
            self.y -= self.vy * dt
            self.x += self.vx * dt
            self.vx -= Ball.RESISTANCE * self.vx * dt
        else:
            if hypot(self.vx, self.vy) < Ball.MIN_SPEED:
                self.live = False
            else:
                self.vy = abs(self.vy) * Ball.REFLECT_COEFFICIENT
                self.vx = self.vx * Ball.REFLECT_COEFFICIENT
                self.y = 500
        if self.x > 780:
            self.vx = -abs(self.vx) * Ball.REFLECT_COEFFICIENT
            self.x = 780

    def draw(self):
        """Отрисовывает мяч на экране"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if abs(obj.x - self.x) <= (self.r + obj.r) and abs(obj.y - self.y) <= (self.r + obj.r):
            return True
        else:
            return False
