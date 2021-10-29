from .Ball import Ball

from math import hypot, acos, sin, cos


class AttackingBall(Ball):
    def __init__(self,
                 rectangle: tuple[float, float, float, float],
                 cors: tuple[float, float],
                 velocity: tuple[float, float],
                 radius: float,
                 color: tuple[int, int, int],
                 target):
        super().__init__(rectangle, cors, velocity, radius, color)
        self.target = target
        self.acceleration = 1000

    def accelerate_to_target(self, dt):
        relative_velocity = (
            self.target.velocity['x'] - self.velocity['x'],
            self.target.velocity['y'] - self.velocity['y'],
        )
        distance = (
            self.target.coordinates['x'] - self.coordinates['x'],
            self.target.coordinates['y'] - self.coordinates['y']
        )
        if hypot(*relative_velocity) < 200:
            scale = self.acceleration / hypot(*distance)
            acceleration_projection = (
                distance[0] * scale,
                distance[1] * scale
            )
        else:
            scale = 1 / hypot(*relative_velocity)

            relative_velocity_direction = (
                relative_velocity[0] * scale,
                relative_velocity[1] * scale
            )
            scale = 1 / hypot(*distance)

            distance_direction = (
                distance[0] * scale,
                distance[1] * scale
            )

            acceleration_direction = (
                distance_direction[0] + relative_velocity_direction[0],
                distance_direction[1] + relative_velocity_direction[1]
            )

            # velocity_direction = (
            #     relative_velocity_direction[0]
            # )
            scale = self.acceleration / hypot(*acceleration_direction)
            acceleration_projection = (
                acceleration_direction[0] * scale,
                acceleration_direction[1] * scale
            )
        self.velocity['x'] += acceleration_projection[0] * dt
        self.velocity['y'] += acceleration_projection[1] * dt

    def move(self, dt):
        self.accelerate_to_target(dt)
        super().move(dt)

    def is_alive(self) -> bool:
        return self.target.is_alive()
