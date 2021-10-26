import pygame


class GameOverScreen:
    CENTER, RIGHT, LEFT = range(3)

    def __init__(self, config, leaderboard, score):
        pygame.init()
        self.config = config
        self.screen = pygame.display.set_mode(config.DIMENTIONS)
        self.clock = pygame.time.Clock()
        self.leaderboard = leaderboard
        self.score = score

        # font =
        self.font_renderer = pygame.font.SysFont("", 50)

    def render_text(self, text, position=None, align=None):
        rendered_text = self.font_renderer.render(text, True, (255, 255, 255))
        width, height = self.font_renderer.size(text)
        if position is None:
            position = self.config.DIMENTIONS[0] / 2, self.config.DIMENTIONS[1] / 2
        if align is None:
            align = GameOverScreen.CENTER

        if align == GameOverScreen.CENTER:
            self.screen.blit(rendered_text, (position[0] - width / 2, position[1] - height / 2))
        elif align == GameOverScreen.LEFT:
            self.screen.blit(rendered_text, (position[0], position[1]))

    def show_screen(self):
        finished = False
        name = ''
        while not finished:
            self.clock.tick(self.config.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if event.key == pygame.K_RETURN:
                            finished = True
                        elif event.unicode not in ':':
                            name += event.unicode
            pygame.display.update()
            self.screen.fill('BLACK')
            self.render_text('Enter your name and press enter',
                             position=(0, self.config.DIMENTIONS[1] / 3),
                             align=GameOverScreen.LEFT)

            self.render_text('name: ' + name,
                             position=(self.config.DIMENTIONS[0] / 5, self.config.DIMENTIONS[1] / 2),
                             align=GameOverScreen.LEFT)
        finished = False
        self.leaderboard.add_record(name, self.score)

        while not finished:
            self.clock.tick(self.config.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    finished = True
            pygame.display.update()
            self.screen.fill('BLACK')
            self.render_text('Leaders:',
                             position=(0, 0),
                             align=GameOverScreen.LEFT
                             )

            for i in range(min(10, len(self.leaderboard.data))):
                name, rating = self.leaderboard.data[i]
                self.render_text('{i}. {name}: {rating}'.format(i=i+1, name=name, rating=rating),
                                 position=(10, (i + 1) * 50),
                                 align=GameOverScreen.LEFT
                                 )

        pygame.quit()
        return name
