from .Target import Target


class StaticTarget(Target):
    def __init__(self,
                 rectangle: tuple[float, float, float, float],
                 cors: tuple[float, float],
                 radius: float,
                 ):
        super().__init__(rectangle, cors, (0, 0), radius, )
