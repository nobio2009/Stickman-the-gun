import pygame
import time

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, indestructible=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3
        self.indestructible = indestructible
        self.visible = True
        self.respawn_time = None

    def hit(self):
        if not self.indestructible:
            self.health -= 1
            if self.health <= 0:
                self.visible = False
                self.respawn_time = time.time() + 5  # Respawn after 5 seconds
                return True
        return False

    def update(self):
        if not self.visible and time.time() > self.respawn_time:
            self.visible = True
            self.health = 3
            self.kill()

    def draw(self, screen):
        print(self.visible)
        if self.visible:
            screen.blit(self.image, self.rect)
