from .Target import Target
from config import CONFIG

import pygame


class BouncingTarget(Target):
    def move(self, dt: float) -> None:
        super().move(dt)
        self.velocity['y'] += CONFIG['gravity'] * dt
