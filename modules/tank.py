import pygame
from math import sin, cos, radians

pygame.init()


class Tank(pygame.sprite.Sprite):
    def __init__(self, coords, ground):
        super().__init__()

        self.name = 'tank'
        self.image = pygame.image.load("data/pics/tank.png")
        self.rect = pygame.Rect(coords[0], coords[1], self.image.get_width(), self.image.get_height())
        self.ground = ground
        self.on_ground = False

    def update(self):
        if not self.is_collided_with(self.ground):
            self.rect.y += 6
            self.image = pygame.image.load("data/pics/tank_extraction.png")
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
        else:
            self.on_ground = True
            self.image = pygame.image.load("data/pics/tank.png")
            self.rect = pygame.Rect(self.rect.x, self.ground.rect.y - self.ground.image.get_height() * 2,
                                    self.image.get_width(), self.image.get_height())
        self.image.set_colorkey((255, 255, 255))

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
