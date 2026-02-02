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
from explosion import Explosion


class Asteroid(CircleShape):
    containers = None
    explosion_group = None

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        angle = random.uniform(0, 360)
        speed = random.uniform(40, 120)
        self.velocity = Vector2(1, 0).rotate(angle) * speed

        # NEW: random polygon shape
        self.points = self.generate_shape()

        # NEW: rotation speed
        self.rotation = random.uniform(-40, 40)

        if Asteroid.containers:
            for group in Asteroid.containers:
                group.add(self)

    # ---------------------------------------------------------
    # Generate a lumpy asteroid polygon
    # ---------------------------------------------------------
    def generate_shape(self):
        points = []
        count = random.randint(8, 14)

        for i in range(count):
            angle = (360 / count) * i + random.uniform(-10, 10)
            distance = random.uniform(self.radius * 0.6, self.radius)
            point = Vector2(distance, 0).rotate(angle)
            points.append(point)

        return points

    # ---------------------------------------------------------
    # Update movement + rotation + wrapping
    # ---------------------------------------------------------
    def update(self, dt):
        self.position += self.velocity * dt

        # Rotate shape
        self.points = [p.rotate(self.rotation * dt) for p in self.points]

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
    # Drawing (polygon instead of circle)
    # ---------------------------------------------------------
    def draw(self, screen):
        translated = [(self.position.x + p.x, self.position.y + p.y) for p in self.points]
        pygame.draw.polygon(screen, "white", translated, LINE_WIDTH)

    # ---------------------------------------------------------
    # Splitting + explosion
    # ---------------------------------------------------------
    def split(self):
        # Explosion
        if Asteroid.explosion_group is not None:
            boom = Explosion(self.position, color=(255, 200, 80), particle_count=25)
            Asteroid.explosion_group.add(boom)

        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        angle = random.uniform(20, 50)

        vel1 = self.velocity.rotate(angle) * 1.2
        vel2 = self.velocity.rotate(-angle) * 1.2

        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)

        a1.velocity = vel1
        a2.velocity = vel2