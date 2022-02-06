from enum import Enum
from itertools import cycle

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

from ui import score

RADIUS = 12
SPEED = 3
SIZE = 24
BUTTON_SIZE = 100


class Direction(Enum):
    """
    Represents a diagonal direction the sprite travels in.
    Value is the x/y change respectively.
    """
    NORTH_EAST = (1, 1)
    SOUTH_EAST = (1, -1)
    SOUTH_WEST = (-1, -1)
    NORTH_WEST = (-1, 1)


class Player(Sprite):
    """
    The player sprite is represented as a filled black circle.
    """
    def __init__(self, pos: tuple[int, int]):
        super(Player, self).__init__()
        self.image = pygame.image.load('resources/player.png')
        self.image = pygame.transform.smoothscale(self.image, (SIZE, SIZE))
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.all_dirs = cycle([Direction.NORTH_WEST, Direction.SOUTH_WEST, Direction.SOUTH_EAST, Direction.NORTH_EAST])
        self.direction = next(self.all_dirs)
        self.alive = True

    def set_pos(self, x, y):
        """
        Set the player position.
        :param x: x position
        :param y: y position
        """
        pos = (x, y)
        self.pos = pos
        self.rect.center = pos

    def draw(self, surface: pygame.Surface):
        """
        Render the player onto the surface.
        The player sprite is represented by a filled black circle.
        :param surface: surface of the main display.
        """
        surface.blit(self.image, self.rect)

    def move(self):
        """
        Move the sprite in its current diagonal direction.
        """
        self.set_pos(
            self.pos[0] + self.direction.value[0] * SPEED,
            self.pos[1] + self.direction.value[1] * SPEED
        )

    def change_direction(self):
        """
        Change the sprite direction (clockwise).
        """
        self.direction = next(self.all_dirs)

    def touching_edge(self, screen: Surface) -> bool:
        """
        Check if the player is touching the edge of the display.
        :param screen: The display surface
        :return: True if the player is touching the edge.
        """
        sx, sy = screen.get_size()
        return \
            self.pos[0] + RADIUS > sx \
            or self.pos[1] + RADIUS > sy \
            or self.pos[0] - RADIUS < 0 \
            or self.pos[1] - RADIUS < score.BAR_HEIGHT
