from game_objects.game_object import GameObject
from random import random
from math import pi, sin, cos, hypot
from pygame.draw import circle


def _random(_min, _max):
    return _min + random() * (_max - _min)


class Circle(GameObject):

    def __init__(self, box, color, radius_range, velocity_range):
        self.box = box
        self.color = color

        self.r = _random(radius_range.min, radius_range.max)

        v = _random(velocity_range.min, velocity_range.max)
        phi = random() * 2 * pi
        self.vx = v * cos(phi)
        self.vy = v * sin(phi)

        self.x = _random(self.r, box.x - self.r)
        self.y = _random(self.r, box.y - self.r)

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if not self.is_inside_box():
            self.reflect()

    def is_inside_box(self, box=None):
        if box is None:
            box = self.box

        if self.x - self.r < 0 or self.x + self.r > box.x:
            return False
        if self.y - self.r < 0 or self.y + self.r > box.y:
            return False
        return True

    def reflect(self, box=None):
        if self.is_inside_box(box):
            return

        if box is None:
            box = self.box

        if self.x - self.r < 0:
            self.vx = abs(self.vx)
        elif self.x + self.r > box.x:
            self.vx = -abs(self.vx)

        if self.y - self.r < 0:
            self.vy = abs(self.vy)
        elif self.y + self.r > box.y:
            self.vy = -abs(self.vy)

    def is_point_in_object(self, point):
        return hypot(self.x - point.x, self.y - point.y) <= self.r

    def draw(self, surface):
        circle(surface, self.color, (self.x, self.y), self.r)

    def cmp_size(self):
        return self.r
