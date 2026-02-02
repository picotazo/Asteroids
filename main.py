# main.py
import pygame
import sys
from pygame.math import Vector2
from background import Starfield

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FONT_SIZE,
    PLAYER_LIVES,
    SHOT_RADIUS,
    SHOT_SPEED,
)
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion


def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    background = Starfield()

    # ---------------------------------------------------------
    # Sprite groups
    # ---------------------------------------------------------
    all_sprites = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()   # NEW

    # Assign containers
    Player.containers = (all_sprites,)
    Asteroid.containers = (asteroid_group, all_sprites)
    Shot.containers = (shot_group, all_sprites)

    # NEW: explosion group references
    Player.explosion_group = explosion_group
    Asteroid.explosion_group = explosion_group

    # ---------------------------------------------------------
    # Player setup
    # ---------------------------------------------------------
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.lives = PLAYER_LIVES
    player.start_invincibility()

    # ---------------------------------------------------------
    # Asteroid field setup
    # ---------------------------------------------------------
    field = AsteroidField(asteroid_group, all_sprites, player)
    field.spawn_initial_asteroids(6)

    # ---------------------------------------------------------
    # Scoring
    # ---------------------------------------------------------
    score = 0
    font = pygame.font.SysFont(None, FONT_SIZE)

    # ---------------------------------------------------------
    # Game loop
    # ---------------------------------------------------------
    running = True
    while running:
        dt = clock.tick(60) / 1000

        # -----------------------------------------------------
        # Event handling
        # -----------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    direction = Vector2(1, 0).rotate(player.rotation)
                    shot = Shot(player.position.x, player.position.y, SHOT_RADIUS)
                    shot.velocity = direction * SHOT_SPEED

        # -----------------------------------------------------
        # Update all sprites
        # -----------------------------------------------------
        all_sprites.update(dt)
        explosion_group.update(dt)   # NEW

        # -----------------------------------------------------
        # Collision: Shots vs Asteroids
        # -----------------------------------------------------
        for shot in shot_group:
            for asteroid in asteroid_group:
                if shot.collides_with(asteroid):
                    shot.kill()
                    asteroid.split()

                    if asteroid.radius > 40:
                        score += 20
                    elif asteroid.radius > 25:
                        score += 50
                    else:
                        score += 100

        # -----------------------------------------------------
        # Collision: Player vs Asteroids
        # -----------------------------------------------------
        for asteroid in asteroid_group:
            if player.collides_with(asteroid) and not player.invincible:
                asteroid.split()
                player.explode()     # NEW
                player.lives -= 1

                if player.lives <= 0:
                    running = False
                else:
                    player.respawn()

        # -----------------------------------------------------
        # Drawing
        # -----------------------------------------------------
        screen.fill("black")
        background.draw(screen)

        # Draw sprites
        for sprite in all_sprites:
            sprite.draw(screen)

        # Draw explosions (NEW)
        for boom in explosion_group:
            boom.draw(screen)

        # Draw score
        score_surf = font.render(f"Score: {score}", True, "white")
        screen.blit(score_surf, (10, 10))

        # Draw lives
        lives_surf = font.render(f"Lives: {player.lives}", True, "white")
        screen.blit(lives_surf, (10, 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()