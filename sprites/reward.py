import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

SIZE = 24


class Reward(Sprite):
    """
    A reward is the only way to increase the score in the game. It spawns in a random position on the
    main stage and adds 15 points to the score when it collides with the player.
    """
    def __init__(self, pos: tuple[int, int]):
        super(Reward, self).__init__()
        self.img_src = pygame.image.load('resources/reward.png')
        self.image = self.img_src
        self.pos = pos
        self.size = 0
        self.set_size(0)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 0.0

    def set_size(self, size):
        """
        Using the source image (self.img_src) scale the image to the desired size and update its
        mask and rect for rendering. This is required for the bouncing scale animation.
        :param size: Desired size.
        """
        self.size = int(size)
        self.image = pygame.transform.smoothscale(self.img_src, (self.size, self.size))
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen: Surface):
        """
        Draw the reward, represented as a dark green rounded square.
        :param screen: Main display for rendering.
        """
        self.velocity = ((SIZE - self.size) * 0.2) + (self.velocity * 0.85)
        self.set_size(self.size + self.velocity)
        screen.blit(self.image, self.rect)
