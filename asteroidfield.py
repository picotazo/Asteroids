# asteroidfield.py

import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField:
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MIN_RADIUS, y * SCREEN_HEIGHT)

        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MIN_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MIN_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MIN_RADIUS
            ),
        ],
    ]

    def __init__(self, asteroid_group, all_sprites_group, player):
        self.asteroid_group = asteroid_group
        self.all_sprites_group = all_sprites_group
        self.player = player
        self.spawn_timer = 0.0

    # ---------------------------------------------------------
    # Spawn a single asteroid
    # ---------------------------------------------------------
    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    # ---------------------------------------------------------
    # Spawn N asteroids at random edges (used at game start)
    # ---------------------------------------------------------
    def spawn_initial_asteroids(self, count):
        for _ in range(count):
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            radius = random.randint(25, 60)

            self.spawn(radius, position, velocity)

    # ---------------------------------------------------------
    # Update: timed spawning
    # ---------------------------------------------------------
    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            radius = random.randint(25, 60)
            self.spawn(radius, position, velocity)
