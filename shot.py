# shot.py

import pygame
from pygame.math import Vector2
from circleshape import CircleShape
from constants import SHOT_SPEED, SHOT_LIFETIME, SCREEN_WIDTH, SCREEN_HEIGHT
import time


class Shot(CircleShape):
    containers = None  # set by main.py

    def __init__(self, x, y, direction):
        super().__init__(x, y, 4)  # small radius for collision
        self.velocity = direction * SHOT_SPEED
        self.spawn_time = time.time()

        if Shot.containers:
            for group in Shot.containers:
                group.add(self)

    # ---------------------------------------------------------
    # Update movement + lifetime + wrapping
    # ---------------------------------------------------------
    def update(self, dt):
        # Move
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

        # Lifetime expiration
        if time.time() - self.spawn_time > SHOT_LIFETIME:
            self.kill()

    # ---------------------------------------------------------
    # Draw bullet
    # ---------------------------------------------------------
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius)