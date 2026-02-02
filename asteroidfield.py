# asteroidfield.py

import random
from pygame.math import Vector2
from asteroid import Asteroid
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
)


class AsteroidField:
    def __init__(self, asteroid_group, all_sprites, player):
        self.asteroid_group = asteroid_group
        self.all_sprites = all_sprites
        self.player = player

    # ---------------------------------------------------------
    # Spawn a single asteroid at a random location
    # ---------------------------------------------------------
    def spawn_asteroid(self):
        radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)

        # Avoid spawning too close to the player
        while True:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pos = Vector2(x, y)

            if pos.distance_to(self.player.position) > 200:
                break

        Asteroid.containers = (self.asteroid_group, self.all_sprites)
        Asteroid(x, y, radius)

    # ---------------------------------------------------------
    # Spawn multiple asteroids at game start
    # ---------------------------------------------------------
    def spawn_initial_asteroids(self, count):
        for _ in range(count):
            self.spawn_asteroid()