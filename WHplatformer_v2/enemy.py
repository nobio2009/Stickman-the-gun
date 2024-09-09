import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((255, 0, 0))  # Red color for enemies
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.jump_power = -10
        self.gravity = 0.5
        self.on_ground = False
        self.direction = random.choice([-1, 1])  # Random initial direction
        self.speed = 2
        self.bullets = pygame.sprite.Group()
        self.ai_active = False

    def update(self, platforms, player):
        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if not platform.visible:
                continue
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.ai_active = True  # Activate AI when hitting the ground
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        if self.ai_active:
            # Move horizontally
            self.rect.x += self.speed * self.direction

            # Change direction if at screen edge or randomly
            if self.rect.left < 0 or self.rect.right > 800 or random.random() < 0.02:
                self.direction *= -1

            # Jump randomly when on ground
            if self.on_ground and random.random() < 0.01:
                self.jump()

            # Shoot at player
            if random.random() < 0.02:
                self.shoot(player)

        # Update bullets
        self.bullets.update()

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power

    def shoot(self, player):
        bullet = Bullet(self.rect.centerx, self.rect.centery, player.rect.center)
        self.bullets.add(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)

    def die(self):
        powerup_type = random.choice(['invincibility'])
        return Powerup(self.rect.centerx, self.rect.centery, powerup_type)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 0))  # Yellow color for enemy bullets
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        angle = math.atan2(target[1] - y, target[0] - x)
        self.velocity = (math.cos(angle) * self.speed, math.sin(angle) * self.speed)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.left < 0 or self.rect.right > 800 or self.rect.top < 0 or self.rect.bottom > 600:
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0) if type == 'shield' else (255, 255, 0))  # Green for shield, yellow for invincibility
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
