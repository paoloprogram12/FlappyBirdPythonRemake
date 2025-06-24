import pygame
from pygame.locals import *
import random

# a Sprite is an object that is used to represent a visual element on the screen,
# EX: a player, enemy, a bullet, etc
# It includes an image and a behavior

pygame.init()
pygame.mixer.init()

# sounds
flap_sound = pygame.mixer.Sound("Flappy Flapper.wav")
death_sound = pygame.mixer.Sound("Flappy Death.wav")
score_sound = pygame.mixer.Sound("Flappy Score.wav")

# sets time
clock = pygame.time.Clock() # creates a timer
fps = 60 # framerate for the game

screenWidth = 864
screenHeight = 936

# game window
screen = pygame.display.set_mode((screenWidth, screenHeight)) # the dimensions for the window of the game
pygame.display.set_caption("Flappy Bird") # title for the game

# define font
font = pygame.font.SysFont('Bauhaus 93', 60)

# define font color
white = (255, 255, 255)

# game variables
groundScroll = 0 # used for the ground image to change its coordinates
scrollSpeed = 4 # moves by 4 px (used for how fast should the ground be moving)
flying = False # bool to check if the game has started or not
gameOver = False # bool to see if flappy has died :(
pipeGap = 150 # gap between top and btm pipes
pipeFrequency = 1500 # milliseconds
lastPipe = pygame.time.get_ticks() - pipeFrequency # measures the time from when the game started
score = 0 # score for bird
passPipe = False # boolean to see if the bird has passed a pipe or not

# loads images
background = pygame.image.load("bg.png") # variable for the background img
ground = pygame.image.load("ground.png") # variable for the ground img
reset_button = pygame.image.load("restart.png")

# the text for the score
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screenHeight / 2)
    score = 0
    return score


# The bird itself
class Bird(pygame.sprite.Sprite): # class for the actual bird
    def __init__(self, x, y): # function for where the flappy bird is going to be placed in the game
        pygame.sprite.Sprite.__init__(self) # inherits functionality? (self variable is now set to sprite(flappy)
        self.images = [] # array for images for bird (flapping animation)
        self.index = 0 # references the particular image in the list
        self.counter = 0

        # for loop for flapping animation, iterates through the array to constantly change the image of the bird
        for num in range(1, 4):
            img = pygame.image.load(f"bird{num}.png")
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # creates boundaries of the rectangle (the image)
        self.rect.center = [x, y] # sets the position of the image
        self.vel = 0 # creates a variable for the sprite (flappy) velocity
        self.clicked = False # check when imouse left button is being released (used to stop usage of holding the mouse button when it's only supposed to be clicked)

    def update(self): # handles all the animation and the movement

        # gravity of the bird
        if flying == True:
            self.vel += 0.5  # increases velocity by 0.5
            if self.vel > 8: # sets a limit for the velocity, so it doesn't keep increasing
                self.vel = 8
            if self.rect.bottom < 768: # stops the bird from falling through the ground
                self.rect.y += int(self.vel) # constantly increases velocity

        if gameOver == False:
            pygame.mouse.get_pressed()[0]

            # jumping of the bird (one click allows the bird to jump)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # used to check if the mouse has been clicked, 0 means for left click, 1 is used to check if it was clicked
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True: # used to check if the mouse has been clicked, 0 means for left click, 0 is used to check if it was not clicked
                self.clicked = False

            # handle the flapping animation
            self.counter += 1 # counter for if it goes greater than the flap cooldown 
            flapCooldown = 5 # cooldown for flapping animation
            # my guesstimation is that every 5 frames, an image will change

            # if the counter reaches more than 5 frames, it switches to 0
            if self.counter > flapCooldown:
                self.counter = 0
                self.index += 1 # updates image to the next image
                if self.index >= len(self.images): # restarts the animation
                    self.index = 0
            self.image = self.images[self.index]

            # bird rotation for gravity
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2) # function to rotate the img, parameters: the image of the bird, position it rotates (* -2 bc we want it cw, originally it is ccw)
        else: # gameOver is now true
             self.image = pygame.transform.rotate(self.images[self.index], -90) # sets the bird to 90 degrees after impact (stops animation moving after flappy has died)

# the pipe obstacles has its own class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")

        # creates a rectangle based on the dimensions of the pipe img
        self.rect = self.image.get_rect()

        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) #x, y
             # gets coordinates of the rectangle
            self.rect.bottomleft = [x, y -  int(pipeGap / 2)]
        if position == -1:
            # gets coordinates of the rectangle
            self.rect.topleft = [x, y + int(pipeGap / 2)]

    # function for pipes to move left
    def update(self):
        self.rect.x -= scrollSpeed # scroolspeed is 4
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # checks if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1: # if lmb is clicked
                action = True

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group() # keeps track of all bird animation (the sprites) in the game
pipe_group = pygame.sprite.Group() # keeps track of all pipes in the game


# a sprite is a 2D image that can be integrated into a larger scene (in this case flappy)

flappy = Bird(100, int(screenHeight / 2)) # initalizes the bird class (the parameters is where the bird will be located in the game)

bird_group.add(flappy) # adds the bird into the the sprite group

# create restart button instance
button = Button(screenWidth // 2 - 50, screenHeight // 2 - 100, reset_button)

death_played = False

run = True
while run: # runs the flappy bird game

    # sets the game loop locked to certain fps (60)
    clock.tick(fps)

    # draw background
    screen.blit(background, (0,0)) # sets the background to background

    # draws background (adds flappy bird onto the game, and pipes)
    bird_group.draw(screen)
    bird_group.update() # i think this allows the flapping animation to work
    pipe_group.draw(screen)
    
    screen.blit(ground, (groundScroll, 768)) # adds ground img to the game

    # used to check the score
    
    if len(pipe_group) > 0:
        # how it works:
        # if the bird is in the middle of the left side of the pipe and the right side of the pipe
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and passPipe == False:
            passPipe = True

        if passPipe == True:
            # if the bird has left the right hand side of the pipe
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score_sound.play()
                score += 1
                passPipe = False

    draw_text(str(score), font, white, int(screenWidth / 2), 20)

    # if a collision has occurred
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        gameOver = True

    # checks if bird has made impact to the ground :(
    if flappy.rect.bottom >= 768:
        gameOver = True
        flying = False
    
    # draw and scrolls the ground
    if gameOver == False and flying == True: # if the game hasn't started and i have already clicked
        # generates new pipes
        # works by using the time to generate multiple pipes
        time_now = pygame.time.get_ticks()
        if time_now - lastPipe > pipeFrequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screenWidth, int(screenHeight / 2) + pipe_height, -1) # adds a bottom pipe onto the screen
            top_pipe = Pipe(screenWidth, int(screenHeight / 2) + pipe_height, 1) # adds top pipe onto the screen
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            lastPipe = time_now

        groundScroll -= scrollSpeed # allows the ground img to look like it is moving
        # resets the x coordinate to once it becomes > than 35
        if abs(groundScroll) > 35:
            groundScroll = 0
        pipe_group.update() # updates the pipes to the screen (its under here so if flappy dies, pipes stop updating)

    # checks for game over and reset
    if gameOver == True:
        if not death_played:
            death_sound.play()
            death_played = True
        if button.draw() == True:
            gameOver = False
            death_played = False
            score = reset_game()


    # quits the game (when the x button on the right is clicked)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameOver == False: # have to click a mouse button first before starting the game
            flying = True
            

    # updates the display (updates the background img)
    pygame.display.update()

pygame.quit()

