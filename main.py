import pygame
from pygame.locals import *

pygame.init()

screenWidth = 864
screenHeight = 936

# game window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Flappy Bird")

# loads images
background = pygame.image.load("bg.png")

run = True
while run:

    # displays background img
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()