import pygame
from pygame.locals import *

pygame.init()

# sets time
clock = pygame.time.Clock()
fps = 60

screenWidth = 864
screenHeight = 936

# game window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Flappy Bird")

# game variables
groundScroll = 0
scrollSpeed = 4 # moves by 4 px

# loads images
background = pygame.image.load("bg.png")
ground = pygame.image.load("ground.png")

run = True
while run:

    clock.tick(fps)

    # draw background
    screen.blit(background, (0,0))
    
    # draw and scrolls the ground
    screen.blit(ground, (groundScroll, 768))
    groundScroll -= scrollSpeed
    if abs(groundScroll) > 35:
        groundScroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # updates the display (updates the background img)
    pygame.display.update()

pygame.quit()

