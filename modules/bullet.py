import pygame
from math import sin, cos, radians
pygame.init()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, coords, angle, speed, total_width, total_height):
        super().__init__()

        self.name = 'bullet'
        self.angle = angle
        self.image = pygame.image.load("data/pics/bullet.png")
        self.image = pygame.transform.rotozoom(self.image, -self.angle, .7)
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(coords[0], coords[1], self.image.get_width(), self.image.get_height())
        self.speed = speed
        self.W, self.H = total_width, total_height

    def update(self):
        self.rect.x = self.rect.x + self.speed * cos(radians(self.angle))
        self.rect.y = self.rect.y + self.speed * sin(radians(self.angle))
        if self.rect.x < 0 or self.rect.x > self.W or self.rect.y < 0 or self.rect.y > self.H:
            self.kill()

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)