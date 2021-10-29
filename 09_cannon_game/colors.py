from random import randint

def random_dark_color():
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    while sum(color) > 255*3 - 100:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
    return color