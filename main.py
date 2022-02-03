import random
import pygame
from pygame.constants import GL_MULTISAMPLEBUFFERS, GL_MULTISAMPLESAMPLES

from player import Player
from reward import Reward


# Constants.
SIZE = (800, 600)
FPS = 60
BG_COLOUR = (210, 255, 120)
CENTER = (SIZE[0]/2, SIZE[1]/2)
REWARD_SPAWN_OFFSET = 60


def spawn_reward() -> Reward:
    """
    Spawn a new Reward sprite at a random position on the screen.
    :return: Reward sprite
    """
    rx = float(random.randint(REWARD_SPAWN_OFFSET, SIZE[0] - REWARD_SPAWN_OFFSET))
    ry = float(random.randint(REWARD_SPAWN_OFFSET, SIZE[1] - REWARD_SPAWN_OFFSET))
    return Reward((rx, ry))


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
    score = 0

    running = True

    while running:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.change_direction()

        # Rendering.
        screen.fill(BG_COLOUR)
        reward.draw(screen)
        player.draw(screen)
        pygame.display.flip()

        # Updating
        clock.tick(FPS)
        if player.alive:
            player.move()
            if pygame.sprite.collide_circle(player, reward):
                score += 15
                print(f'Score: {score}')
                reward = spawn_reward()
            player.alive = not player.touching_edge(screen)
        else:
            print("Player dead.")
            running = False

    pygame.quit()


if __name__ == '__main__':
    main()
