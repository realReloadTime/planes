import pygame
from random import choice
pygame.init()


class Tank(pygame.sprite.Sprite):
    def __init__(self, coords, ground):
        super().__init__()

        self.name = 'tank'
        numb = choice(('1', '2'))
        self.statuses = [pygame.transform.scale(pygame.image.load(f"data/pics/newtank{numb}.png"), (600, 203)),
                         pygame.transform.scale(pygame.image.load(f"data/pics/extr{numb}.png"), (748, 693)),
                         pygame.image.load("data/pics/explosion.png")]
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
            self.rect = pygame.Rect(self.rect.x, self.ground.rect.y - self.ground.image.get_height() - 60,
                                    self.image.get_width(), self.image.get_height())
        if self.death:
            self.image = pygame.transform.rotozoom(self.statuses[2], 0, self.size)
            self.rect = pygame.Rect(self.rect.x, self.rect.y + self.image.get_height(), self.image.get_width(),
                                    self.image.get_height())
            self.size -= 0.01
        if self.size == 0:
            self.kill()
        self.image.set_colorkey((255, 255, 255))

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)


class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self, coords, ground):
        super().__init__()

        self.name = 'enemy_plane'
        self.statuses = [pygame.image.load("data/pics/enemy_plane2 (1).png"),
                         pygame.image.load("data/pics/enemy_plane2 (2).png"),
                         pygame.image.load("data/pics/explosion.png")]
        self.ground = ground
        if max(coords[0], self.ground.rect.width - coords[0]) == coords[0]:
            self.image = self.statuses[1]
            self.motion = 1
            self.rect = pygame.Rect(0, coords[1], self.image.get_width(), self.image.get_height())
        else:
            self.image = self.statuses[0]
            self.motion = -1
            self.rect = pygame.Rect(self.ground.rect.width, coords[1], self.image.get_width(), self.image.get_height())
        self.image.set_colorkey((255, 255, 255))
        self.speed = 5
        self.alive = True
        self.on_ground = False

    def death(self):
        self.alive = False
        self.image = self.statuses[2]
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())

    def update(self):
        if self.alive:
            self.rect.x += self.speed * self.motion
            if not(0 <= self.rect.x <= self.ground.rect.width):
                self.kill()
        else:
            if self.rect.y < self.ground.rect.height + 30:
                self.rect.y += 2
            else:
                self.kill()
