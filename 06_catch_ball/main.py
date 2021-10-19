import pygame
from game_objects.circle import Circle
from game_objects.square import Square
from random import randint
from colors import *
from subclasses import Range, Cors
from game import Game

pygame.init()

class Config:
    DIMENTIONS = (1200, 900)
    FPS = 120
    OBJECT_COUNT = 10

    objects = [
        {'class': Circle, 'points': 1, 'velocity_range':  Range(40, 100), 'size_range':  Range(20, 60)},
        {'class': Square, 'points': 2, 'velocity_range':  Range(40, 100), 'size_range':  Range(20, 60)},
    ]


game = Game(Config())
game.play()


