import pygame

pygame.font.init()


class InputText:
    def __init__(self, coords, font_size=32, text=''):
        self.text = text  # button text
        self.coords = coords

        self.font = pygame.font.SysFont('Comic Sans MS', font_size)
        self.text_sur = self.font.render(self.text, False, (0, 0, 0))
        self.surface = pygame.surface.Surface((300, 50))

        self.active = False
        self.rect = pygame.rect.Rect(coords[0], coords[1], self.surface.get_width(), self.surface.get_height())

    def draw(self, screen):
        size_w = max(300, self.text_sur.get_width())
        self.surface = pygame.surface.Surface((size_w, self.rect.height))
        pygame.draw.rect(self.surface, (255, 255, 255),
                         (0, 0, size_w, self.surface.get_height()), self.rect.height)
        if self.active:
            pygame.draw.rect(self.surface, (200, 0, 0), (0, 0, size_w, self.surface.get_height()), 2)
        else:
            pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, size_w, self.surface.get_height()), 2)
        self.surface.blit(self.text_sur, (0, 0))
        screen.blit(self.surface, (self.rect.left, self.rect.top))

    def update(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN and (self.rect[0] <= event.pos[0] <= self.rect[0] + self.rect[2]) and
                (self.rect[1] <= event.pos[1] <= (self.rect[1] + self.rect[3]))):   # set active field (can enter)
            self.active = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # set NOT active field
            self.active = False

        if self.active:  # field activated and ...
            if '|' in self.text:
                self.text = ''.join(self.text.split('|'))
            if event.type == pygame.KEYDOWN:
                if (event.key != pygame.K_BACKSPACE and len(pygame.key.name(event.key)) == 1 and
                        pygame.key.get_mods() & pygame.KMOD_SHIFT):  # capitalizes letter if pressed SHIFT
                    self.text += pygame.key.name(event.key).capitalize()
                elif event.key != pygame.K_BACKSPACE and len(pygame.key.name(event.key)) == 1:  # pressed text button
                    self.text += pygame.key.name(event.key)
                elif event.key == pygame.K_BACKSPACE and len(self.text) > 1:  # pressed backspace
                    self.text = self.text[:-1]
                elif event.key == pygame.K_BACKSPACE and len(self.text) == 1:  # pressed backspace and text 'll be empty
                    self.text = ''
            self.text += '|'
        else:
            if '|' in self.text:
                self.text = ''.join(self.text.split('|'))
        self.text_sur = self.font.render(self.text, False, (0, 0, 0))


def test():  # testing function (not uses in MAIN run)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode()
    input_box = InputText((100, 500), text="ABoBa")
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            input_box.update(event)
            if event.type == pygame.QUIT:
                return
        input_box.draw(screen)
        clock.tick(60)
        pygame.display.flip()


if __name__ == '__main__':
    test()
