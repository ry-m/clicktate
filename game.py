import random
from enum import Enum

import pygame
from pygame.surface import Surface

from constants import SIZE, CENTER, REWARD_SPAWN_OFFSET
from particles.particles import ParticleEffect
from sprites.obstacle import Obstacle
from sprites.player import Player
from sprites.reward import Reward
from ui.score import BAR_HEIGHT, Score

from ui.play_button import PlayButton


class GameState(Enum):
    INTRO_ANIM = 0,
    CLICK_TO_START = 1,
    RUNNING = 2,
    GAME_OVER = 3


def _spawn_reward() -> Reward:
    """
    Spawn a new Reward sprite at a random position on the screen.
    :return: Reward sprite
    """
    rx = random.randint(REWARD_SPAWN_OFFSET, SIZE[0] - REWARD_SPAWN_OFFSET)
    ry = random.randint(REWARD_SPAWN_OFFSET + BAR_HEIGHT, SIZE[1] - REWARD_SPAWN_OFFSET)
    return Reward((rx, ry))


class Clicktate:
    """
    Represents the overall game including its sprites and game objects.
    Maintains the score and game state.
    """
    def __init__(self):
        self.player = Player(CENTER)
        self.reward = _spawn_reward()
        self.obstacle = Obstacle(self.player)
        self.death_particles = ParticleEffect(player_death=True)
        self.reward_particles = ParticleEffect()
        self.state = GameState.RUNNING
        self.retry_btn = PlayButton(True)
        self.score = Score(SIZE[0])

    def render(self, screen: Surface):
        """
        Draw and render objects to the screen.
        :param screen: Display surface.
        """
        if self.state == GameState.RUNNING:
            self.player.draw(screen)
            self.reward.draw(screen)
            self.obstacle.draw(screen)
            self.reward_particles.draw(screen)
        elif self.state == GameState.GAME_OVER:
            self.retry_btn.draw(screen)

        self.death_particles.draw(screen)
        self.score.draw(screen)

    def update(self, screen: Surface):
        """
        Update the game (game tick).
        :param screen: Display surface.
        """
        if self.state == GameState.RUNNING:
            if self.player.alive:
                self.player.move()
                if pygame.sprite.collide_mask(self.player, self.reward):
                    reward_particles = ParticleEffect()
                    reward_particles.trigger(self.reward.pos)
                    self.score.update(15)
                    self.reward = _spawn_reward()
                self.player.alive = not self.player.touching_edge(screen) and not \
                    (pygame.sprite.collide_mask(self.player, self.obstacle) and self.obstacle.is_active())
            else:
                self.death_particles.trigger(self.player.pos)
                self.retry_btn = PlayButton(True, self.player.pos)
                self.state = GameState.GAME_OVER

    def reset(self):
        """
        Reset the game (create a new game).
        """
        self.player = Player(CENTER)
        self.reward = _spawn_reward()
        self.score.set_to_zero()
        self.state = GameState.RUNNING

    def handle_click(self):
        """
        Handle a mouse click, dependent on the game state.
        :return:
        """
        if self.state == GameState.RUNNING:
            self.player.change_direction()
        elif self.state == GameState.GAME_OVER:
            if self.retry_btn.active:
                self.reset()
