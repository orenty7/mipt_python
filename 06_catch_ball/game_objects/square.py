from game_objects.game_object import GameObject
from random import random
from math import pi, sin, cos, hypot
from pygame.draw import rect


def _random(_min, _max):
    return _min + random() * (_max - _min)


class Square(GameObject):

    def __init__(self, box, color, size_range, velocity_range):
        self.box = box
        self.color = color

        self.size = _random(size_range.min, size_range.max)

        v = _random(velocity_range.min, velocity_range.max)
        phi = random() * 2 * pi
        self.vx = v * cos(phi)
        self.vy = v * sin(phi)

        self.x = _random(self.size, box.x - self.size)
        self.y = _random(self.size, box.y - self.size)

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if not self.is_inside_box():
            self.reflect()

    def is_inside_box(self, box=None):
        if box is None:
            box = self.box

        if self.x - self.size < 0 or self.x + self.size > box.x:
            return False
        if self.y - self.size < 0 or self.y + self.size > box.y:
            return False
        return True

    def reflect(self, box=None):
        if self.is_inside_box(box):
            return

        if box is None:
            box = self.box

        if self.x - self.size < 0:
            self.vx = abs(self.vx)
        elif self.x + self.size > box.x:
            self.vx = -abs(self.vx)

        if self.y - self.size < 0:
            self.vy = abs(self.vy)
        elif self.y + self.size > box.y:
            self.vy = -abs(self.vy)

    def is_point_in_object(self, point):
        return abs(self.x - point.x) <= self.size and abs(self.y - point.y) <= self.size

    def draw(self, surface):
        rect(surface, self.color, (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2))

    def cmp_size(self):
        return self.size
