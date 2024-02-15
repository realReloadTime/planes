import pygame
from modules.plane import Plane
from modules.camera import Camera

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("")
WIN_WIDTH, WIN_HEIGHT = pygame.display.get_window_size()
repeat = False


class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("data/pics/sky.png")
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())


class Ground(pygame.sprite.Sprite):
    def __init__(self, sky_height):
        super().__init__()

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
    sky = Sky()
    ground = Ground(sky.image.get_height())
    plane = Plane((0, 1500))
    total_width = ground.image.get_width()
    total_height = ground.image.get_height() + sky.image.get_height()
    camera = Camera(camera_configure, total_width, total_height)

    entities = pygame.sprite.Group()
    timer = pygame.time.Clock()
    FPS = 60

    entities.add(sky)
    entities.add(ground)
    entities.add(plane)
    # entities.add()

    move = False
    cur_key = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    global repeat
                    repeat = not repeat
                    if repeat:
                        main()
                        return
                move = True
                cur_key = event.key
            elif event.type == pygame.KEYUP:
                move = False

        if move:
            plane.clicked_button(cur_key)
        if plane.rect.x > total_width + plane.rect.width // 2:
            plane.rect.x = -plane.rect.width // 2
        if plane.rect.y > total_height - ground.rect.height:
            plane.death()
        if plane.rect.x < -plane.rect.width:
            plane.rect.x = total_width
        if plane.rect.y < -plane.rect.width - 50:
            plane.angle = -plane.angle + 2
            plane.clicked_button(pygame.K_w)
            plane.rect.y = -plane.rect.height - 20
        camera.update(plane)
        plane.update()
        entities.draw(screen)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()
        timer.tick(FPS)


if __name__ == '__main__':
    main()
