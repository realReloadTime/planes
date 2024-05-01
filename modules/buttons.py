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
        self.surface = pygame.surface.Surface((self.text_sur.get_width(), self.text_sur.get_height()),
                                              pygame.SRCALPHA, 32)  # total surface
        self.surface.convert_alpha()
        if background_color is None:  # erase background
            pygame.draw.rect(self.surface, (0, 0, 0),
                             (0, 0, self.text_sur.get_width(), self.text_sur.get_height()), 1, 30)  # empty background
        else:
            pygame.draw.rect(self.surface, background_color,
                             (0, 0, self.text_sur.get_width(), self.text_sur.get_height()),
                             border_radius=30)  # background
        pygame.draw.rect(self.surface, self.text_color,
                         (0, 0, self.text_sur.get_width(), self.text_sur.get_height()), 2, 30)  # frame

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
                             2, 30)  # frame red
            self.text_sur = self.font.render(self.text, False,
                                             (255 - self.text_color[0],
                                              255 - self.text_color[1],
                                              255 - self.text_color[2]))  # revert colors
            self.surface.blit(self.text_sur, (0, 0))
        else:
            pygame.draw.rect(self.surface, self.text_color,
                             (0, 0, self.text_sur.get_width(), self.text_sur.get_height()),
                             2, 30)  # frame
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


class Label:
    def __init__(self, coords, text, text_color=(0, 0, 0), font_size=32):
        self.text = text  # text
        self.text_color = text_color
        self.coords = list(coords)  # surface coords

        self.font = pygame.font.SysFont('Comic Sans MS', font_size)  # font for text (object)
        self.text_sur = self.font.render(self.text, False, self.text_color)  # text surface

        self.width, self.height = self.text_sur.get_width(), self.text_sur.get_height()
        self.surface = pygame.surface.Surface((self.text_sur.get_width(), self.text_sur.get_height()),
                                              pygame.SRCALPHA, 32)  # total surface
        self.surface.convert_alpha()

    def draw(self, screen):  # draw label on screen
        self.surface.blit(self.text_sur, (0, 0))
        screen.blit(self.surface, self.coords)

    def edit_text(self, text):  # function for optimize editing text on label
        self.text = text
        self.text_sur = self.font.render(self.text, False, self.text_color)  # text surface
        self.coords = [self.coords[0] - (self.text_sur.get_width() - self.width),
                       self.coords[1] - (self.text_sur.get_height() - self.height)]
        self.width, self.height = self.text_sur.get_width(), self.text_sur.get_height()
        self.surface = pygame.surface.Surface((self.text_sur.get_width(), self.text_sur.get_height()),
                                              pygame.SRCALPHA, 32)  # total surface
        self.surface.convert_alpha()

    def centerize(self, window_width, window_height, vertical=False):  # centerizes label on screen
        if vertical:
            self.coords[1] = window_height / 2 - self.height / 2
        else:
            self.coords[0] = window_width / 2 - self.width / 2

    def rightize(self, window_width,
                 window_height=None):  # rightizes label on screen (if window_height != None moves to label UP too)
        self.coords[0] = window_width - self.width - 10
        if window_height:
            self.coords[1] = self.height
        print(self.coords)


# https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame (function down)


def add_outline_to_image(image: pygame.Surface, thickness: int, color: tuple,
                         color_key: tuple = (255, 0, 255)) -> pygame.Surface:
    mask = pygame.mask.from_surface(image)
    mask_surf = mask.to_surface(setcolor=color)
    mask_surf.set_colorkey((0, 0, 0))

    new_img = pygame.Surface((image.get_width() + 2, image.get_height() + 2))
    new_img.fill(color_key)
    new_img.set_colorkey(color_key)

    for i in -thickness, thickness:
        new_img.blit(mask_surf, (i + thickness, thickness))
        new_img.blit(mask_surf, (thickness, i + thickness))
    new_img.blit(image, (thickness, thickness))

    return new_img
