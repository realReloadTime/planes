import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, name, source):
        super().__init__()

        self.name = name
        self.image = pygame.image.load(source)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())


class Ground(pygame.sprite.Sprite):  # bottom background
    def __init__(self, sky_height, source):
        super().__init__()

        self.name = 'ground'
        self.image = pygame.image.load(source)
        self.rect = pygame.Rect(0, sky_height, self.image.get_width(), self.image.get_height())
