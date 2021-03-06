import random
from pygame.surface import Surface


ORANGE = (230, 100, 45)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Particle:
    def __init__(self, pos: tuple[int, int], player_death: bool):
        self.size = random.randint(4, 9)
        self.pos = pos
        self.image = Surface((self.size, self.size))
        self.colour = ORANGE if player_death else BLACK if random.randint(0, 1) else WHITE
        self.image.fill(self.colour)
        self.x_vel = random.randint(-4, 4)
        self.y_vel = random.randint(-7, -2)

    def draw(self, screen: Surface):
        """
        Draw a single particle, update its animation.
        :param screen: Display surface for rendering.
        """
        if not self.is_off_screen(screen.get_size()):
            self.y_vel += 0.35
            self.pos = (self.pos[0] + self.x_vel, self.pos[1] + self.y_vel)
            screen.blit(self.image, self.image.get_rect(center=self.pos))

    def is_off_screen(self, screen_dimensions: tuple[int, int]) -> bool:
        return self.pos[0] <= 0 \
               or self.pos[1] <= 0 \
               or self.pos[0] >= screen_dimensions[0] \
               or self.pos[1] >= screen_dimensions[1]


class ParticleEffect:
    def __init__(self, player_death: bool = False):
        self.pos = (0, 0)
        self.player_death = player_death
        self.batch = []
        self.active = False

    def trigger(self, pos: tuple[int, int]):
        self.pos = pos
        for i in range(random.randint(6, 11)):
            self.batch.append(Particle(pos, self.player_death))
        self.active = True

    def draw(self, screen: Surface):
        if self.active:
            for particle in self.batch:
                particle.draw(screen)
