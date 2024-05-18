import pygame
import json
from modules.plane import Plane
from modules.camera import Camera
from modules.enemies import Tank, EnemyPlane
from modules.bullet import Bullet
from modules.buttons import ButtonText, ButtonIcon, Label
from modules.background import Background, Ground
from modules.user_interface import Interface
from modules.input import InputText
from modules.busters import TimeShift, BulletInfinity
from random import randint, choice

pygame.init()  # always uses
pygame.font.init()  # ||-||-||
# ---------------------

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # here's blits all elements of gameplay
pygame.display.set_caption("САМОЛЕТИК")  # just title for app
WIN_WIDTH, WIN_HEIGHT = pygame.display.get_window_size()  # const values WIDTH and HEIGHT of current window
FPS = 60

settings = json.load(open('data/settings.json', 'r'))  # data from settings.json here
if "music" not in settings:  # rules for settings.json
    settings["music"] = 1
if "records" not in settings:
    settings["records"] = dict()
settings["current_profile"] = False
settings["level"] = 0
settings["total_score"] = 0

font_for_text = pygame.font.SysFont('Comic Sans MS', 30)
pygame.mixer.music.load("data/audis/alexander-nakarada-near-end-action.mp3")  # background music
if settings["music"]:  # if music ON at start
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1)
else:  # if music OFF on start
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()

authors_flag = False


def camera_configure(camera, target_rect):  # definition to calculate move of camera
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2 - 250, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


def clicked_start():  # useless thing just for bug hunting
    pass


def close_game():
    settings["total_score"] = 0
    json.dump(settings, open('data/settings.json', 'w'))
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


def enter_name(inp=''):  # profile input function
    if not inp:  # empty input
        pass
    else:  # input(profile name) isn't empty
        if inp not in settings['records']:
            if not settings['current_profile']:
                settings['records'][inp] = settings['total_score']
            else:
                settings['total_score'] = 0
                settings['records'][inp] = settings['total_score']
        elif inp in settings['records']:
            if settings['current_profile'] == inp:
                settings['records'][inp] = max(settings['records'][inp], settings['total_score'])
            else:
                settings['total_score'] = settings['records'][inp]
        settings['current_profile'] = inp


button_volume.action = sound_check
if not settings["music"]:
    button_volume.cross_image()


def preview():
    background = pygame.image.load("data/pics/menu1.png")
    panel = pygame.image.load("data/pics/author1.png")
    panel.convert_alpha()
    button_prev = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 1.1), ' НАЗАД ', 100, clicked_start, (255, 255, 255),
                             (0, 0, 255))  # add button
    button_prev.centerize()  # centralize text on button
    coords = [1920, 100]
    clock = pygame.time.Clock()
    fanfars = pygame.mixer.Sound('data/audis/fanfar.wav')
    fanfars.play()
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                fanfars.stop()
                return
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                fanfars.stop()
                running = False
            if button_prev.update(event):
                fanfars.stop()
                running = False
        coords[0] -= 10
        screen.blit(background, (0, 0))
        screen.blit(panel, coords)
        button_prev.draw(screen)
        clock.tick(20)
        pygame.display.flip()
        if coords[0] == 0:
            coords[0] += 10


def authors(scrn=None, coords=None):
    pass


def change_level():
    settings["level"] += 1
    settings["level"] %= 3
    return True


def menu():  # menu screen
    background = pygame.image.load("data/pics/menu1.png")
    button_start = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 4), ' НАЧАТЬ ', 150, clicked_start,
                              (0, 0, 0), (0, 0, 255))  # add button НАЧАТЬ
    button_start.centerize()  # centralize text on button
    button_controls = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 2), ' УПРАВЛЕНИЕ ',
                                 80, controls, (0, 0, 0), (0, 0, 255))  # add button УПРАВЛЕНИЕ
    button_controls.centerize()
    button_exit = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 4 * 3), ' ВЫХОД ', 80, close_game,
                             (0, 0, 0), (0, 0, 255))  # add button ВЫХОД
    button_exit.centerize()
    button_records = ButtonText((150, 200), ' РЕКОРДЫ ', 50, records,
                                (0, 0, 0), (0, 0, 255))  # add button РЕКОРДЫ
    button_records.centerize()  # centralize text on button

    input_name = InputText((10, button_records.rect[0] + 500))

    button_entname = ButtonText((230, input_name.rect.top + 95),
                                ' ВПИСАТЬ СЕБЯ В ИСТОРИЮ ', 30, enter_name,
                                (0, 0, 0), (0, 0, 255))  # add button ВПИСАТЬ СЕБЯ В ИСТОРИЮ
    button_entname.centerize()  # centralize text on button

    button_author = ButtonText((WIN_WIDTH - 300, 100),
                               ' АВТОРЫ ', 30, authors,
                               (0, 0, 0), (0, 0, 255))
    button_author.rect[0] = WIN_WIDTH - button_author.rect[2]
    button_author.rect[1] = WIN_HEIGHT - button_author.rect[3]

    profile_rec = Label((0, 0), f"Ваш рекорд: {settings['total_score']}")
    profile_rec.rightize(WIN_WIDTH, WIN_HEIGHT)
    if settings["current_profile"]:
        profile_rec.edit_text(f"{settings['current_profile']}, Ваш рекорд: {settings['total_score']}")
    button_level = ButtonText((0, 0), f" Текущий уровень: {settings['level']} ",
                              28, change_level, background_color=(150, 0, 0))
    button_level.rect[0] = WIN_WIDTH - button_level.rect[2]
    button_level.rect[1] = profile_rec.coords[1] + button_level.rect[3] + 10
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            input_name.update(event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                if button_author.update(event):
                    print("press")
                    preview()
                if button_level.update(event):
                    button_level = ButtonText((0, 0), f" Текущий уровень: {settings['level']} ",
                                              28, change_level, background_color=(150, 0, 0))
                    button_level.rect[0] = WIN_WIDTH - button_level.rect[2]
                    button_level.rect[1] = profile_rec.coords[1] + button_level.rect[3] + 10
                if button_entname.update(event):
                    enter_name(input_name.text)
                    profile_rec.edit_text(f"{settings['current_profile']}, Ваш рекорд: {settings['total_score']}")
                if button_start.update(
                        event):  # starts game (in next IF updates buttons and starts theirs event functions)
                    running = False
                elif (button_exit.update(event) or button_controls.update(event) or
                      button_records.update(event)):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_volume.update(event)
        screen.blit(background, (0, 0))

        button_start.draw(screen)
        button_controls.draw(screen)
        button_records.draw(screen)
        button_entname.draw(screen)
        button_exit.draw(screen)
        button_volume.draw(screen)
        button_author.draw(screen)
        button_level.draw(screen)
        input_name.draw(screen)
        profile_rec.draw(screen)

        pygame.display.flip()
    game()
    return


def controls():  # controls screen
    background = pygame.image.load("data/pics/menu1.png")
    button_prev = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 1.5), ' НАЗАД ', 100, clicked_start,
                             (0, 0, 255))  # add button
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


def records():
    background = pygame.image.load("data/pics/menu2.png")
    button_prev = ButtonText((WIN_WIDTH // 2, WIN_HEIGHT // 1.1), ' НАЗАД ', 100, clicked_start,
                             (0, 0, 255))  # add button
    button_prev.centerize()  # centralize text on button
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                if button_prev.update(event):
                    running = False
        screen.blit(background, (0, 0))
        button_prev.draw(screen)
        for i in range(len(settings["records"])):
            key = list(settings["records"].keys())[i]
            new_l = Label((0, (50 * i + 10)), f'{key} - {settings["records"][key]}', (255, 255, 0))
            new_l.centerize(WIN_WIDTH, WIN_HEIGHT)
            new_l.draw(screen)
        pygame.display.flip()
    menu()


def game():  # game cycle
    prev_balance = 0  # previous score for editing speed plane

    sky = Background("sky", f"data/pics/sky{settings['level']}.png")  # sky box
    ground = Ground(sky.image.get_height(), f"data/pics/ground{settings['level']}.png")  # ground box

    plane = Plane((0, 1150), sky.rect.height)  # main character
    interface = Interface(WIN_WIDTH, WIN_HEIGHT, settings["total_score"])  # interface thing

    timeshb = TimeShift((1000, 500))
    bullinf = BulletInfinity((1000, 500))

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
    entities.add(timeshb)
    entities.add(bullinf)

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
                    enter_name(settings["current_profile"])
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
        timeshb.collided(plane, interface)
        bullinf.collided(plane, interface)
        for e in entities:
            if e.name == 'tank' or e.name == 'bullet' or e.name == 'enemy_plane':
                e.update()
            if plane.is_collided_with(e) and (e.name == 'tank' or e.name == 'ground' or e.name == 'enemy_plane'):
                if e.name == 'tank' and not e.death:
                    interface.plus_score()
                    plane.death()
                    e.death = True
                elif e.name == 'ground':
                    plane.death()
                elif e.name == 'enemy_plane':
                    interface.health -= 10
                    e.death()
            for b in bullets:
                if b.is_collided_with(e) and e.name == 'tank' and not e.death:  # kill tank by bullet
                    interface.plus_score()
                    b.kill()
                    e.death = True
                    coordx = choice((randint(0, abs(plane.rect.x - 500)), randint(abs(plane.rect.x + 500), 4850)))
                    entities.add(Tank((coordx, randint(-200, 100)), ground))
                    break
                if b.is_collided_with(e) and e.name == 'enemy_plane':
                    interface.plus_score()
                    e.death()
            screen.blit(e.image, camera.apply(e))
        if not plane.alive:
            fly_sound.stop()
            interface.death()
        interface.draw(screen)
        pygame.display.flip()
        timer.tick(FPS)
        if (interface.current_score % 5 == 0 and
                interface.current_score != 0 and
                prev_balance != interface.current_score):
            plane.speed += 1
        if (interface.current_score % 2 == 0 and
                interface.current_score != 0 and
                prev_balance != interface.current_score):
            entities.add(EnemyPlane((plane.rect.x, plane.rect.y), ground))
        if not interface.alive:
            plane.death()
        prev_balance = interface.current_score

    json.dump(settings, open('data/settings.json', 'w'))
    pygame.mixer.stop()
    menu()
    return


if __name__ == '__main__':
    menu()
