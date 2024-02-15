import pygame
from math import sin, cos, radians
pygame.init()


class Tank(pygame.sprite.Sprite):
    def __init__(self, coords, sky_height, ground_height):
        super().__init__()

        self.name = 'tank'
        self.image = pygame.image.load("data/pics/tank.png")
        self.rect = pygame.Rect(coords[0], coords[1], self.image.get_width(), self.image.get_height())
        self.sky_height = sky_height
        self.ground_height = ground_height

    def update(self):
        if self.rect.y < self.sky_height - self.ground_height:
            self.rect.y += 6
            self.image = pygame.image.load("data/pics/tank_extraction.png")
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
        else:
            self.image = pygame.image.load("data/pics/tank.png")
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
        self.image.set_colorkey((255, 255, 255))

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
