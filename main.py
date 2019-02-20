import pygame
import pygame.font
pygame.init()
pygame.font.init()

import classes

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

size = (960, 720) #CHANGE THIS
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shmup")

done = False

clock = pygame.time.Clock()

player = classes.Player(480, 670, 50, 1)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)

    screen.blit(player.draw(), (player.x, player.y))
    player.update()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
