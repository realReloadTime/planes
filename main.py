import pygame
from modules.plane import Plane
from modules.camera import Camera
from modules.tank import Tank
from modules.bullet import Bullet
from random import randint

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("")
WIN_WIDTH, WIN_HEIGHT = pygame.display.get_window_size()
FPS = 60


class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.name = 'sky'
        self.image = pygame.image.load("data/pics/sky.png")
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())


class Ground(pygame.sprite.Sprite):
    def __init__(self, sky_height):
        super().__init__()

        self.name = 'ground'
        self.image = pygame.image.load("data/pics/ground.png")
        self.rect = pygame.Rect(0, sky_height, self.image.get_width(), self.image.get_height())


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


def main():
    repeat = False
    balance = 0

    sky = Sky()
    ground = Ground(sky.image.get_height())
    plane = Plane((0, 1150), sky.rect.height)
    total_width = ground.image.get_width()
    total_height = ground.image.get_height() + sky.image.get_height()
    print(total_height, total_width)
    camera = Camera(camera_configure, total_width, total_height)
    font_for_text = pygame.font.SysFont('Comic Sans MS', 30)

    entities = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    timer = pygame.time.Clock()

    entities.add(sky)
    entities.add(ground)
    entities.add(plane)
    for i in range(5):
        entities.add(Tank((randint(800, total_width), randint(0, sky.rect.height - ground.rect.height)), sky.rect.height, ground.rect.height))

    move = False
    cur_key = None
    running = True
    while running:
        balance_text = font_for_text.render(f'ТЕКУЩИЕ ОЧКИ: {balance}', False, (0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    repeat = not repeat
                    if repeat:
                        main()
                        return
                if event.key == pygame.K_1:
                    plane.death()
                if event.key == pygame.K_SPACE and plane.alive:
                    new_bullet = Bullet((plane.rect.x, plane.rect.y), plane.angle, 20, total_width, total_height)
                    entities.add(new_bullet)
                    bullets.add(new_bullet)
                move = True
                cur_key = event.key
            elif event.type == pygame.KEYUP:
                move = False

        if move:
            plane.clicked_button(cur_key)
        if plane.rect.x > total_width + plane.rect.width // 2:
            plane.rect.x = -plane.rect.width // 2
        if plane.rect.x < -plane.rect.width:
            plane.rect.x = total_width
        if plane.rect.y < -plane.rect.width - 50:
            plane.angle = -plane.angle + 2
            plane.clicked_button(pygame.K_w)
            plane.rect.y = -plane.rect.height - 20
        camera.update(plane)
        plane.update()
        for e in entities:

            if e.name == 'tank' or e.name == 'bullet':
                e.update()
            if plane.is_collided_with(e) and (e.name == 'tank' or e.name == 'ground'):
                plane.death()
                if e.name == 'tank':
                    balance += 1
                    e.kill()
            for b in bullets:
                if b.is_collided_with(e) and e.name == 'tank':
                    balance += 1
                    b.kill()
                    e.kill()
                    entities.add(Tank((randint(max(plane.rect.x + 500, 1000), total_width), randint(0, sky.rect.height - ground.rect.height)),
                                      sky.rect.height, ground.rect.height))
            screen.blit(e.image, camera.apply(e))
        screen.blit(balance_text, (WIN_WIDTH - balance_text.get_width(), balance_text.get_height()))
        pygame.display.update()
        timer.tick(FPS)


if __name__ == '__main__':
    main()
