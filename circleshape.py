# circleshape.py

import pygame
from pygame.math import Vector2


class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.position = Vector2(x, y)
        self.radius = radius
        self.velocity = Vector2(0, 0)

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)

