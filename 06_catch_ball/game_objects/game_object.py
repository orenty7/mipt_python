from abc import ABC, abstractmethod


class GameObject(ABC):

    @abstractmethod
    def is_point_in_object(self, point):
        """Попадает ли точка внутрь объекта"""

    @abstractmethod
    def is_inside_box(self):
        """Попадает ли объект внутрь игровой области"""

    @abstractmethod
    def reflect(self):
        """Отражение объекта от стенок"""

    @abstractmethod
    def move(self, dt):
        """Двигает игровой объект"""

    @abstractmethod
    def draw(self, screen):
        """Рисует объект на экране"""
