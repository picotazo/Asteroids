# asteroid.py

import pygame
import random
from pygame.math import Vector2
from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    ASTEROID_MIN_RADIUS,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from logger import log_event


class Asteroid(CircleShape):
    containers = None  # set by main.py

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        # Random movement direction
        angle = random.uniform(0, 360)
        speed = random.uniform(40, 120)
        self.velocity = Vector2(1, 0).rotate(angle) * speed

        if Asteroid.containers:
            for group in Asteroid.containers:
                group.add(self)

    # ---------------------------------------------------------
    # Update movement + wrapping
    # ---------------------------------------------------------
    def update(self, dt):
        self.position += self.velocity * dt

        # Screen wrapping
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------
    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
        )

    # ---------------------------------------------------------
    # Splitting logic
    # ---------------------------------------------------------
    def split(self):
        # Remove this asteroid
        self.kill()

        # If too small, do not split further
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        # New radius for children
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Random angle offset
        angle = random.uniform(20, 50)

        # Two new velocity vectors
        vel1 = self.velocity.rotate(angle) * 1.2
        vel2 = self.velocity.rotate(-angle) * 1.2

        # Spawn two new asteroids
        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)

        a1.velocity = vel1
        a2.velocity = vel2