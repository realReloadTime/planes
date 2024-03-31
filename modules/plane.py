import pygame
from math import sin, cos, radians
pygame.init()


class Plane(pygame.sprite.Sprite):
    def __init__(self, coords, sky_height):
        super().__init__()

        self.name = 'plane'
        self.sky_height = sky_height
        self.image = pygame.image.load("data/pics/plane.png")
        self.orig_image = self.image
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(coords[0], coords[1], self.image.get_width(), self.image.get_height())
        self.angle = 0
        self.alive = True
        self.speed = 5

    def update(self):
        if self.alive:
            self.rect.x += cos(radians(self.angle)) * self.speed
            self.rect.y += sin(radians(self.angle)) * self.speed
        else:
            if self.rect.y < self.sky_height:
                self.rect.y += 4

    def clicked_button(self, key):
        if self.alive:
            if key == pygame.K_w or key == pygame.K_UP:
                self.angle -= 2 / 5 * self.speed
                self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
                self.image.set_colorkey((255, 255, 255))
            elif key == pygame.K_s or key == pygame.K_DOWN:
                self.angle += 2 / 5 * self.speed
                self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
                self.image.set_colorkey((255, 255, 255))

    def death(self):
        self.alive = False
        self.image = pygame.image.load("data/pics/explosion.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
