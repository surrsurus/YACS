import pygame
import menu

### Board Init ###

# Color tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each board tile
WIDTH = 40
HEIGHT = 40
 
# This sets the margin between each tile
MARGIN = 3

# Create the chess board
board = []
flop = True
for row in range(8):
    board.append([])
    flop = not flop
    for column in range(8):
        if flop:
            board[row].append(0)
        else:
            board[row].append(1)
        flop = not flop

print(board)

### Pygame Init ###

# Initialize pygame
pygame.init()
 
# Set screen dimensions
WINDOW_SIZE = [WIDTH * 8 + (MARGIN * 8), HEIGHT * 8 + (MARGIN * 8)]
screen = pygame.display.set_mode(WINDOW_SIZE)
MenuManager.setWindowSize()

 
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to board coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Change color
            # board[row][column] = 2
            print("Click ", pos, "board coordinates: ", row, column)
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the board
    for row in range(8):
        for column in range(8):

            color = WHITE
            if board[row][column] == 1:
                color = BLACK
            if board[row][column] == 2:
                color = GREEN
            
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
 
    # FPS Limiter
    clock.tick(60)
 
    # Flush changes to screen
    pygame.display.flip()
 
# Program will hang on exit without this
pygame.quit()