import pygame

# Initialize Pygame
pygame.init()

# Initialize the mixer (optional but good practice)
pygame.mixer.init()

# Load the sound
click_sound = pygame.mixer.Sound("Flappy Death.wav")

# Set up a basic display (required for event loop)
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Play Sound Example")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Play sound when you click the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()

pygame.quit()
