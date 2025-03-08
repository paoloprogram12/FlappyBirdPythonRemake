import pygame
from pygame.locals import *

pygame.init()

# sets time
clock = pygame.time.Clock() # creates a timer
fps = 60 # framerate for the game

screenWidth = 864
screenHeight = 936

# game window
screen = pygame.display.set_mode((screenWidth, screenHeight)) # the dimensions for the window of the game
pygame.display.set_caption("Flappy Bird") # title for the game

# game variables
groundScroll = 0 # used for the ground image to change its coordinates
scrollSpeed = 4 # moves by 4 px (used for how fast should the ground be moving)

# loads images
background = pygame.image.load("bg.png") # variable for the background img
ground = pygame.image.load("ground.png") # variable for the ground img

# The bird itself
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):

        # handle the animation
        self.counter += 1
        flapCooldown = 5

        if self.counter > flapCooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screenHeight / 2))

bird_group.add(flappy)


run = True
while run: # runs the flappy bird game

    # sets the game loop locked to certain fps (60)
    clock.tick(fps)

    # draw background
    screen.blit(background, (0,0)) # sets the background to background

    bird_group.draw(screen)
    bird_group.update()
    
    # draw and scrolls the ground
    screen.blit(ground, (groundScroll, 768)) # adds ground img to the game
    groundScroll -= scrollSpeed # allows the ground img to look like it is moving
    # resets the x coordinate to once it becomes > than 35
    if abs(groundScroll) > 35:
        groundScroll = 0


    # quits the game (when the x button on the right is clicked)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # updates the display (updates the background img)
    pygame.display.update()

pygame.quit()

