from game_objects.circle import Circle
from game_objects.square import Square
from subclasses import Range
from game import Game
from game_over_screen import GameOverScreen
from leaderboard import Leaderboard


class Config:
    DIMENTIONS = (1200, 900)
    FPS = 120
    OBJECT_COUNT = 10

    objects = [
        {'class': Circle, 'points': 1, 'velocity_range': Range(40, 100), 'size_range': Range(20, 60)},
        {'class': Circle, 'points': 5, 'velocity_range': Range(70, 100), 'size_range': Range(20, 40)},
        {'class': Square, 'points': 2, 'velocity_range': Range(40, 100), 'size_range': Range(20, 60)},
        {'class': Square, 'points': 10, 'velocity_range': Range(100, 200), 'size_range': Range(20, 60)},
    ]


game = Game(Config())
score = game.play(10)
leaderboard = Leaderboard()
game_over_screen = GameOverScreen(Config, leaderboard, score)
game_over_screen.show_screen()
leaderboard.save()

