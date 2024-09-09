import pygame
import sys
import time
import random
import threading
from player import Player
from platform import Platform
from enemy import Enemy, Powerup

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman the gun")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Fonts
font = pygame.font.Font(None, 36)

# Create the player
player = Player(50, HEIGHT - 100)

# Create platforms
platforms = [
    Platform(0, HEIGHT - 40, WIDTH, 40, indestructible=True),  # Main floor
    Platform(300, 400, 200, 40),
    Platform(100, 300, 150, 40),
    Platform(500, 200, 200, 40),
]

# Enemy spawning
def spawn_enemies(num_enemies):
    enemies = pygame.sprite.Group()
    for _ in range(num_enemies):
        x = random.randint(100, WIDTH - 100)
        y = random.choice([360, 260, 160])  # Corresponding to platform heights
        enemies.add(Enemy(x, y))
    return enemies

# Game variables
round_number = 1
enemies = spawn_enemies(2)  # Start with 2 enemies
round_start_time = time.time()
countdown_start = None
score = 0
powerups = pygame.sprite.Group()

# Leaderboard
leaderboard = []

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def poweruptimer(player, powerup):
    if powerup == 'invincibility':
        player.invincible = True
        time.sleep(5)
        player.invincible = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update(platforms)
    for enemy in enemies:
        enemy.update(platforms, player)
    for platform in platforms:
        platform.update()

    # Check for collisions between player bullets and enemies
    for bullet in player.bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        for enemy in hit_enemies:
            bullet.kill()
            score += 10  # Increase score for each enemy killed
            powerup = enemy.die()
            if powerup:
                powerups.add(powerup)

        # Check for collisions between player bullets and platforms
        for platform in platforms:
            if platform.visible and bullet.rect.colliderect(platform.rect):
                bullet.kill()
                platform.hit()

    # Check for collisions between enemy bullets and player
    for enemy in enemies:
        for bullet in enemy.bullets:
            if pygame.sprite.collide_rect(bullet, player):
                if not player.invincible and not player.shield:
                    print(f"Game Over! Your score: {score}")
                    leaderboard.append(score)
                    leaderboard.sort(reverse=True)
                    leaderboard = leaderboard[:5]  # Keep only top 5 scores
                    running = False
                bullet.kill()
            
            # Check for collisions between enemy bullets and platforms
            for platform in platforms:
                if platform.visible and bullet.rect.colliderect(platform.rect):
                    bullet.kill()
                    platform.hit()

    # Check for collisions between player and enemies
    if pygame.sprite.spritecollide(player, enemies, False):
        if not player.invincible and not player.shield:
            print(f"Game Over! Your score: {score}")
            leaderboard.append(score)
            leaderboard.sort(reverse=True)
            leaderboard = leaderboard[:5]  # Keep only top 5 scores
            running = False

    # Check for powerup collisions
    collected_powerups = pygame.sprite.spritecollide(player, powerups, True)
    for powerup in collected_powerups:
        #if powerup.type == 'shield':
            #player.shield = True
            #player.invincibility_timer = pygame.time.get_ticks()
        if powerup.type == 'invincibility' and not player.invincible:
            thread = threading.Thread(target=poweruptimer, args=(player, powerup.type))
            thread.start()

    print(player.invincible)

    # Check if all enemies are defeated
    if len(enemies) == 0:
        if countdown_start is None:
            countdown_start = time.time()
        
        # 10 second countdown
        countdown = 10 - int(time.time() - countdown_start)
        if countdown <= 0:
            round_number += 1
            enemies = spawn_enemies(round_number + 1)  # Increase enemies each round
            countdown_start = None
            round_start_time = time.time()

    # Draw
    screen.fill(GRAY)
    player.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    powerups.draw(screen)

    # Draw HUD
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    round_text = font.render(f"Round: {round_number}", True, WHITE)
    screen.blit(round_text, (WIDTH - 120, 10))

    # Draw countdown if active
    if countdown_start is not None:
        countdown_text = font.render(f"Next round in: {countdown}", True, WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - 100, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over screen
screen.fill(BLACK)
game_over_text = font.render("Game Over", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 50))

# Display leaderboard
#leaderboard_text = font.render("Leaderboard:", True, WHITE)
#screen.blit(leaderboard_text, (WIDTH // 2 - 70, HEIGHT // 2 + 20))
#for i, score in enumerate(leaderboard):
#    score_text = font.render(f"{i+1}. {score}", True, WHITE)
#    screen.blit(score_text, (WIDTH // 2 - 40, HEIGHT // 2 + 60 + i * 30))

#pygame.display.flip()

# Wait for a few seconds before quitting
#pygame.time.wait(5000)

pygame.quit()
sys.exit()
