import pygame


class ButtonText(pygame.sprite.Sprite):
    def __init__(self, coords, text, font_size, action, text_color=(0, 0, 0), backgr_color=(255, 255, 255)):
        super().__init__()

        self.font = pygame.font.SysFont('Comic Sans MS', font_size)
        self.action = action
        self.text = self.font.render(text, False, text_color)
        self.text_color = text_color
        self.backgr = pygame.surface.Surface((self.text.get_width(), self.text.get_height()))
        pygame.draw.rect(self.backgr, backgr_color, (0, 0, self.text.get_width(), self.text.get_height()))  # background
        pygame.draw.rect(self.backgr, text_color, (0, 0, self.text.get_width(), self.text.get_height()), 2)  # frame

        self.backgr.blit(self.text, (0, 0))
        self.rect = [coords[0], coords[1], self.text.get_width(), self.text.get_height()]

    def update(self, event):
        mouse_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and (
                self.rect[0] <= mouse_pos[0] <= (self.rect[0] + self.rect[2]) and self.rect[1] <= mouse_pos[1] <=
                (self.rect[1] + self.rect[3])):
            self.action()
            return True
        elif (self.rect[0] <= mouse_pos[0] <= (self.rect[0] + self.rect[2]) and self.rect[1] <= mouse_pos[1] <= (self.rect[
            1] + self.rect[3])):
            pygame.draw.rect(self.backgr, (255, 0, 0), (0, 0, self.text.get_width(), self.text.get_height()),
                             2)  # frame red
        else:
            pygame.draw.rect(self.backgr, self.text_color, (0, 0, self.text.get_width(), self.text.get_height()),
                             2)  # frame
        return False

    def draw(self, screen):
        screen.blit(self.backgr, (self.rect[0], self.rect[1]))

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