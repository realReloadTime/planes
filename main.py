import pygame
from modules.plane import Plane

pygame.init()
window_size = 1000, 500
fullscreen = True
background_color = (255, 255, 255)
fps = 60

if not fullscreen:
    screen = pygame.display.set_mode(window_size)
else:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_size = pygame.display.get_window_size()
pygame.display.set_caption("САМОЛЕТЫ")
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
sprites.add(Plane((0, 50), (1, 0)))
running = True
while running:
    screen.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    sprites.draw(screen)
    sprites.update(event)
    clock.tick(fps)
    pygame.display.update()
pygame.quit()