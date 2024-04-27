import pygame
import json
from modules.plane import Plane
from modules.camera import Camera
from modules.tank import Tank
from modules.bullet import Bullet
from modules.buttons import ButtonText, ButtonIcon
from modules.background import Background, Ground
from modules.user_interface import Interface
from random import randint

pygame.init()  # always uses
pygame.font.init()  # ||-||-||
# ---------------------

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # here's blits all elements of gameplay
pygame.display.set_caption("САМОЛЕТИК")  # just title for app
WIN_WIDTH, WIN_HEIGHT = pygame.display.get_window_size()  # const values WIDTH and HEIGHT of current window
FPS = 60

settings = json.load(open('data/settings.json', 'r'))  # data from settings.json here
if "total_score" not in settings:  # rules if settings not exists
    settings["total_score"] = 0
if "music" not in settings:
    settings["music"] = 1

font_for_text = pygame.font.SysFont('Comic Sans MS', 30)
pygame.mixer.music.load("data/audis/alexander-nakarada-near-end-action.mp3")  # background music
if settings["music"]:  # if music ON at start
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1)
else:  # if music OFF on start
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()


def camera_configure(camera, target_rect):  # definition to calculate move of camera
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


def clicked_start():  # useless thing just for bug hunting
    print('Начинаем игру')


def close_game():
    pygame.display.quit()
    pygame.quit()


button_volume = ButtonIcon((WIN_WIDTH // 2, 0), "data/pics/volume_on.png",
                           "data/pics/volume_off.png", 1)  # menu volume button
button_volume.rect[1] = WIN_HEIGHT - button_volume.rect[3]  # replace to bottom of screen


def sound_check():
    if button_volume.status:
        pygame.mixer.music.unpause()
        settings["music"] = 1
    else:
        pygame.mixer.music.pause()
        settings["music"] = 0


button_volume.action = sound_check
if not settings["music"]:
    button_volume.cross_image()


def menu():  # menu screen
    background = pygame.image.load("data/pics/menu1.png")
    button_start = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 4), ' НАЧАТЬ ', 150, clicked_start,
                              (0, 255, 0), (0, 0, 255))  # add button
    button_start.centerize()  # centralize text on button
    button_controls = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 2), ' УПРАВЛЕНИЕ ', 80, controls, (0, 255, 0),
                                 (0, 0, 255))
    button_controls.centerize()
    button_exit = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 4 * 3), ' ВЫХОД ', 80, close_game,
                             (0, 255, 0), (0, 0, 255))  # add button
    button_exit.centerize()
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                if button_start.update(event) or button_exit.update(event):
                    running = False
                if button_controls.update(event):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_volume.update(event)
        screen.blit(background, (0, 0))
        button_start.draw(screen)
        button_controls.draw(screen)
        button_exit.draw(screen)
        button_volume.draw(screen)
        pygame.display.flip()
    game()
    return


def controls():  # controls screen
    background = pygame.image.load("data/pics/menu1.png")
    button_prev = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 1.5), ' НАЗАД ', 100, clicked_start,
                             (255, 255, 0), (0, 0, 255))  # add button
    button_prev.centerize()  # centralize text on button
    texts = ['В этой игре нужно управлять самолетом и уничтожать вражескую технику.',
             'Столкновение с землей и чужой техникой может привести к смерти.', '',
             'Управление:', 'ДВИЖЕНИЕ - Стрелки вверх/вниз или W/S,',
             'СТРЕЛЬБА - Пробел,', 'R - перезапуск, 1 - самоуничтожение']
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION) and button_prev.update(event):
                running = False
        screen.blit(background, (0, 0))
        for text in texts:
            txt = font_for_text.render(text, False, (255, 255, 255))
            screen.blit(txt, ((WIN_WIDTH - txt.get_width()) // 2, txt.get_height() * texts.index(text) + 5))
        button_prev.draw(screen)
        pygame.display.flip()
    menu()
    return


def game():  # game cycle
    prev_balance = 0  # previous score for editing speed plane

    sky = Background("sky", "data/pics/sky.png")  # sky box
    ground = Ground(sky.image.get_height(), "data/pics/ground.png")  # ground box
    plane = Plane((0, 1150), sky.rect.height)  # main character
    interface = Interface(WIN_WIDTH, WIN_HEIGHT, settings["total_score"])  # interface thing

    fly_sound = pygame.mixer.Sound('data/audis/flying_plane (mp3cut.net).wav')  # plane sound
    bul_sound = pygame.mixer.Sound('data/audis/attack (mp3cut.net).wav')  # fire sound

    total_width = ground.image.get_width()  # get size of window
    total_height = ground.image.get_height() + sky.image.get_height()
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             event.key == pygame.K_ESCAPE):  # exit event
                running = False
                if interface.current_score > settings["total_score"]:
                    settings["total_score"] = interface.current_score
                break
            elif event.type == pygame.KEYDOWN:  # button pressed
                if event.key == pygame.K_r:  # restart button (R)
                    if interface.current_score > settings["total_score"]:
                        settings["total_score"] = interface.current_score
                    game()
                    return
                if event.key == pygame.K_1:  # suicide button (1)
                    plane.death()
                if event.key == pygame.K_SPACE and plane.alive and interface.can_fire():  # fire button (SPACE)
                    interface.cooldown = 0
                    bul_sound.play()
                    new_bullet = Bullet((plane.rect.x, plane.rect.y), -plane.angle,
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
                    interface.plus_score()
                    plane.death()
                    e.death = True
                elif e.name == 'ground':
                    plane.death()
            for b in bullets:
                if b.is_collided_with(e) and e.name == 'tank' and not e.death:  # kill tank by bullet
                    interface.plus_score()
                    b.kill()
                    e.death = True
                    entities.add(Tank((randint(0, total_width - 200), randint(-200, 300)), ground))
                    break
            screen.blit(e.image, camera.apply(e))
        if not plane.alive:
            interface.death()
        interface.draw(screen)
        pygame.display.flip()
        timer.tick(FPS)
        if interface.current_score % 5 == 0 and interface.current_score != 0 and prev_balance != interface.current_score:
            plane.speed += .5
        prev_balance = interface.current_score
    if not plane.alive:
        fly_sound.stop()
    json.dump(settings, open('data/settings.json', 'w'))
    pygame.mixer.stop()
    menu()
    return


if __name__ == '__main__':
    menu()  # preview screen, starts firstly for open menu screen
