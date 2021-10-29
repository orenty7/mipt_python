from .FragBall import FragBall
from .GravityBall import GravityBall
from config import CONFIG


class GravityFragBall(FragBall):
    def create_fragments(self):
        if self.fragmentations_to_live >= 1:
            self.fragments = [
                GravityFragBall((self.rectangle['x_min'], self.rectangle['y_min'],
                                 self.rectangle['x_max'], self.rectangle['y_max']),
                                self.cors(),
                                (self.velocity['x'] + 10, self.velocity['y'] + 10),
                                self.radius / 1.1,
                                self.color,
                                self.fragmentations_to_live - 1
                                ),
                GravityFragBall((self.rectangle['x_min'], self.rectangle['y_min'],
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
                GravityBall((self.rectangle['x_min'], self.rectangle['y_min'],
                             self.rectangle['x_max'], self.rectangle['y_max']),
                            self.cors(),
                            (self.velocity['x'], self.velocity['y']),
                            self.radius,
                            self.color,
                            5)
            ]

    def move(self, dt):
        self.velocity['y'] += CONFIG['gravity'] * dt
        super().move(dt)
