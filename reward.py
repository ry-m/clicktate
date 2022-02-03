import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface


SIZE = 24


class Reward(Sprite):
    def __init__(self, pos: tuple[float, float]):
        super(Reward, self).__init__()
        self.image = pygame.image.load('resources/reward.png')
        self.image = pygame.transform.smoothscale(self.image, (SIZE, SIZE))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)
