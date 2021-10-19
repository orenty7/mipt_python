import pygame
from random import randint, choice
from subclasses import Range, Cors
from colors import *


def random_color():
    c = (randint(0, 255), randint(0, 255), randint(0, 255))
    while sum(c) < 100:
        c = (randint(0, 255), randint(0, 255), randint(0, 255))
    return c


class Game:
    def __init__(self, config):
        pygame.init()

        self.config = config
        self.screen = pygame.display.set_mode(config.DIMENTIONS)
        self.clock = pygame.time.Clock()
        self.box = Cors(*config.DIMENTIONS)
        self.game_objects = []
        self.game_objects_factory()
        self.score = 0

    def generate_game_object(self):
        game_object_dict = choice(self.config.objects)
        return game_object_dict['class'](
            self.box,
            random_color(),
            game_object_dict['size_range'],
            game_object_dict['velocity_range']
        )

    def game_objects_factory(self):
        for i in range(self.config.OBJECT_COUNT):
            self.game_objects.append(self.generate_game_object())

    def sort_game_objects_by_size(self):
        self.game_objects.sort(key=lambda obj: obj.cmp_size(), reverse=True)

    def onclick(self, mouse):
        for i in range(len(self.game_objects)):
            if self.game_objects[i].is_point_in_object(mouse):
                self.score += self.point_for_hit(self.game_objects[i])
                self.game_objects[i] = self.generate_game_object()
        self.sort_game_objects_by_size()

    def point_for_hit(self, game_object):
        for _object in self.config.objects:
            if type(game_object) is _object['class']:
                return _object['points']

    def tick(self):
        dt = 1 / self.config.FPS
        for game_object in self.game_objects:
            game_object.move(dt)

    def render(self):
        for game_object in self.game_objects:
            game_object.draw(self.screen)

    def render_score(self):
        cors = (10, 15)
        FONTSIZE = 50
        font = pygame.font.SysFont("", FONTSIZE)
        fontImage = font.render("Score: {score} ".format(score=self.score), True, CYAN, BLACK)
        self.screen.blit(fontImage, cors)

    def play(self):
        finished = False
        while not finished:
            self.clock.tick(self.config.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = Cors(*event.pos)
                    self.onclick(point)

            pygame.display.update()
            self.screen.fill('BLACK')
            self.render()
            self.render_score()
            self.tick()

        pygame.quit()
