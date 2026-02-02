# background.py

import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Starfield:
    def __init__(self, star_count=200):
        self.stars = []

        for _ in range(star_count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(150, 255)
            self.stars.append((x, y, brightness))

    def draw(self, screen):
        for x, y, b in self.stars:
            screen.set_at((x, y), (b, b, b))