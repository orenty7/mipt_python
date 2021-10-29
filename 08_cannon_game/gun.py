from math import atan, atan2, sin, cos
import pygame

from colors import *
from ball import Ball


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        """Включает заряд пушки """
        self.f2_on = 1

    def fire2_end(self, event, balls):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * 20 * cos(self.an)
        new_ball.vy = - self.f2_power * 20 * sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event is not None:
            if event.pos[0] != 20:
                self.an = atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Рисует пушку на экране"""
        width = 10
        rect = ((20, 450),
                (20 + max(self.f2_power, 20) * cos(self.an),
                 450 + max(self.f2_power, 20) * sin(self.an)),
                (20 + (max(self.f2_power, 20)) * cos(self.an) - width * sin(self.an),
                 450 + (max(self.f2_power, 20) * sin(self.an) + width * cos(self.an))),
                (20 - width * sin(self.an),
                 450 + width * cos(self.an)))
        pygame.draw.polygon(self.screen, self.color, rect)

    def power_up(self):
        """Отслеживает силу заряда пушки"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
