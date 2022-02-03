import pygame
from pygame.constants import GL_MULTISAMPLEBUFFERS, GL_MULTISAMPLESAMPLES

from player import Player


# Constants.
SIZE = (800, 600)
FPS = 60
BG_COLOUR = (210, 255, 120)
CENTER = (SIZE[0]/2, SIZE[1]/2)


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
        player.draw(screen)
        pygame.display.flip()

        # Updating
        clock.tick(FPS)
        player.move()

    pygame.quit()


if __name__ == '__main__':
    main()
