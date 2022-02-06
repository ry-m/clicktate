import math

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

from sprites.player import SIZE as PLAYER_SIZE

RETRY_BUTTON = pygame.image.load('resources/retry.png')
RETRY_BUTTON_ACTIVE = pygame.image.load('resources/retry_active.png')
PLAY_BUTTON = pygame.image.load('resources/play.png')
PLAY_BUTTON_ACTIVE = pygame.image.load('resources/play_active.png')

INACTIVE_SIZE = 100.0
ACTIVE_SIZE = 120.0


def scaled_image(image: Surface, size: float) -> Surface:
    return pygame.transform.smoothscale(image, (size, size))


class PlayButton(Sprite):
    def __init__(self, is_retry_btn: bool = False, pos: tuple[int, int] = (0, 0)):
        super(PlayButton, self).__init__()
        self.img_src = RETRY_BUTTON if is_retry_btn else PLAY_BUTTON
        self.image = scaled_image(self.img_src, PLAYER_SIZE)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.size = PLAYER_SIZE
        self.is_retry_btn = is_retry_btn
        self.active = False

    def draw(self, screen: Surface):
        # Move sprite to center.
        self.pos = (
            self.pos[0] + (screen.get_width() / 2 - self.pos[0]) * 0.2,
            self.pos[1] + (screen.get_height() / 2 - self.pos[1]) * 0.2
        )

        mouse_pos = pygame.mouse.get_pos()
        touching = math.dist(mouse_pos, self.pos) <= self.size / 2
        self.active = touching

        # Set image and
        if self.is_retry_btn:
            self.img_src = RETRY_BUTTON_ACTIVE if touching else RETRY_BUTTON
        else:
            self.img_src = PLAY_BUTTON_ACTIVE if touching else PLAY_BUTTON

        if touching:
            self.size += (ACTIVE_SIZE - self.size) * 0.1
        else:
            self.size += (INACTIVE_SIZE - self.size) * 0.1

        # Set the size of the image based on self.size:
        self.image = scaled_image(self.img_src, self.size)

        # Draw the image.
        screen.blit(self.image, self.image.get_rect(center=self.pos))
