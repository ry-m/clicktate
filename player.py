from enum import Enum
from itertools import cycle

import pygame
from pygame.sprite import Sprite
from pygame import gfxdraw
from pygame.surface import Surface


RADIUS = 12
SPEED = 2


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
    def __init__(self, pos: tuple[float, float]):
        super(Player, self).__init__()
        self.image = pygame.surface.Surface((RADIUS * 2, RADIUS * 2))
        self.rect = self.image.get_rect(center=pos)
        self.radius = RADIUS
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]
        self.all_dirs = cycle([Direction.NORTH_WEST, Direction.SOUTH_WEST, Direction.SOUTH_EAST, Direction.NORTH_EAST])
        self.direction = next(self.all_dirs)
        self.alive = True

    def set_pos(self, x, y):
        """
        Set the player position.
        :param x: x position
        :param y: y position
        """
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def draw(self, surface: pygame.Surface):
        """
        Render the player onto the surface.
        The player sprite is represented by a filled black circle.
        :param surface: surface of the main display.
        """
        gfxdraw.filled_circle(surface, self.x, self.y, RADIUS, (0, 0, 0))

    def move(self):
        """
        Move the sprite in its current diagonal direction.
        """
        self.set_pos(
            self.x + self.direction.value[0] * SPEED,
            self.y + self.direction.value[1] * SPEED
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
        return self.x+RADIUS > sx or self.y+RADIUS > sy or self.x-RADIUS < 0 or self.y-RADIUS < 0
