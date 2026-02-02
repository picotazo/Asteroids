# main.py
import pygame
import sys
import json
import os
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


# ---------------------------------------------------------
# High Score Helpers
# ---------------------------------------------------------
def load_high_scores():
    if not os.path.exists("highscores.json"):
        return []
    with open("highscores.json", "r") as f:
        return json.load(f)


def save_high_score(score):
    scores = load_high_scores()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:10]  # keep top 10
    with open("highscores.json", "w") as f:
        json.dump(scores, f)


# ---------------------------------------------------------
# Game Over Screen
# ---------------------------------------------------------
def game_over_screen(screen, font, score):
    title = font.render("GAME OVER", True, "white")
    score_text = font.render(f"Final Score: {score}", True, "white")
    prompt = font.render("Press R to Restart or Q to Quit", True, "white")

    # Load high scores
    scores = load_high_scores()
    high_title = font.render("High Scores:", True, "white")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill("black")

        # Draw main text
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 260))

        # Draw high scores
        screen.blit(high_title, (SCREEN_WIDTH // 2 - high_title.get_width() // 2, 340))
        y = 380
        for s in scores[:10]:
            hs = font.render(str(s), True, "white")
            screen.blit(hs, (SCREEN_WIDTH // 2 - hs.get_width() // 2, y))
            y += 30

        pygame.display.flip()


# ---------------------------------------------------------
# Main Game Loop
# ---------------------------------------------------------
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
    explosion_group = pygame.sprite.Group()

    # Assign containers
    Player.containers = (all_sprites,)
    Asteroid.containers = (asteroid_group, all_sprites)
    Shot.containers = (shot_group, all_sprites)

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
        explosion_group.update(dt)

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
                player.explode()
                player.lives -= 1

                if player.lives <= 0:
                    save_high_score(score)
                    result = game_over_screen(screen, font, score)
                    if result == "restart":
                        return main()

                else:
                    player.respawn()

        # -----------------------------------------------------
        # Drawing
        # -----------------------------------------------------
        screen.fill("black")
        background.draw(screen)

        for sprite in all_sprites:
            sprite.draw(screen)

        for boom in explosion_group:
            boom.draw(screen)

        score_surf = font.render(f"Score: {score}", True, "white")
        screen.blit(score_surf, (10, 10))

        lives_surf = font.render(f"Lives: {player.lives}", True, "white")
        screen.blit(lives_surf, (10, 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()