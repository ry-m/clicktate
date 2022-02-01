import pygame
from player import Player


# Constants.
SIZE = (800, 600)
BG_COLOUR = (210, 255, 120)
CENTER = (SIZE[0]/2, SIZE[1]/2)


def main():
    """
    Main program loop.
    """
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Clicktate')

    player = Player(CENTER)

    running = True

    while running:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rendering.
        screen.fill(BG_COLOUR)
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
