from .Ball import Ball
from .LinearBall import LinearBall

from math import hypot
import pygame


class FragBall(Ball):
    def __init__(self,
                 rectangle: tuple[float, float, float, float],
                 cors: tuple[float, float],
                 velocity: tuple[float, float],
                 radius: float,
                 color: tuple[int, int, int],
                 fragmentations_to_live=3):
        super().__init__(rectangle, cors, velocity, radius, color)
        self.fragments = []
        self.fragmentations_to_live = fragmentations_to_live
        self.fragmentated = False

        self.alive = True

    def create_fragments(self):
        if self.fragmentations_to_live >= 1:
            self.fragments = [
                FragBall((self.rectangle['x_min'], self.rectangle['y_min'],
                          self.rectangle['x_max'], self.rectangle['y_max']),
                         self.cors(),
                         (self.velocity['x'] + 10, self.velocity['y'] + 10),
                         self.radius / 1.1,
                         self.color,
                         self.fragmentations_to_live - 1
                         ),
                FragBall((self.rectangle['x_min'], self.rectangle['y_min'],
                          self.rectangle['x_max'], self.rectangle['y_max']),
                         self.cors(),
                         (self.velocity['x'] - 10, self.velocity['y'] - 10),
                         self.radius / 1.1,
                         self.color,
                         self.fragmentations_to_live - 1
                         )
            ]
        else:
            self.fragments = [
                LinearBall((self.rectangle['x_min'], self.rectangle['y_min'],
                            self.rectangle['x_max'], self.rectangle['y_max']),
                           self.cors(),
                           (self.velocity['x'], self.velocity['y']),
                           self.radius,
                           self.color,
                           5)
            ]

    def move(self, dt):
        if not self.fragmentated:
            super().move(dt)
            if super().reflect():
                self.create_fragments();
                self.fragmentated = True
        else:
            for fragment in self.fragments:
                fragment.move(dt)
                if not fragment.is_alive():
                    self.fragments.remove(fragment)

            if len(self.fragments) == 0:
                self.alive = False

    def is_hit(self, target) -> bool:
        if not self.fragmentated:
            res = hypot(self.cors()[0] - target.cors()[0],
                        self.cors()[1] - target.cors()[1]) < self.radius + target.radius
            if res:
                self.alive = False
            return res
        else:
            for fragment in self.fragments:
                if fragment.is_hit(target):
                    return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        if not self.fragmentated:
            pygame.draw.circle(screen, self.color, self.cors(), self.radius)
        else:
            for fragment in self.fragments:
                fragment.draw(screen)

    def is_alive(self) -> bool:
        return self.alive
