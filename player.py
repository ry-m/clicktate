import pygame
from pygame.sprite import Sprite
from pygame import gfxdraw

# Player circle radius.
RADIUS = 12


class Player(Sprite):
    def __init__(self, pos: tuple[float, float]):
        super(Player, self).__init__()
        self.image = pygame.surface.Surface((RADIUS * 2, RADIUS * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, surface: pygame.Surface):
        """
        Render the player onto the surface.
        The player sprite is represented by a filled black circle.
        :param surface: Surface of the main display.
        """
        gfxdraw.filled_circle(surface, self.rect.center[0], self.rect.center[1], RADIUS, (0, 0, 0))
