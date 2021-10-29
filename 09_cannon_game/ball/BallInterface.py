from ..target import TargetInterface

from abc import ABC, abstractmethod
import pygame


class BallInterface(ABC):
    @abstractmethod
    def move(self, dt: float) -> None:
        """Двигает шарик в соответствии с типом шарика"""

    @abstractmethod
    def is_alive(self) -> bool:
        """Нужно ли удалять шарик"""

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Рисует шарик на экране"""

    @abstractmethod
    def is_hit(self, target: TargetInterface) -> bool:
        """Попадает ли шарик в мишень"""

    @abstractmethod
    def cors(self) -> tuple[float, float]:
        """Возвращает координаты шарика"""

    @abstractmethod
    def radius(self) -> float:
        """Возвращает радиус шарика"""

