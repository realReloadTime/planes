import pygame
from math import sin, cos, radians
pygame.init()


class Plane(pygame.sprite.Sprite):
    def __init__(self, coord, speed, src="data/pics/plane.png"):
        super().__init__()

        self.rect = coord
        self.speed = list(speed)
        self.image = pygame.image.load(src).convert_alpha()
        self.angle = 0

    def update(self, event):
        self.rect = (self.rect[0] + self.speed[0] * cos(radians(self.angle)),
                     self.rect[1] + self.speed[1] * sin(radians(self.angle)))
        print(self.rect)
        print(self.angle)
        print("----")
        if event.type == pygame.KEYDOWN:
            self.on_click_button(event.key)

    def on_click_button(self, key):
        if key == pygame.K_w or key == pygame.K_UP:
            self.angle += 2
            self.image = pygame.transform.rotate(self.image, self.angle)
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.angle -= 2
            self.image = pygame.transform.rotate(self.image, self.angle)
