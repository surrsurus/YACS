import pygame
import menu
from menu import MenuManager
import util, board
from server import Server
from client import Client

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
board = board.Board()
menu.updateBoards(board)
serverNotInitialized = True
clientNotInitialized = True
firstTurn = True

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

    if MenuManager.CURRENT == MenuManager.GAME_SERVER:
        # Server loop. 
        # If the above is true, the player who clicked "Host Game" is now on the game screen
        # Accept connection if needed, otherwise wait for host to take turn and then send it to client
        if serverNotInitialized:
            server = Server("192.168.192.209", 25565)
            server.startServer()
            serverNotInitialized = False
        if board.getValidMoveHasHappened():
            server.send(board)
            # exit here on checkmate
            board = server.recieve()

    elif MenuManager.CURRENT == MenuManager.GAME_CLIENT:
        # Client loop. 
        # If the above is true, the player who clicked "Join Game" is now on the game screen
        # Wait for player to take turn and then send it to server
        if clientNotInitialized:
            client = Client("192.168.192.209", 25565)
            client.connect()
            clientNotInitialized = False
        if firstTurn:
            theirmove = client.recieve()
            board.move(thiermove)
            firstTurn = False
        else:
            if board.getValidMoveHasHappened():
                move = board.getValidMove()
                client.send(move)
                # exit here on checkmate
                board = client.recieve()
 
    # FPS Limiter
    clock.tick(60)
 
    # Flush changes to screen
    pygame.display.flip()
 
# Program will hang on exit without this
client.disconnect()
server.stopServer()
pygame.quit()