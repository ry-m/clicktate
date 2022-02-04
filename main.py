import random
from enum import Enum

import pygame
from pygame.constants import GL_MULTISAMPLEBUFFERS, GL_MULTISAMPLESAMPLES

from particles.particles import ParticleEffect
from sprites.obstacle import Obstacle
from sprites.player import Player
from sprites.reward import Reward
from score import BAR_HEIGHT, Score

# Constants.
SIZE = (800, 600)
FPS = 60
BG_COLOUR = (210, 255, 120)
CENTER = (SIZE[0] / 2, SIZE[1] / 2)
REWARD_SPAWN_OFFSET = 60

# Events
spawn_obs_event = pygame.USEREVENT + 1
activate_obs_event = pygame.USEREVENT + 2
deactivate_obs_event = pygame.USEREVENT + 3


class GameState(Enum):
    INTRO_ANIM = 0,
    CLICK_TO_START = 1,
    RUNNING = 2,
    GAME_OVER = 3


def spawn_reward() -> Reward:
    """
    Spawn a new Reward sprite at a random position on the screen.
    :return: Reward sprite
    """
    rx = random.randint(REWARD_SPAWN_OFFSET, SIZE[0] - REWARD_SPAWN_OFFSET)
    ry = random.randint(REWARD_SPAWN_OFFSET + BAR_HEIGHT, SIZE[1] - REWARD_SPAWN_OFFSET)
    return Reward((rx, ry))


def trigger_obs():
    time = random.randint(5500, 10500)
    pygame.time.set_timer(spawn_obs_event, time, loops=1)  # Spawn event.
    pygame.time.set_timer(activate_obs_event, time + 1000, loops=1)  # Activate event (1.5s after spawn)


def main():
    """
    Main program loop.
    """
    pygame.init()
    screen = pygame.display.set_mode(SIZE, GL_MULTISAMPLEBUFFERS)
    clock = pygame.time.Clock()
    pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 3)
    pygame.display.set_caption('Clicktate')

    player = Player(CENTER)
    reward = spawn_reward()
    obstacle = Obstacle(player)
    death_particles = ParticleEffect(player_death=True)
    reward_particles = ParticleEffect()
    score = Score(SIZE[0])

    running = True
    state = GameState.RUNNING
    trigger_obs()

    while running:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == GameState.RUNNING:
                    player.change_direction()
            if event.type == spawn_obs_event and state == GameState.RUNNING:
                obstacle.spawn()
            if event.type == activate_obs_event and state == GameState.RUNNING:
                obstacle.activate()
                pygame.time.set_timer(deactivate_obs_event, 1500, loops=1)
            if event.type == deactivate_obs_event and state == GameState.RUNNING:
                obstacle.deactivate()
                trigger_obs()

        # Rendering.
        screen.fill(BG_COLOUR)
        reward.draw(screen)
        player.draw(screen)
        obstacle.draw(screen)
        reward_particles.draw(screen)
        death_particles.draw(screen)
        score.draw(screen)

        pygame.display.flip()

        # Updating
        clock.tick(FPS)
        if state == GameState.RUNNING:
            if player.alive:
                player.move()
                if pygame.sprite.collide_mask(player, reward):
                    reward_particles = ParticleEffect()
                    reward_particles.trigger(reward.pos)
                    score.update(15)
                    print(f'Score: {score.score}')
                    reward = spawn_reward()
                player.alive = not player.touching_edge(screen) and not \
                    (pygame.sprite.collide_mask(player, obstacle) and obstacle.is_active())
            else:
                death_particles.trigger((player.x, player.y))
                state = GameState.GAME_OVER

    pygame.quit()


if __name__ == '__main__':
    main()
