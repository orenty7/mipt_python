from .Ball import Ball


class LinearBall(Ball):
    def __init__(self,
                 rectangle: tuple[float, float, float, float],
                 cors: tuple[float, float],
                 velocity: tuple[float, float],
                 radius: float,
                 color: tuple[int, int, int],
                 reflection_to_live=10):
        super().__init__(rectangle, cors, velocity, radius, color)
        self.reflects_to_live = reflection_to_live
        self.reflecting = False

    def move(self, dt):
        super().move(dt)
        collision = super().reflect()
        if collision and not self.reflecting:
            self.reflects_to_live -= 1

        self.reflecting = collision

    def is_hit(self, target) -> bool:
        if super().is_hit(target):
            self.reflects_to_live = 0
            return True
        return False

    def is_alive(self) -> bool:
        return self.reflects_to_live > 0
