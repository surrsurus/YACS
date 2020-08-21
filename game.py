import pygame
from menu import MenuManager
from enum import Enum

### Game Globals ###

DEBUG = True

# This sets the WIDTH and HEIGHT of each board tile
WIDTH = 40
HEIGHT = WIDTH
 
# This sets the margin between each tile
MARGIN = 1

# Color tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

### Board Init ###

class Tile(object):
    '''Tile object representing individual board tile'''
    def __init__(self, color, coord, piece=[]):
        self.color = color
        self.coord = coord
        self.piece = piece

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

    def draw(self, screen):
        '''Render board to screen, right now, board is the screen so no xy is passed'''
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(screen,
                                self.board[row][col].color,
                                [(MARGIN + WIDTH) * col + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])

    def tile_at(self, coord):
        '''Return tile at coord'''
        for row in self.board:
            for tile in row:
                if tile.coord == coord:
                    return tile

    def coord_2_pos(self, coord):
        '''Convert a chess coordinate to pygame position'''
        for row in range(8):
            for col in range(8):
                if coord == self.board[row][col].coord:
                    return ((MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN)
    
    def __getitem__(self, i):
        return self.board[i]

# New board
board = Board()

### Pieces Init ###

b_pawn_img = pygame.image.load('./assets/chesspieces/black/png/black_pawn.png')
b_rook_img = pygame.image.load('./assets/chesspieces/black/png/black_rook.png')
b_knight_img = pygame.image.load('./assets/chesspieces/black/png/black_knight.png')
b_bishop_img = pygame.image.load('./assets/chesspieces/black/png/black_bishop.png')
b_queen_img = pygame.image.load('./assets/chesspieces/black/png/black_queen.png')
b_king_img = pygame.image.load('./assets/chesspieces/black/png/black_king.png')

w_pawn_img = pygame.image.load('./assets/chesspieces/white/png/white_pawn.png')
w_rook_img = pygame.image.load('./assets/chesspieces/white/png/white_rook.png')
w_knight_img = pygame.image.load('./assets/chesspieces/white/png/white_knight.png')
w_bishop_img = pygame.image.load('./assets/chesspieces/white/png/white_bishop.png')
w_queen_img = pygame.image.load('./assets/chesspieces/white/png/white_queen.png')
w_king_img = pygame.image.load('./assets/chesspieces/white/png/white_king.png')

class PieceColor(Enum):
    BLACK = 0
    WHITE = 1

class PieceType(Enum):
    '''An enum to represent the types of chess pieces'''
    PAWN = 0
    ROOK = 1
    KNIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5

class Piece(object):
    def __init__(self, ptype, color, img, coord):
        self.type = ptype
        self.color = color
        self.img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        self.coord = coord

    def draw(self, screen, pos):
        '''Render a piece to a screen'''
        screen.blit(self.img, pos)

# Create pieces
BLACK_PIECES = [
    Piece(PieceType.PAWN, PieceColor.BLACK, b_pawn_img, "A7"),
    Piece(PieceType.PAWN, PieceColor.BLACK, b_pawn_img, "B7"),
    Piece(PieceType.PAWN, PieceColor.BLACK, b_pawn_img, "C7"),
    Piece(PieceType.PAWN, PieceColor.BLACK, b_pawn_img, "D7"),
    Piece(PieceType.PAWN, PieceColor.BLACK, b_pawn_img, "E7"),
    Piece(PieceType.PAWN, PieceColor.BLACK, b_pawn_img, "F7"),
    Piece(PieceType.PAWN, PieceColor.BLACK, b_pawn_img, "G7"),
    Piece(PieceType.PAWN, PieceColor.BLACK, b_pawn_img, "H7"),
    Piece(PieceType.ROOK, PieceColor.BLACK, b_rook_img, "A8"),
    Piece(PieceType.ROOK, PieceColor.BLACK, b_rook_img, "H8"),
    Piece(PieceType.KNIGHT, PieceColor.BLACK, b_knight_img, "B8"),
    Piece(PieceType.KNIGHT, PieceColor.BLACK, b_knight_img, "G8"),
    Piece(PieceType.BISHOP, PieceColor.BLACK, b_bishop_img, "C8"),
    Piece(PieceType.BISHOP, PieceColor.BLACK, b_bishop_img, "F8"),
    Piece(PieceType.QUEEN, PieceColor.BLACK, b_queen_img, "D8"),
    Piece(PieceType.KING, PieceColor.BLACK, b_king_img, "E8")
]
WHITE_PIECES = [
    Piece(PieceType.PAWN, PieceColor.WHITE, w_pawn_img, "A2"),
    Piece(PieceType.PAWN, PieceColor.WHITE, w_pawn_img, "B2"),
    Piece(PieceType.PAWN, PieceColor.WHITE, w_pawn_img, "C2"),
    Piece(PieceType.PAWN, PieceColor.WHITE, w_pawn_img, "D2"),
    Piece(PieceType.PAWN, PieceColor.WHITE, w_pawn_img, "E2"),
    Piece(PieceType.PAWN, PieceColor.WHITE, w_pawn_img, "F2"),
    Piece(PieceType.PAWN, PieceColor.WHITE, w_pawn_img, "G2"),
    Piece(PieceType.PAWN, PieceColor.WHITE, w_pawn_img, "H2"),
    Piece(PieceType.ROOK, PieceColor.WHITE, w_rook_img, "A1"),
    Piece(PieceType.ROOK, PieceColor.WHITE, w_rook_img, "H1"),
    Piece(PieceType.KNIGHT, PieceColor.WHITE, w_knight_img, "B1"),
    Piece(PieceType.KNIGHT, PieceColor.WHITE, w_knight_img, "G1"),
    Piece(PieceType.BISHOP, PieceColor.WHITE, w_bishop_img, "C1"),
    Piece(PieceType.BISHOP, PieceColor.WHITE, w_bishop_img, "F1"),
    Piece(PieceType.QUEEN, PieceColor.WHITE, w_queen_img, "D1"),
    Piece(PieceType.KING, PieceColor.WHITE, w_king_img, "E1")
]

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
 
### Game Loop ###

# Loop until the user clicks the close button.
done = False

while not done:

    for event in pygame.event.get():

        # Set the screen background
        screen.fill(WHITE)
        MenuManager.drawCurrent(screen)

        # Quit scenario
        if event.type == pygame.QUIT: 
            done = True

        # Clicked a tile scenario
        elif event.type == pygame.MOUSEBUTTONUP:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            MenuManager.handleClick(pos)

    # FPS Limiter
    clock.tick(60)
 
    # Flush changes to screen
    pygame.display.flip()
 
# Program will hang on exit without this
pygame.quit()