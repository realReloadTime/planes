import pygame
from math import sin, cos, radians
pygame.init()


class Plane(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()

        self.image = pygame.image.load("data/pics/plane.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(coords[0], coords[1], self.image.get_width(), self.image.get_height())
        self.angle = 0

    def update(self):
        self.rect.x += cos(radians(self.angle)) * 10
        self.rect.y += sin(radians(self.angle)) * 10

    def clicked_button(self, key):
        if key == pygame.K_w or key == pygame.K_UP:
            self.angle -= 2
            self.image.set_colorkey((255, 255, 255))
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.angle += 2
            self.image.set_colorkey((255, 255, 255))