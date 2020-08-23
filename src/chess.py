import copy
import enum
import board


class ChessState(enum.Enum):
    inProgress = 1
    blackChecked = 2
    whiteChecked = 3
    blackCheckmated = 4
    whiteCheckmated = 5
    draw = 6


class PieceType(enum.Enum):
    empty = 0
    pawn = 1
    king = 2
    queen = 3
    rook = 4
    bishop = 5
    knight = 6


class Pos:
    colDict = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
        "E": 5,
        "F": 6,
        "G": 7,
        "H": 8,
    }

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def getPosAsPair(self):
        return self.colDict.get(self.col), self.row

    def getPosAsString(self):
        return  self.col + str(self.row)


class Color:
    # Black is false
    def __init__(self, color):
        self.color = color

    def setColor(self, color):
        self.color = color

    def getColor(self) -> bool:
        return self.color


class Piece:
    def __init__(self, row, column, active, pieceType, color):
        self.pos = Pos(row, column)
        self.active = active
        self.pieceType = pieceType
        self.color = Color(color)
        self.en_passant = False
        self.has_not_moved = True

    def setpos(self, pos):
        self.pos = pos

    def getpos(self) -> ():
        return self.pos

    def getPosAsString(self):
        return self.pos.getPosAsString()

    def setActive(self, active):
        self.active = active

    def settype(self, piecetype):
        self.pieceType = piecetype

    def gettype(self):
        return self.pieceType

    def setColor(self, color):
        self.color.setColor(color)

    def getColor(self):
        return self.color.getColor()

    def getActive(self):
        return self.active

    def getEnPassant(self):
        return self.en_passant

    def setEnPassant(self, en_passant):
        self.en_passant = en_passant

    def getHasNotMoved(self):
        return self.has_not_moved

    def setHasNotMoved(self, can_castle):
        self.has_not_moved = can_castle


class ChessBoard:
    def __init__(self):
        self.tiles = []
        self.whitePieces = []
        self.blackPieces = []

    def setStartBoard(self):
        self.tiles = []
        self.whitePieces = []
        self.blackPieces = []
        self.whitePieces.extend([Piece(1, "A", True, PieceType.rook, True),
                                 Piece(1, "B", True, PieceType.knight, True),
                                 Piece(1, "C", True, PieceType.bishop, True),
                                 Piece(1, "D", True, PieceType.queen, True),
                                 Piece(1, "E", True, PieceType.king, True),
                                 Piece(1, "F", True, PieceType.bishop, True),
                                 Piece(1, "G", True, PieceType.knight, True),
                                 Piece(1, "H", True, PieceType.rook, True)])
        self.blackPieces.extend([Piece(8, "A", True, PieceType.rook, False),
                                 Piece(8, "B", True, PieceType.knight, False),
                                 Piece(8, "C", True, PieceType.bishop, False),
                                 Piece(8, "D", True, PieceType.queen, False),
                                 Piece(8, "E", True, PieceType.king, False),
                                 Piece(8, "F", True, PieceType.bishop, False),
                                 Piece(8, "G", True, PieceType.knight, False),
                                 Piece(8, "H", True, PieceType.rook, False)])

        for letter in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            self.blackPieces.append(Piece(7, letter, True, PieceType.pawn, False))
            self.whitePieces.append(Piece(2, letter, True, PieceType.pawn, True))

        self.tiles.append(self.whitePieces[0:8])
        self.tiles.append(self.whitePieces[8:16])

        for i in [3, 4, 5, 6]:
            emptyrow = []
            for letter in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                emptyrow.append(Piece(0, "", False, PieceType.empty, False))
            self.tiles.append(emptyrow)

        self.tiles.append(self.blackPieces[8:16])
        self.tiles.append(self.blackPieces[0:8])

    def setBoard(self, tiles):
        self.whitePieces = []
        self.blackPieces = []
        for row in tiles:
            for piece in row:
                if piece.gettype() != PieceType.empty and piece.getColor():
                    self.whitePieces.append(piece)
                elif piece.gettype() != PieceType.empty:
                    self.blackPieces.append(piece)

        self.tiles = tiles

    def setEmptyBoard(self):
        tiles = []

        for i in range(8):
            emptyrow = []
            for j in range(8):
                emptyrow.append(Piece(0, "", False, PieceType.empty, False))
            tiles.append(emptyrow)
        self.tiles = tiles
        self.whitePieces = []
        self.blackPieces = []

    def getstate(self, color):
        logic = ChessLogic()
        return logic.checkState(self, color)

    def getWhitePieces(self):
        return self.whitePieces

    def getBlackPieces(self):
        return self.blackPieces

    def addpiece(self, piece):
        if piece.getColor():
            self.whitePieces.append(piece)
        else:
            self.blackPieces.append(piece)
        piece_pos = piece.getpos().getPosAsPair()
        self.setpos(piece_pos[0], piece_pos[1], piece)

    def addpieces(self, *pieces):
        for piece in pieces:
            self.addpiece(piece)

    def inBoardBounds(self, posx, posy):
        return not (posx >= 9 or posx <= 0 or posy >= 9 or posy <= 0)

    def getpos(self, posx, posy):
        if self.inBoardBounds(posx, posy):
            piece = self.tiles[posy - 1][posx - 1]
        else:
            return None
        return piece

    def setpos(self, posx, posy, piece: Piece):
        self.tiles[posy - 1][posx - 1] = piece

    def print(self, color=True):
        playerorder = self.tiles.copy()
        if color:
            playerorder.reverse()
        for row in playerorder:
            for item in row:
                if item is None:
                    print("none,", end="")
                else:
                    if item.getColor():
                        print("w", end="")
                    else:
                        print("b", end="")
                    print(item.gettype().name + ",", end="")
            print("")


class SpecialMove(enum.Enum):
    king_castle = 0
    queen_castle = 1
    en_passant_trigger = 2
    en_passant = 3


class ChessLogic:

    def __init__(self):
        self.moveHistory = []

    def validateMove(self, startPos, endPos, board: ChessBoard, check_for_check=True):
        # if move is not on board.
        if startPos[0] > 8 or startPos[1] > 8 or endPos[0] > 8 or endPos[1] > 8:
            return False

        piece = board.getpos(startPos[0], startPos[1])

        if piece is None:
            return False

        color = piece.getColor()
        piece_type = piece.gettype()

        if piece_type == PieceType.empty:
            return False

        if board.getpos(endPos[0], endPos[1]) is None:
            return False

        # if piece at end is same color
        if board.getpos(endPos[0], endPos[1]).gettype() != PieceType.empty \
                and board.getpos(endPos[0], endPos[1]).getColor() == piece.getColor():
            return False

        method_dict = {1: self.getValidPawnMoves,
                       2: self.getValidKingMoves,
                       3: self.getValidQueenMoves,
                       4: self.getValidRookMoves,
                       5: self.getValidBishopMoves,
                       6: self.getValidKnightMoves}
        move = self.move_in_list(startPos, endPos, method_dict[piece_type.value](startPos, board))
        if move:
            simboard = self.sim_move(move[0], move[1], board)
            if not check_for_check or not self.inCheck(color, simboard):
                self.moveHistory.append((startPos, endPos, board))
                return simboard
        return False

    def move_in_list(self, startpos, endpos, move_list):
        for move in move_list:
            if startpos == move[0] and endpos == (move[1][0], move[1][1]):
                return move
        return False

    def inCheck(self, color, board: ChessBoard):
        king_pos = self.findking(color, board)
        for i in range(len(board.tiles)):
            row = board.tiles[i]
            for j in range(len(row)):
                item = row[j]
                if item.gettype() != PieceType.empty and item.gettype() != PieceType.king:
                    if item.getColor() != color:
                        logic = ChessLogic()
                        if logic.validateMove((j + 1, i + 1), king_pos, board, False):
                            return True

    def move(self, piece, endpos, board):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        startpos = piece.getpos().getPosAsPair()

        piece.setpos(Pos(endpos[1], letters[endpos[0] - 1]))
        board.setpos(endpos[0], endpos[1], piece)
        board.setpos(startpos[0], startpos[1], Piece(0, "", False, PieceType.empty, False))

    def remove(self, taken_piece, board):
        taken_piece.setActive(False)
        if taken_piece.gettype() != PieceType.empty:
            taken_pos = taken_piece.getpos().getPosAsPair()
            board.setpos(taken_pos[0], taken_pos[1], Piece(0, "", False, PieceType.empty, False))

    def move_side_effects(self, piece, endpos, board):
        piece.setHasNotMoved(False)
        if piece.gettype() == PieceType.pawn and endpos[1] in [1, 8]:
            piece.settype(PieceType.queen)
        self.untrigger_en_passant(board, piece.getColor())

    def untrigger_en_passant(self, board, color):
        if color:
            pieces = board.getBlackPieces()
        else:
            pieces = board.getWhitePieces()
        for piece in pieces:
            if piece.gettype() == PieceType.pawn:
                piece.setEnPassant(False)

    def handle_special_moves(self, piece, endpos, board):
        if len(endpos) <= 2:
            return
        if endpos[2] == SpecialMove.king_castle:
            rook = board.getpos(8, piece.getpos().getPosAsPair()[1])
            self.move(rook, (6, piece.getpos().getPosAsPair()[1]), board)

        if endpos[2] == SpecialMove.queen_castle:
            rook = board.getpos(1, piece.getpos().getPosAsPair()[1])
            self.move(rook, (4, piece.getpos().getPosAsPair()[1]), board)
            pass

        if endpos[2] == SpecialMove.en_passant_trigger:
            king_side_piece = board.getpos(endpos[0] + 1, endpos[1])
            queen_side_piece = board.getpos(endpos[0] - 1, endpos[1])
            for adj_piece in [king_side_piece, queen_side_piece]:
                if adj_piece is not None and adj_piece.gettype() == PieceType.pawn:
                    piece.setEnPassant(True)
            pass

        if endpos[2] == SpecialMove.en_passant:
            taken_piece = board.getpos(endpos[0], piece.getpos().getPosAsPair()[1])
            self.remove(taken_piece, board)

    def sim_move(self, startpos, endpos, board):
        newboard = copy.deepcopy(board)

        piece = newboard.getpos(startpos[0], startpos[1])
        taken_piece = newboard.getpos(endpos[0], endpos[1])

        self.move_side_effects(piece, endpos, newboard)
        self.handle_special_moves(piece, endpos, newboard)
        self.remove(taken_piece, newboard)
        self.move(piece, endpos, newboard)

        return newboard

    def findking(self, color, board):
        for i in range(len(board.tiles)):
            row = board.tiles[i]
            for j in range(len(row)):
                item = row[j]
                if item.gettype() == PieceType.king:
                    if item.getColor() == color:
                        return j + 1, i + 1

    def getValidPawnMoves(self, startpos, board):
        piece = board.getpos(startpos[0], startpos[1])
        color = piece.getColor()
        if color:
            direction = 1
        else:
            direction = -1
        moves = []
        if board.getpos(startpos[0], startpos[1] + 1 * direction) is not None \
                and board.getpos(startpos[0], startpos[1] + 1 * direction).gettype() == PieceType.empty:
            moves.append((startpos, (startpos[0], startpos[1] + 1 * direction)))

        if ((color and startpos[1] == 2) or (not color and startpos[1] == 7)) \
                and board.getpos(startpos[0], startpos[1] + 2 * direction) is not None \
                and board.getpos(startpos[0], startpos[1] + 1 * direction).gettype() == PieceType.empty \
                and board.getpos(startpos[0], startpos[1] + 2 * direction).gettype() == PieceType.empty:

            en_passant_king_side = board.getpos(startpos[0] + 1, startpos[1] + 2 * direction)
            en_passant_queen_side = board.getpos(startpos[0] - 1, startpos[1] + 2 * direction)

            if self.canEnPassantTrigger(en_passant_king_side, color) \
                    or self.canEnPassantTrigger(en_passant_queen_side, color):
                moves.append((startpos, (startpos[0], startpos[1] + 2 * direction, SpecialMove.en_passant_trigger)))
            else:
                moves.append((startpos, (startpos[0], startpos[1] + 2 * direction)))

        if board.getpos(startpos[0] + 1, startpos[1] + 1 * direction) is not None \
                and board.getpos(startpos[0] + 1, startpos[1] + 1 * direction).gettype() != PieceType.empty \
                and board.getpos(startpos[0] + 1, startpos[1] + 1 * direction).getColor() != color:
            moves.append((startpos, (startpos[0] + 1, startpos[1] + 1 * direction)))

        if board.getpos(startpos[0] - 1, startpos[1] + 1 * direction) is not None \
                and board.getpos(startpos[0] - 1, startpos[1] + 1 * direction).gettype() != PieceType.empty \
                and board.getpos(startpos[0] - 1, startpos[1] + 1 * direction).getColor() != color:
            moves.append((startpos, (startpos[0] - 1, startpos[1] + 1 * direction)))

        moves.extend(self.getEnPassant(startpos, color, direction, board))

        return moves

    def canEnPassantTrigger(self, piece, color):
        return piece is not None and piece.gettype() == PieceType.pawn and piece.getColor() != color

    def getEnPassant(self, startpos, color, direction, board):
        moves = []

        if board.getpos(startpos[0] - 1, startpos[1] + 1 * direction) is not None \
                and board.getpos(startpos[0] - 1, startpos[1] + 1 * direction).gettype() == PieceType.empty \
                and board.getpos(startpos[0] - 1, startpos[1]).getColor() != color \
                and board.getpos(startpos[0] - 1, startpos[1]).getEnPassant():
            moves.append((startpos, (startpos[0] - 1, startpos[1] + 1 * direction, SpecialMove.en_passant)))

        if board.getpos(startpos[0] + 1, startpos[1] + 1 * direction) is not None \
                and board.getpos(startpos[0] + 1, startpos[1] + 1 * direction).gettype() == PieceType.empty \
                and board.getpos(startpos[0] + 1, startpos[1]).getColor() != color \
                and board.getpos(startpos[0] + 1, startpos[1]).getEnPassant():
            moves.append((startpos, (startpos[0] + 1, startpos[1] + 1 * direction, SpecialMove.en_passant)))

        return moves

    def getValidKingMoves(self, startpos, board):
        moves = []
        king_pairs = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        color = board.getpos(startpos[0], startpos[1]).getColor()
        for pair in king_pairs:
            if self.isEnemyOrEmpty(color, (startpos[0] + pair[0], startpos[1] + pair[1]), board):
                moves.append((startpos, (startpos[0] + pair[0], startpos[1] + pair[1])))
        if self.canCastleKingSide(startpos, color, board):
            moves.append((startpos, (startpos[0] + 2, startpos[1], SpecialMove.king_castle)))

        if self.canCastleQueenSide(startpos, color, board):
            moves.append((startpos, (startpos[0] - 2, startpos[1], SpecialMove.queen_castle)))
        return moves

    def canCastleKingSide(self, startpos, color, board):
        if self.inCheck(color, board):
            return False
        rook = board.getpos(8, startpos[1])
        king = board.getpos(startpos[0], startpos[1])
        if rook is None or king is None or rook.gettype() != PieceType.rook or king.gettype() != PieceType.king:
            return False
        if not rook.getHasNotMoved() or not king.getHasNotMoved():
            return False
        if not board.getpos(7, startpos[1]).gettype() == PieceType.empty \
                and board.getpos(6, startpos[1]) == PieceType.empty:
            return False
        simboard = self.sim_move(startpos, (6, startpos[1]), board)
        if self.inCheck(color, simboard):
            return False
        return True

    def canCastleQueenSide(self, startpos, color, board):
        if self.inCheck(color, board):
            return False
        rook = board.getpos(1, startpos[1])
        king = board.getpos(startpos[0], startpos[1])
        if rook is None or king is None or rook.gettype() != PieceType.rook or king.gettype() != PieceType.king:
            return False
        if not rook.getHasNotMoved() or not king.getHasNotMoved():
            return False
        if not board.getpos(4, startpos[1]).gettype() == PieceType.empty \
                and board.getpos(3, startpos[1]) == PieceType.empty:
            return False
        simboard = self.sim_move(startpos, (4, startpos[1]), board)
        if self.inCheck(color, simboard):
            return False
        return True

    def getValidKnightMoves(self, startpos, board):
        moves = []
        knight_pairs = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        color = board.getpos(startpos[0], startpos[1]).getColor()
        for pair in knight_pairs:
            if self.isEnemyOrEmpty(color, (startpos[0] + pair[0], startpos[1] + pair[1]), board):
                moves.append((startpos, (startpos[0] + pair[0], startpos[1] + pair[1])))
        return moves

    def isEnemyOrEmpty(self, color, endpos, board):
        if board.getpos(endpos[0], endpos[1]) is None:
            return False
        if board.getpos(endpos[0], endpos[1]).gettype() == PieceType.empty:
            return True
        if board.getpos(endpos[0], endpos[1]).getColor() != color:
            return True
        return False

    def getValidRookMoves(self, startpos, board):
        color = board.getpos(startpos[0], startpos[1]).getColor()
        moves = []
        rook_pairs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for pair in rook_pairs:
            moves.extend(self.iterateMoves(board, color, startpos, pair[0], pair[1]))
        return moves

    def getValidBishopMoves(self, startpos, board):
        color = board.getpos(startpos[0], startpos[1]).getColor()
        moves = []
        bishop_pairs = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for pair in bishop_pairs:
            moves.extend(self.iterateMoves(board, color, startpos, pair[0], pair[1]))
        return moves

    def getValidQueenMoves(self, startpos, board):
        moves = []
        moves.extend(self.getValidBishopMoves(startpos, board))
        moves.extend(self.getValidRookMoves(startpos, board))
        return moves

    def iterateMoves(self, board, color, startpos, horistep, vertstep):
        moves = []

        i, j = startpos[0] + horistep, startpos[1] + vertstep

        while board.getpos(i, j) is not None:
            piece = board.getpos(i, j)
            if piece.gettype() != PieceType.empty:
                if piece.getColor() != color:
                    moves.append((startpos, (i, j)))
                break
            moves.append((startpos, (i, j)))
            i += horistep
            j += vertstep
        return moves

    def getAnyMoves(self, color, board: ChessBoard):
        if color:
            pieces = board.getWhitePieces()
        else:
            pieces = board.getBlackPieces()

        method_dict = {1: self.getValidPawnMoves,
                       2: self.getValidKingMoves,
                       3: self.getValidQueenMoves,
                       4: self.getValidRookMoves,
                       5: self.getValidBishopMoves,
                       6: self.getValidKnightMoves}

        for piece in pieces:
            if not piece.getActive():
                continue
            startpos = piece.getpos().getPosAsPair()
            piecetype = piece.gettype()
            for move in method_dict[piecetype.value](startpos, board):
                simboard = self.sim_move(move[0], move[1], board)
                if not self.inCheck(color, simboard):
                    return True
        return False

    def checkState(self, board, color):
        white_has_moves = self.getAnyMoves(True, board)
        black_has_moves = self.getAnyMoves(False, board)
        if self.inCheck(True, board):
            if white_has_moves:
                return ChessState.whiteChecked
            else:
                return ChessState.whiteCheckmated
        if self.inCheck(False, board):
            if black_has_moves:
                return ChessState.blackChecked
            else:
                return ChessState.blackCheckmated
        if (not white_has_moves and color) or (not black_has_moves and not color):
            return ChessState.draw
        return ChessState.inProgress

class Chess:
    board = ChessBoard()
    board.setStartBoard()
    logic = ChessLogic()
    color = True

    def make_move(self, start, end):
        startpos = self.chessToInts(start)
        endpos = self.chessToInts(end)
        piece = self.board.getpos(startpos[0], startpos[1])
        if piece is None:
            return False
        if piece.gettype() == PieceType.empty or self.color != piece.getColor():
            return False

        move_result = self.logic.validateMove(startpos, endpos, self.board)
        if move_result:
            self.board = move_result
            self.color = not self.color
            return True
        return False

    def chessToInts(self, chessPos):
        return Pos.colDict.get(chessPos[0]), int(chessPos[1])

    def getState(self):
        return self.logic.checkState(self.board, self.color)

    def printBoard(self):
        b = board.Board()
        color_dict = {True: board.PieceColor.WHITE, False: board.PieceColor.BLACK}
        p_t_d = {PieceType.pawn: (board.PieceType.PAWN, board.b_pawn_img, board.w_pawn_img),
                 PieceType.king: (board.PieceType.KING, board.b_king_img, board.w_king_img),
                 PieceType.queen: (board.PieceType.QUEEN, board.b_queen_img, board.w_queen_img),
                 PieceType.rook: (board.PieceType.ROOK, board.b_rook_img, board.w_rook_img),
                 PieceType.bishop: (board.PieceType.BISHOP, board.b_bishop_img, board.w_bishop_img),
                 PieceType.knight: (board.PieceType.KNIGHT, board.b_knight_img, board.w_knight_img)}

        all_pieces = (self.board.getWhitePieces(), self.board.getBlackPieces())
        updated_pieces = ([], [])

        for i in range(len(all_pieces)):
            for piece in all_pieces[i]:
                if not piece.getActive():
                    continue
                type = piece.gettype()
                color = piece.getColor()
                piece_color = color_dict.get(color)
                piece_info = p_t_d.get(type)
                white_piece = board.Piece(piece_info[0],
                                          piece_color,
                                          piece_info[piece_color.value+1],
                                          piece.getPosAsString())
                updated_pieces[i].append(white_piece)

        return updated_pieces

