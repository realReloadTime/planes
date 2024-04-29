import pygame
pygame.font.init()


class ButtonText(pygame.sprite.Sprite):
    def __init__(self, coords, text, font_size, action, text_color=(0, 0, 0), background_color=None):
        super().__init__()

        self.action = action  # action on click
        self.text = text  # button text
        self.text_color = text_color

        self.font = pygame.font.SysFont('Comic Sans MS', font_size)  # font for text (object)
        self.text_sur = self.font.render(self.text, False, self.text_color)  # text surface on button
        self.surface = pygame.surface.Surface((self.text_sur.get_width(), self.text_sur.get_height()))  # total surface
        if background_color is None:  # erase background
            self.surface = pygame.surface.Surface((self.text_sur.get_width(), self.text_sur.get_height()),
                                                  pygame.SRCALPHA, 32)
            self.surface.convert_alpha()
            pygame.draw.rect(self.surface, (0, 0, 0),
                             (0, 0, self.text_sur.get_width(), self.text_sur.get_height()), 1, 1)  # empty background
        else:
            self.surface = pygame.surface.Surface((self.text_sur.get_width(), self.text_sur.get_height()))
            pygame.draw.rect(self.surface, background_color,
                             (0, 0, self.text_sur.get_width(), self.text_sur.get_height()))  # background
        pygame.draw.rect(self.surface, self.text_color,
                         (0, 0, self.text_sur.get_width(), self.text_sur.get_height()), 2)  # frame

        self.surface.blit(self.text_sur, (0, 0))
        self.rect = [coords[0], coords[1], self.text_sur.get_width(), self.text_sur.get_height()]

    def update(self, event):
        mouse_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and (
                self.rect[0] <= mouse_pos[0] <= (self.rect[0] + self.rect[2]) and self.rect[1] <= mouse_pos[1] <=
                (self.rect[1] + self.rect[3])):
            self.action()
            return True
        elif (self.rect[0] <= mouse_pos[0] <= (self.rect[0] + self.rect[2]) and
              self.rect[1] <= mouse_pos[1] <= (self.rect[1] + self.rect[3])):
            pygame.draw.rect(self.surface,
                             (255 - self.text_color[0],
                              255 - self.text_color[1],
                              255 - self.text_color[2]), (0, 0, self.text_sur.get_width(), self.text_sur.get_height()),
                             2)  # frame red
            self.text_sur = self.font.render(self.text, False,
                                             (255 - self.text_color[0],
                                              255 - self.text_color[1],
                                              255 - self.text_color[2]))  # revert colors
            self.surface.blit(self.text_sur, (0, 0))
        else:
            pygame.draw.rect(self.surface, self.text_color,
                             (0, 0, self.text_sur.get_width(), self.text_sur.get_height()),
                             2)  # frame
            self.text_sur = self.font.render(self.text, False, self.text_color)  # text surface on button
            self.surface.blit(self.text_sur, (0, 0))
        return False

    def draw(self, screen):
        screen.blit(self.surface, (self.rect[0], self.rect[1]))

    def centerize(self):
        self.rect[0] = self.rect[0] - self.rect[2] // 2
        self.rect[1] = self.rect[1] - self.rect[3] // 2


class ButtonIcon(pygame.sprite.Sprite):
    def __init__(self, coords, source, source2, action):
        super().__init__()

        self.coords = coords
        self.pics = [source, source2]
        self.image = pygame.image.load(self.pics[0])
        self.image.set_colorkey((255, 255, 255))
        self.rect = [self.coords[0], self.coords[1], self.image.get_width(), self.image.get_height()]
        self.status = True
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, (self.rect[0], self.rect[1]))

    def update(self, event):
        mouse_pos = event.pos
        if self.rect[0] <= mouse_pos[0] <= (self.rect[0] + self.rect[2]) and \
                self.rect[1] <= mouse_pos[1] <= (self.rect[1] + self.rect[3]):
            self.cross_image()
            self.action()
            return True

    def cross_image(self):
        self.status = not self.status
        if self.status:
            self.image = pygame.image.load(self.pics[0])
        else:
            self.image = pygame.image.load(self.pics[1])
        self.image.set_colorkey((255, 255, 255))
        self.rect = [self.rect[0], self.rect[1], self.image.get_width(), self.image.get_height()]
