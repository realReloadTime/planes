import pygame
from math import sin, cos, radians

pygame.init()


class Tank(pygame.sprite.Sprite):
    def __init__(self, coords, ground):
        super().__init__()

        self.name = 'tank'
        self.statuses = [pygame.image.load("data/pics/tank.png"), pygame.image.load("data/pics/tank_extraction.png")]
        self.image = self.statuses[0]
        self.rect = pygame.Rect(coords[0], coords[1], self.image.get_width(), self.image.get_height())
        self.ground = ground
        self.size = 1
        self.death = False
        self.on_ground = False

    def update(self):
        if not self.is_collided_with(self.ground) and not self.on_ground:
            self.rect.y += 6
            self.image = self.statuses[1]
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
        else:
            self.on_ground = True
            self.image = self.statuses[0]
            self.rect = pygame.Rect(self.rect.x, self.ground.rect.y - self.ground.image.get_height() * 2,
                                    self.image.get_width(), self.image.get_height())
        if self.death:
            self.image = pygame.transform.rotozoom(self.image, 0, self.size)
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
            self.size -= 0.1
        if self.size == 0:
            self.kill()
        self.image.set_colorkey((255, 255, 255))

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
