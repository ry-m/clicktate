from enum import Enum

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

from sprites.player import Player

SIZE = 24
DIST_FROM_PLAYER = 60
FADE_SPEED = 8


class ObstacleState(Enum):
    INACTIVE = -1  # The obstacle is invisible.
    SPAWNING = 0  # The obstacle is 'fading in'
    LURKING = 1  # The obstacle is following the player and half-visible.
    ACTIVE = 2  # The obstacle is active and fully visible.


class Obstacle(Sprite):
    """
    An obstacle is represented as an orange triangle. It has four states:
    inactive: not visible, not active.
    spawning: the obstacle is fading in, still inactive.
    lurking: the obstacle is following the player.
    active: the obstacle plants itself, becomes active.
    """
    def __init__(self, player: Player):
        super(Obstacle, self).__init__()
        self.state = ObstacleState.INACTIVE
        self.player = player
        self.image = pygame.image.load('resources/obstacle.png')
        self.image = pygame.transform.smoothscale(self.image, (SIZE, SIZE))
        self.rect = self.image.get_rect(center=self.get_pos_from_player())
        self.mask = pygame.mask.from_surface(self.image)
        self.alpha = 0

    def is_active(self) -> bool:
        """
        :return: True if the obstacle is in an active state.
        """
        return self.state == ObstacleState.ACTIVE

    def get_pos_from_player(self) -> tuple[float, float]:
        """
        Retrieve the offset position from the player's current position.
        :return: Coordinates of the obstacle position.
        """
        ox = self.player.pos[0] + self.player.direction.value[0]*DIST_FROM_PLAYER
        oy = self.player.pos[1] + self.player.direction.value[1]*DIST_FROM_PLAYER
        return float(ox), float(oy)

    def spawn(self):
        """
        Set the state to SPAWNING
        """
        self.state = ObstacleState.SPAWNING

    def activate(self):
        """
        Set the state to ACTIVE
        """
        self.state = ObstacleState.ACTIVE

    def deactivate(self):
        """
        Set the state to INACTIVE
        """
        self.state = ObstacleState.INACTIVE

    def draw(self, screen: Surface):
        """
        Draw the sprite.
        :param screen: Screen for rendering.
        """
        if self.state == ObstacleState.INACTIVE:
            self.alpha = max(0, self.alpha - FADE_SPEED)
        elif self.state == ObstacleState.SPAWNING:
            self.alpha = min(128, self.alpha + FADE_SPEED)
            if self.alpha == 128:
                self.state = ObstacleState.LURKING
        elif self.state == ObstacleState.ACTIVE:
            self.alpha = min(255, self.alpha + FADE_SPEED)

        if self.state == ObstacleState.SPAWNING or self.state == ObstacleState.LURKING:
            # Update the position. If active, don't update.
            self.rect = self.image.get_rect(center=self.get_pos_from_player())

        self.image.set_alpha(self.alpha)
        screen.blit(self.image, self.rect)
