# explosion.py

import pygame
import random
from pygame.math import Vector2


class Particle(pygame.sprite.Sprite):
    def __init__(self, position, velocity, lifetime, color):
        super().__init__()
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.lifetime = lifetime
        self.color = color
        self.age = 0

    def update(self, dt):
        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
            return

        self.position += self.velocity * dt

    def draw(self, screen):
        # Fade out over time
        alpha = max(0, 255 * (1 - self.age / self.lifetime))
        color = (*self.color, int(alpha))

        # Draw as a small glowing dot
        surf = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (2, 2), 2)
        screen.blit(surf, self.position)


class Explosion(pygame.sprite.Group):
    def __init__(self, position, color=(255, 200, 50), particle_count=20):
        super().__init__()
        self.position = Vector2(position)

        for _ in range(particle_count):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 200)
            velocity = Vector2(1, 0).rotate(angle) * speed
            lifetime = random.uniform(0.3, 0.8)

            particle = Particle(self.position, velocity, lifetime, color)
            self.add(particle)

    def draw(self, screen):
        for particle in self.sprites():
            particle.draw(screen)