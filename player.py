# player.py

import pygame
from pygame.math import Vector2
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_ACCELERATION,
    PLAYER_FRICTION,
    PLAYER_INVINCIBILITY_TIME,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
import time


class Player(CircleShape):
    containers = None  # set by main.py

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)

        self.velocity = Vector2(0, 0)
        self.rotation = 0  # degrees
        self.lives = 3
        self.respawn_time = 0
        self.invincible = False

        if Player.containers:
            for group in Player.containers:
                group.add(self)

    # ---------------------------------------------------------
    # Input handling
    # ---------------------------------------------------------
    def handle_input(self, dt):
        keys = pygame.key.get_pressed()

        # Rotation (A/D or Left/Right)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotation -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotation += PLAYER_TURN_SPEED * dt

        # Thrust (W or Up)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction = Vector2(1, 0).rotate(self.rotation)
            self.velocity += direction * PLAYER_ACCELERATION * dt

        # Reverse thrust (S or Down)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction = Vector2(1, 0).rotate(self.rotation)
            self.velocity -= direction * PLAYER_ACCELERATION * dt

    # ---------------------------------------------------------
    # Respawn + invincibility
    # ---------------------------------------------------------
    def start_invincibility(self):
        self.invincible = True
        self.respawn_time = time.time()

    def update_invincibility(self):
        if self.invincible:
            if time.time() - self.respawn_time >= PLAYER_INVINCIBILITY_TIME:
                self.invincible = False

    # ---------------------------------------------------------
    # Update loop
    # ---------------------------------------------------------
    def update(self, dt):
        self.handle_input(dt)
        self.update_invincibility()

        # Apply friction
        self.velocity *= PLAYER_FRICTION

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

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------
    def draw(self, screen):
        # Ship is a triangle
        direction = Vector2(1, 0).rotate(self.rotation)

        left = direction.rotate(140) * PLAYER_RADIUS
        right = direction.rotate(-140) * PLAYER_RADIUS
        nose = direction * (PLAYER_RADIUS * 1.4)

        p1 = self.position + nose
        p2 = self.position + left
        p3 = self.position + right

        color = "yellow" if self.invincible else "white"

        pygame.draw.polygon(screen, color, [p1, p2, p3], 2)

    # ---------------------------------------------------------
    # Collision override (invincibility)
    # ---------------------------------------------------------
    def collides_with(self, other):
        if self.invincible:
            return False
        return super().collides_with(other)

    # ---------------------------------------------------------
    # Respawn logic
    # ---------------------------------------------------------
    def respawn(self):
        self.position = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = Vector2(0, 0)
        self.rotation = 0
        self.start_invincibility()