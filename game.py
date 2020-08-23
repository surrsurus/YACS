import pygame
from menu import MenuManager
from client import Client
from server import Server

import util

### Game Globals ###

DEBUG = True

### Pygame Init ###

# Initialize pygame
pygame.init()
 
# Set screen dimensions
WINDOW_SIZE = [1000, 800]
screen = pygame.display.set_mode(WINDOW_SIZE)
MenuManager.setWindowSize(WINDOW_SIZE)

# Set title
pygame.display.set_caption("YACS - Yet Another Chess Simulator")
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Client objs go here
server = None
client = None

# Loop until the user clicks the close button.
done = False

### Game Loop ###
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

    if MenuManager.CURRENT == MenuManager.GAME_SERVER:
        # Server loop. 
        # If the above is true, the player who clicked "Host Game" is now on the game screen
        # Accept connection if needed, otherwise wait for host to take turn and then send it to client
        # move = board.getValidMove()
        # server.send(move)
        # thiermove = server.recieve()
        # board.move(thiermove)

    elif MenuManager.CURRENT == MenuManager.GAME_CLIENT:
        # Client loop. 
        # If the above is true, the player who clicked "Join Game" is now on the game screen
        # Wait for player to take turn and then send it to server
        # theirmove = client.recieve()
        # board.move(thiermove)
        # move = board.getValidMove()
        # server.send(move)
 
    # FPS Limiter
    clock.tick(60)
 
    # Flush changes to screen
    pygame.display.flip()
 
# Program will hang on exit without this
pygame.quit()