import pygame
pygame.font.init()


class InputText:
    def __init__(self, coords, font_size=32, text=''):
        self.text = text  # button text
        self.coords = coords

        self.font = pygame.font.SysFont('Comic Sans MS', font_size)
        self.text_sur = self.font.render(self.text, False, (0, 0, 0))
        self.surface = pygame.surface.Surface((300, 100))
        self.surface.set_colorkey(pygame.Color((255, 255, 255)))
        # self.surface.convert_alpha()
        pygame.draw.rect(self.surface, (255, 255, 255),
                         (0, 0, self.text_sur.get_width(), self.text_sur.get_height()))
        self.active = False
        self.rect = self.surface.get_rect()
        print(self.rect)

    def draw(self, screen):
        pygame.draw.rect(self.surface, (255, 255, 255),
                         (0, 0, self.text_sur.get_width(), self.text_sur.get_height()))
        self.surface.blit(self.text_sur, (0, 0))
        screen.blit(self.surface, self.coords)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.active = True
            print("WOW")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.active = False
            print("FOP " + str(event.pos))

        if self.active and event.type == pygame.KEYDOWN:
            if self.text[-1] == '|':
                self.text = self.text[:-1]
            self.text += event.text

        if self.active and self.text[-1] != '|':
            self.text += '|'
        elif self.active and self.text[-1] == '|':
            self.text = self.text[:-1]

        if self.active:
            self.text_sur = self.font.render(self.text, False, (0, 0, 0))


def test():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode()
    input_box = InputText((100, 500), text="Pffwf")
    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            input_box.update(event)
            if event.type == pygame.QUIT:
                return
        input_box.draw(screen)
        clock.tick(60)
        pygame.display.flip()


if __name__ == '__main__':
    test()