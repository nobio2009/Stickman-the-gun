import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.invincible = True
        self.shield = False
        self.invincibility_timer = 0
        self.load_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.jumping = False
        self.bullets = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 500  # Delay between shots in milliseconds
        self.facing_right = True  # New attribute to track facing direction

    def load_image(self):
        if os.path.exists("blood_angel.png"):
            self.image = pygame.image.load("blood_angel.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 60))
        else:
            self.image = pygame.Surface((40, 60))
            self.image.fill((255, 0, 0))  # Red color for Blood Angel

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5
            self.facing_right = True

        # Jumping
        if keys[pygame.K_SPACE] and not self.jumping:
            self.velocity_y = -20
            self.jumping = True

        # Shooting
        if keys[pygame.K_e]:
            self.shoot()

        # Apply gravity
        self.velocity_y += 0.8
        self.rect.y += self.velocity_y

        # Check for collisions with platforms
        for platform in platforms:
            if not platform.visible:
                continue
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.jumping = False
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        # Update bullets
        self.bullets.update()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.facing_right)
            self.bullets.add(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_right):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 255, 0))  # Yellow color for bullet
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = 1 if direction_right else -1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > 800:  # Remove bullet if it goes off-screen
            self.kill()
 
