# player.py

import pygame
from pygame.math import Vector2
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_THRUST,
    PLAYER_INVINCIBILITY_TIME,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from explosion import Explosion


class Player(CircleShape):
    containers = None
    explosion_group = None   # NEW: explosion group reference

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.velocity = Vector2(0, 0)
        self.invincible = False
        self.invincibility_timer = 0

        if Player.containers:
            for group in Player.containers:
                group.add(self)

    # ---------------------------------------------------------
    # Movement + wrapping
    # ---------------------------------------------------------
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Rotation
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation += PLAYER_TURN_SPEED * dt

        # Thrust
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = Vector2(1, 0).rotate(self.rotation)
            self.velocity += direction * PLAYER_THRUST * dt

        # Movement
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

        # Invincibility timer
        if self.invincible:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------
    def draw(self, screen):
        # Flash while invincible
        if self.invincible:
            if int(self.invincibility_timer * 10) % 2 == 0:
                return

        # Draw triangle ship
        points = self.get_triangle_points()
        pygame.draw.polygon(screen, "white", points, 2)

    def get_triangle_points(self):
        forward = Vector2(1, 0).rotate(self.rotation)
        right = forward.rotate(140)
        left = forward.rotate(-140)

        tip = self.position + forward * self.radius
        r = self.position + right * self.radius * 0.7
        l = self.position + left * self.radius * 0.7

        return [tip, r, l]

    # ---------------------------------------------------------
    # Explosion + respawn
    # ---------------------------------------------------------
    def explode(self):
        if Player.explosion_group is not None:
            boom = Explosion(self.position, color=(100, 200, 255), particle_count=30)
            Player.explosion_group.add(boom)

    def respawn(self):
        self.position = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = Vector2(0, 0)
        self.rotation = 0
        self.start_invincibility()

    def start_invincibility(self):
        self.invincible = True
        self.invincibility_timer = PLAYER_INVINCIBILITY_TIME