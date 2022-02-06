import random

import pygame
from pygame.constants import GL_MULTISAMPLEBUFFERS, GL_MULTISAMPLESAMPLES

from constants import SIZE, BG_COLOUR, FPS
from game import Clicktate, GameState

# Events
spawn_obs_event = pygame.USEREVENT + 1
activate_obs_event = pygame.USEREVENT + 2
deactivate_obs_event = pygame.USEREVENT + 3


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

    game = Clicktate()

    running = True
    trigger_obs()

    while running:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click()
            if event.type == spawn_obs_event and game.state == GameState.RUNNING:
                game.obstacle.spawn()
            if event.type == activate_obs_event and game.state == GameState.RUNNING:
                game.obstacle.activate()
                pygame.time.set_timer(deactivate_obs_event, 1500, loops=1)
            if event.type == deactivate_obs_event and game.state == GameState.RUNNING:
                game.obstacle.deactivate()
                trigger_obs()

        # Rendering.
        screen.fill(BG_COLOUR)
        game.render(screen)

        pygame.display.flip()

        # Updating
        clock.tick(FPS)
        game.update(screen)

    pygame.quit()


if __name__ == '__main__':
    main()
