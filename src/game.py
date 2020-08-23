import pygame
from menu import MenuManager

import util

### Game Globals ###

DEBUG = True

### Pygame Init ###

# Initialize pygame
pygame.init()
 
# Set screen dimensions
WINDOW_SIZE = [1440, 900]
screen = pygame.display.set_mode(WINDOW_SIZE)
MenuManager.setWindowSize(WINDOW_SIZE)

# Set title
pygame.display.set_caption("YACS - Yet Another Chess Simulator")
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
### Game Loop ###

# Loop until the user clicks the close button.
done = False

while not done:

    for event in pygame.event.get():

        # Quit scenario
        if event.type == pygame.QUIT: 
            done = True

        # Clicked a tile scenario
        elif event.type == pygame.MOUSEBUTTONUP:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            MenuManager.handleClick(pos)

    # Set the screen background
    screen.fill(util.WHITE)
    MenuManager.drawCurrent(screen)
 
    # FPS Limiter
    clock.tick(60)
 
    # Flush changes to screen
    pygame.display.flip()
 
# Program will hang on exit without this
pygame.quit()