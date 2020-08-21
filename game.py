import pygame

### Game Globals ###

DEBUG = True

### Board Init ###

# Color tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each board tile
WIDTH = 40
HEIGHT = WIDTH
 
# This sets the margin between each tile
MARGIN = 1

class Tile(object):
    '''Tile object representing individual board tile'''
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord

class Board(object):
    '''Board object representing chess game board'''
    def __init__(self):
        self.board = []

        # Create the chess board
        flop = False
        rank = 0
        for i in range(8):
            self.board.append([])

            flop = not flop
            row = "A"

            for col in range(8):
                if flop:
                    self.board[i].append(Tile(WHITE, row + str(8 - rank)))
                else:
                    self.board[i].append(Tile(BLACK, row + str(8 - rank)))

                flop = not flop
                # Increment row
                row = chr(ord(row) + 1)

            rank += 1

    def at(self, coord):
        for row in self.board:
            for tile in row:
                if tile.coord == coord:
                    return tile
    
    def __getitem__(self, i):
        return self.board[i]

# New board
board = Board()

### Pygame Init ###

# Initialize pygame
pygame.init()
 
# Set screen dimensions
WINDOW_SIZE = [WIDTH * 8 + (MARGIN * 8), HEIGHT * 8 + (MARGIN * 8)]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
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

            if DEBUG:
                print("Click ", pos, "board coordinates: ", row, column, "coord: ", board[row][column].coord)
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the board
    for row in range(8):
        for column in range(8):
            
            pygame.draw.rect(screen,
                             board[row][column].color,
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