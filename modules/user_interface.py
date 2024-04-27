import pygame

pygame.init()
pygame.font.init()
font_for_text = pygame.font.SysFont('Comic Sans MS', 30)


class Interface(pygame.sprite.Sprite):
    def __init__(self, width, height, total_score):
        super().__init__()

        self.surf = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32)
        self.surf.convert_alpha()

        self.window_size = width, height
        self.health = 100
        self.cooldown = 0
        self.current_score = 0
        self.total_score = total_score
        self.alive = True

    def draw(self, screen):
        self.surf = pygame.surface.Surface(self.window_size, pygame.SRCALPHA, 32)
        self.surf.convert_alpha()
        if self.health == 0:
            self.death()
        if self.alive:
            balance_text = font_for_text.render(f'ТЕКУЩИЕ ОЧКИ: {self.current_score}', False, (255, 0, 0))
            total_text = font_for_text.render(f'РЕКОРД: {self.total_score}', False, (255, 0, 0))
            screen.blit(balance_text, (self.window_size[0] - balance_text.get_width() - 5, 5))
            screen.blit(total_text, (self.window_size[0] - total_text.get_width() - 5,
                                     total_text.get_height() + balance_text.get_rect().x))
            self.cooldown %= 101
            if self.cooldown < 100:
                self.cooldown += 1
            pygame.draw.rect(self.surf, (255, 0, 0), (0, 5, self.health * 3, 30))
            pygame.draw.rect(self.surf, (0, 0, 255),
                             (0, total_text.get_height() + balance_text.get_rect().x, self.cooldown * 3, 30))
        else:
            pass
        screen.blit(self.surf, (0, 0))

    def plus_score(self):
        self.current_score += 1

    def reduce_health(self):
        self.health -= 10

    def can_fire(self):
        return self.cooldown == 100

    def death(self):
        self.health = 0
        self.alive = False


def test():
    screen = pygame.display.set_mode()
    WIN_WIDTH, WIN_HEIGHT = pygame.display.get_window_size()
    interface = Interface(WIN_WIDTH, WIN_HEIGHT, 100)
    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        interface.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    test()
