import pygame
from random import randint
pygame.init()


class TimeShift(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()

        self.name = 'timeshift'
        self.image = pygame.image.load('data/pics/timeshift.png')
        self.image.set_colorkey((255, 255, 255))
        self.coords = coords

        self.rect = pygame.Rect(coords[0], coords[1], 75, 75)
        self.oldspeed = 8
        self.ondoing_counter = 0

    def draw(self, screen):
        screen.blit(self.image, self.coords)

    def collided(self, plane, interface):
        if plane.is_collided_with(self):
            interface.timeb = True
            if self.ondoing_counter == 0:
                self.oldspeed = plane.speed
                self.ondoing_counter = 300
                self.image = pygame.transform.scale(self.image, (0, 0))
        if self.ondoing_counter > 1:
            plane.speed = 5
            self.ondoing_counter -= 1
        elif self.ondoing_counter == 1:
            plane.speed = self.oldspeed
            interface.timeb = False
            self.ondoing_counter = 0
            self.rect.x = randint(100, 5200)
            self.rect.y = randint(400, 1500)
            self.image = pygame.image.load('data/pics/timeshift.png')


class BulletInfinity(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()

        self.name = 'bullinf'
        self.image = pygame.image.load('data/pics/bullinfinity.png')
        self.image.set_colorkey((255, 255, 255))
        self.coords = coords

        self.rect = pygame.Rect(coords[0], coords[1], 75, 75)
        self.ondoing_counter = 0

    def draw(self, screen):
        screen.blit(self.image, self.coords)

    def collided(self, plane, interface):
        if plane.is_collided_with(self):
            interface.bullb = True
            if self.ondoing_counter == 0:
                self.ondoing_counter = 300
                self.image = pygame.transform.scale(self.image, (0, 0))
        if self.ondoing_counter > 1:
            interface.cooldown = 100
            self.ondoing_counter -= 1
        elif self.ondoing_counter == 1:
            self.ondoing_counter = 0
            interface.bullb = False
            self.rect.x = randint(100, 5200)
            self.rect.y = randint(400, 1500)
            self.image = pygame.image.load('data/pics/bullinfinity.png')
