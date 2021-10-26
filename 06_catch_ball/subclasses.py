class Cors:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'x: {x}, y: {y}'.format(x=self.x, y=self.y)


class Range:
    def __init__(self, _min, _max):
        self.min = _min
        self.max = _max

    def __str__(self):
        return 'min: {m}, max: {M}'.format(m=self.min, M=self.max)
