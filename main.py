import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 600))

clock = pygame.time.Clock()
keep_playing = True

while keep_playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_playing = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()