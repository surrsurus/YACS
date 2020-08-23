import pygame
from src import menu
from src import client
from src import server
import board
from src import util, chess

### Game Globals ###

DEBUG = True

### Pygame Init ###

# Initialize pygame
pygame.init()
 
# Set screen dimensions
WINDOW_SIZE = [1440, 900]
screen = pygame.display.set_mode(WINDOW_SIZE)
menu.MenuManager.setWindowSize(WINDOW_SIZE)

# Set title
pygame.display.set_caption("YACS - Yet Another Chess Simulator")
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Client objs go here
server = None
client = None
board = board.Board()
menu.updateBoardObjs(board)

# Loop until the user clicks the close button.
done = False

### Game Loop ###
game = chess.Chess()

while not done:

    for event in pygame.event.get():

        # Quit scenario
        if event.type == pygame.QUIT: 
            done = True

        # Clicked a tile scenario
        elif event.type == pygame.MOUSEBUTTONUP:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            menu.MenuManager.handleClick(pos)


    # Set the screen background
    screen.fill(util.WHITE)
    menu.MenuManager.drawCurrent(screen)

    if menu.MenuManager.CURRENT == menu.MenuManager.GAME_SERVER:
        # Server loop. 
        # If the above is true, the player who clicked "Host Game" is now on the game screen
        # Accept connection if needed, otherwise wait for host to take turn and then send it to client
        # move = board.getValidMove()
        # server.send(move)
        # thiermove = server.recieve()
        # board.move(thiermove)
        pass
    elif menu.MenuManager.CURRENT == menu.MenuManager.GAME_CLIENT:
        # Client loop. 
        # If the above is true, the player who clicked "Join Game" is now on the game screen
        # Wait for player to take turn and then send it to server
        # theirmove = client.recieve()
        # board.move(thiermove)
        # move = board.getValidMove()
        # server.send(move)
        pass
 
    # FPS Limiter
    clock.tick(60)
 
    # Flush changes to screen
    pygame.display.flip()
 
# Program will hang on exit without this
pygame.quit()