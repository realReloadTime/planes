import pygame
import json
from modules.plane import Plane
from modules.camera import Camera
from modules.tank import Tank
from modules.bullet import Bullet
from modules.buttons import ButtonText, ButtonIcon
from random import randint

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("САМОЛЕТИК")
WIN_WIDTH, WIN_HEIGHT = pygame.display.get_window_size()
FPS = 60

settings = json.load(open('data/settings.json', 'r'))
if "total_score" not in settings:
    settings["total_score"] = 0
if "music" not in settings:
    settings["music"] = 1
font_for_text = pygame.font.SysFont('Comic Sans MS', 30)
pygame.mixer.music.load("data/audis/alexander-nakarada-near-end-action.mp3")
if settings["music"]:
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1)
fly_sound = pygame.mixer.Sound('data/audis/flying_plane (mp3cut.net).wav')
bul_sound = pygame.mixer.Sound('data/audis/attack (mp3cut.net).wav')


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


def clicked_start():
    print('Начинаем игру')


button_volume = ButtonIcon((WIN_WIDTH // 2, 0), "data/pics/volume_on.png",
                           "data/pics/volume_off.png", 1)
button_volume.rect[1] = WIN_HEIGHT - button_volume.rect[3]


def sound_check():
    if button_volume.status:
        pygame.mixer.music.unpause()
        settings["music"] = 1
    else:
        pygame.mixer.music.pause()
        settings["music"] = 0
    print(settings["music"], button_volume.status)


button_volume.action = sound_check


def preview():  # menu screen
    running = True
    button_start = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 2), ' НАЧАТЬ ', 150, clicked_start,
                              (0, 255, 0), (0, 0, 255))
    button_start.centerize()
    texts = ['В этой игре нужно управлять самолетом и уничтожать вражескую технику.',
             'Столкновение с землей и чужой техникой может привести к смерти.', '',
             'Управление:', 'ДВИЖЕНИЕ - Стрелки вверх/вниз или W/S,',
             'СТРЕЛЬБА - Пробел,', 'R - перезапуск, 1 - самоуничтожение']
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            if (event.type == pygame.MOUSEBUTTONDOWN or
                event.type == pygame.MOUSEMOTION) and button_start.update(event):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_volume.update(event)
        screen.fill((0, 0, 0))
        for text in texts:
            txt = font_for_text.render(text, False, (255, 255, 255))
            screen.blit(txt, ((WIN_WIDTH - txt.get_width()) // 2, txt.get_height() * texts.index(text) + 5))
        button_start.draw(screen)
        button_volume.draw(screen)
        pygame.display.flip()
    main()


def main():  # game cycle
    balance = 0  # current score
    prev_balance = 0  # previous score for editing speed plane
    sky = Sky()  # sky box
    ground = Ground(sky.image.get_height())  # ground box
    plane = Plane((0, 1150), sky.rect.height)  # main character
    total_width = ground.image.get_width()  # get size of window
    total_height = ground.image.get_height() + sky.image.get_height()
    print(total_height, total_width)
    camera = Camera(camera_configure, total_width, total_height)  # camera on main character

    entities = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    timer = pygame.time.Clock()

    entities.add(sky)
    entities.add(ground)
    entities.add(plane)
    for i in range(5):
        entities.add(Tank((randint(800, total_width), randint(0, 200)), ground))

    move = False
    cur_key = None
    running = True
    fly_sound.play(-1)
    while running:
        balance_text = font_for_text.render(f'ТЕКУЩИЕ ОЧКИ: {balance}', False, (0, 0, 0))
        total_text = font_for_text.render(f'РЕКОРД: {settings["total_score"]}', False, (150, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             event.key == pygame.K_ESCAPE):  # exit event
                running = False
                if balance > settings["total_score"]:
                    settings["total_score"] = balance
                break
            elif event.type == pygame.KEYDOWN:  # button pressed
                if event.key == pygame.K_r:  # restart button (R)
                    if balance > settings["total_score"]:
                        settings["total_score"] = balance
                    main()
                    return
                if event.key == pygame.K_1:  # suicide button (1)
                    plane.death()
                if event.key == pygame.K_SPACE and plane.alive:  # fire button (SPACE)
                    bul_sound.play()
                    new_bullet = Bullet((plane.rect.x, plane.rect.y), plane.angle,
                                        20, total_width, total_height)  # create new button
                    entities.add(new_bullet)  # add to layout
                    bullets.add(new_bullet)  # add to group of buttons
                move = True  # is plane rotating?
                cur_key = event.key
            elif event.type == pygame.KEYUP:  # event to stop rotating plane
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
                if e.name == 'tank' and not e.death:
                    balance += 1
                    plane.death()
                    e.death = True
                elif e.name == 'ground':
                    plane.death()
            for b in bullets:
                if b.is_collided_with(e) and e.name == 'tank' and not e.death:
                    balance += 1
                    b.kill()
                    e.death = True
                    entities.add(Tank((randint(0, total_width - 200), randint(-200, 300)), ground))
                    break
            screen.blit(e.image, camera.apply(e))
        screen.blit(balance_text, (WIN_WIDTH - balance_text.get_width() - 5, 5))
        screen.blit(total_text, (WIN_WIDTH - total_text.get_width() - 5,
                                 total_text.get_height() + balance_text.get_height()))
        pygame.display.flip()
        timer.tick(FPS)
        if balance % 5 == 0 and balance != 0 and prev_balance != balance:
            plane.speed += .5
        prev_balance = balance
    if not plane.alive:
        fly_sound.stop()
    json.dump(settings, open('data/settings.json', 'w'))


if __name__ == '__main__':
    preview()  # preview screen(menu)
