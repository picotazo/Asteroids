import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
        )

    def split(self):
        # Always destroy the current asteroid
        self.kill()

        # If this asteroid is already the smallest size, we're done
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Log the split event
        log_event("asteroid_split")

        # Pick a random angle between 20 and 50 degrees
        angle = random.uniform(20, 50)

        # Create two new velocity vectors by rotating the original
        vel1 = self.velocity.rotate(angle)
        vel2 = self.velocity.rotate(-angle)

        # New radius for the smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Spawn the two new asteroids at the same position
        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Make them move faster (1.2x)
        a1.velocity = vel1 * 1.2
        a2.velocity = vel2 * 1.2

    def update(self, dt):
        self.position += self.velocity * dt