import pygame.key
import pygame.sprite
import pygame as p
import random
from settings import *


class Ship:
    def __init__(self, pos, images):
        self.image = images[0]
        self.images = images
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hp = 4
        self.score = 0
        self.start_pos = pos

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, target_surf):
        if self.hp > 0:
            target_surf.blit(self.image, self.rect)
            if self.hp < 4:
                target_surf.blit(self.images[-self.hp], self.rect)

    def get_damage(self, damage):
        if self.hp > 0:
            self.hp -= damage

    def rebuild(self):
        self.rect.center = self.start_pos
        self.hp = 4
        self.score = 0


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(3, 9)


    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_y = 10

    def update(self):
        self.rect.y -= self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class Button(p.sprite.Sprite):
    def __init__(self, pos, text, font):
        super().__init__()
        self.image = p.Surface((360, 80))
        self.image.fill('YELLOW')
        self.rect = self.image.get_rect(center=pos)

        self.text_surf, self.text_rect = font.render(text, size=42)
        self.text_rect.center = self.rect.center

    def draw(self, target_surf):
         target_surf.blit(self.image, self.rect)
         target_surf.blit(self.text_surf, self.text_rect)

