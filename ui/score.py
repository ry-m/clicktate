import pygame
from pygame.surface import Surface

BAR_HEIGHT = 60
FONT_SIZE = 16
TEXT_COLOUR = (50, 110, 80, 0)


class Score:
    def __init__(self, screen_w: int):
        pygame.font.init()
        self.width = screen_w
        self.score = 0
        self.best = 0
        self.font_lt = pygame.font.Font('resources/font/Comfortaa-Light.ttf', FONT_SIZE)
        self.font_bold = pygame.font.Font('resources/font/Comfortaa-Bold.ttf', FONT_SIZE)
        self.score_text = self.font_lt.render('SCORE:', True, TEXT_COLOUR)
        self.best_text = self.font_lt.render('BEST:', True, TEXT_COLOUR)

    def update(self, i: int):
        self.score += i
        self.best = max(self.best, self.score)

    def set_to_zero(self):
        self.score = 0

    def draw(self, screen: Surface):
        bar = Surface((self.width, BAR_HEIGHT))
        bar.fill((255, 255, 255, 0))
        bar_rect = bar.get_rect(center=(self.width / 2, BAR_HEIGHT / 2))

        score_text = self.font_bold.render(f'{self.score}', True, TEXT_COLOUR)
        best_text = self.font_bold.render(f'{self.best}', True, TEXT_COLOUR)

        bar.blit(self.score_text, (10, 10))
        bar.blit(self.best_text, (10, 30))
        bar.blit(score_text, (75, 10))
        bar.blit(best_text, (60, 30))

        screen.blit(bar, bar_rect)
