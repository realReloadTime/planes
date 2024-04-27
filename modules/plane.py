import pygame
from math import sin, cos, radians
pygame.init()


class Plane(pygame.sprite.Sprite):  # REWRITE ROTATE MOVE
    def __init__(self, coords, sky_height):
        super().__init__()

        self.name = 'plane'
        self.sky_height = sky_height
        self.image = pygame.image.load("data/pics/plane.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
        self.orig_image = self.image
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(coords[0], coords[1], self.image.get_width(), self.image.get_height())
        self.angle = 0
        self.alive = True
        self.speed = 6

    def update(self):
        if self.alive:
            self.rect.x += cos(radians(self.angle)) * self.speed
            self.rect.y -= sin(radians(self.angle)) * self.speed
        else:
            if self.rect.y < self.sky_height:
                self.rect.y += 4

    def clicked_button(self, key):
        if self.alive:
            if key == pygame.K_w or key == pygame.K_UP:
                self.angle += 2 / 5 * self.speed
            elif key == pygame.K_s or key == pygame.K_DOWN:
                self.angle -= 2 / 5 * self.speed
            self.image = rotate(self.orig_image, (self.rect.left, self.rect.top),
                                (self.orig_image.get_width() / 2, self.orig_image.get_height() / 2), self.angle)[0]
            self.image.set_colorkey((255, 255, 255))

    def death(self):
        self.alive = False
        self.image = pygame.image.load("data/pics/explosion.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)


def rotate(image, pos, origin_pos, angle):  # pos - pos of img, origin_pos - pos of center REWRITE
    # offset from pivot to center
    image_rect = image.get_rect(center=(pos[0] - origin_pos[0], pos[1] - origin_pos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # rotated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # rotated image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    return rotated_image, rotated_image_rect
