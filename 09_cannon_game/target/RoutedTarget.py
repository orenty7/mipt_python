from .Target import Target

from math import hypot


class RoutedTarget(Target):
    def __init__(self,
                 rectangle: tuple[float, float, float, float],
                 velocity: float,
                 radius: float,
                 route: list[tuple[float, float]]):
        self.route = route
        self.full_velocity = velocity
        velocity_projection = [
            route[1][0] - route[0][0],
            route[1][1] - route[0][1]
        ]
        scale = velocity / hypot(*velocity_projection)
        velocity_projection = (
            velocity_projection[0] * scale,
            velocity_projection[1] * scale
        )
        super().__init__(rectangle, route[0], velocity_projection, radius)
        self.goto_point_index = 1

    def distance_to_point(self):
        return hypot(self.coordinates['x'] - self.route[self.goto_point_index][0],
                     self.coordinates['y'] - self.route[self.goto_point_index][1]
                     )

    def route_to_point(self):
        velocity_projection = [
            self.route[self.goto_point_index][0] - self.coordinates['x'],
            self.route[self.goto_point_index][1] - self.coordinates['y']
        ]
        scale = self.full_velocity / hypot(*velocity_projection)
        velocity_projection = (
            velocity_projection[0] * scale,
            velocity_projection[1] * scale
        )
        self.velocity['x'] = velocity_projection[0]
        self.velocity['y'] = velocity_projection[1]

    def move(self, dt):
        super().move(dt)
        if self.distance_to_point() < 1:
            self.goto_point_index += 1
            if self.goto_point_index == len(self.route):
                self.goto_point_index = 0
        self.route_to_point()
