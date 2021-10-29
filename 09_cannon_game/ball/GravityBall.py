from .LinearBall import LinearBall
from config import CONFIG


class GravityBall(LinearBall):
    def move(self, dt):
        super().move(dt)
        self.velocity['y'] += CONFIG['gravity'] * dt
