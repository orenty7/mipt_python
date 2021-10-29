from abc import ABC, abstractmethod
import pygame


class TargetInterface(ABC):
    @abstractmethod
    def move(self, dt: float) -> None:
        """Двигает мишень в соответствии с типом мишени"""

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        """Рисует шарик на экране"""

    @abstractmethod
    def is_alive(self) -> bool:
        """Самоуничтожение некоторых типов мишеней"""
