from unittest import TestCase
import Chess


class TestChessLogic(TestCase):
    def setUp(self):
        self.board = Chess.ChessBoard()
        self.logic = Chess.ChessLogic()
        self.board.setEmptyBoard()

    def test_validateMove(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        wrook = Chess.Piece(3, "C", True, Chess.PieceType.rook, True)
        wbishop = Chess.Piece(3, "G", True, Chess.PieceType.bishop, True)
        wrook2 = Chess.Piece(3, "E", True, Chess.PieceType.rook, True)
        bqueen = Chess.Piece(7, "E", True, Chess.PieceType.queen, False)
        bbishop = Chess.Piece(4, "H", True, Chess.PieceType.bishop, False)
        bbishop2 = Chess.Piece(5, "A", True, Chess.PieceType.bishop, False)
        self.board.addpieces(wking, bking, wrook, wbishop, wrook, wrook2)

        self.assertTrue(self.logic.validateMove((5, 3), (5, 4), self.board))
        self.assertTrue(self.logic.validateMove((5, 1), (4, 2), self.board))
        self.assertTrue(self.logic.validateMove((5, 8), (6, 7), self.board))
        self.assertTrue(self.logic.validateMove((3, 3), (3, 8), self.board))
        self.assertTrue(self.logic.validateMove((7, 3), (2, 8), self.board))

        self.board.addpieces(bqueen, bbishop, bbishop2)

        self.assertTrue(self.logic.validateMove((5, 3), (5, 4), self.board))
        self.assertFalse(self.logic.validateMove((5, 3), (4, 3), self.board))
        self.assertTrue(self.logic.validateMove((5, 1), (4, 2), self.board))
        self.assertTrue(self.logic.validateMove((5, 8), (6, 7), self.board))
        self.assertFalse(self.logic.validateMove((3, 3), (3, 8), self.board))
        self.assertFalse(self.logic.validateMove((7, 3), (2, 8), self.board))
        self.assertTrue(self.logic.validateMove((7, 3), (2, 8), self.board, False))
        self.assertTrue(self.logic.validateMove((7, 3), (8, 4), self.board))

    def test_move(self):

        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        self.board.addpiece(wking)
        self.board.addpiece(bking)
        self.logic.move(wking, (6, 1), self.board)
        self.assertTrue(self.board.getpos(6, 1) is wking)
        self.assertTrue(self.board.getpos(5, 1).gettype() == Chess.PieceType.empty)
        self.assertTrue(wking.getpos().getPosAsPair() == (6, 1))

    def test_remove(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        self.board.addpiece(wking)
        self.board.addpiece(bking)
        self.logic.remove(wking, self.board)
        self.assertFalse(wking.active)
        self.assertTrue(self.board.getpos(5, 1).gettype() == Chess.PieceType.empty)

    def test_move_side_effects(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        wpawn = Chess.Piece(7, "H", True, Chess.PieceType.pawn, True)
        bpawn = Chess.Piece(4, "H", True, Chess.PieceType.pawn, False)
        bpawn.setEnPassant(True)
        self.board.addpiece(wking)
        self.board.addpiece(bking)
        self.board.addpiece(wpawn)
        self.board.addpiece(bpawn)
        self.logic.move_side_effects(wpawn, (8, 8), self.board)
        self.assertTrue(wpawn.gettype() == Chess.PieceType.queen)
        self.assertFalse(bpawn.getEnPassant())
        self.logic.move_side_effects(wking, (6, 1), self.board)
        self.assertFalse(wking.getHasNotMoved())
        self.assertTrue(bking.getHasNotMoved())

    def test_sim_move(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        wrook = Chess.Piece(1, "A", True, Chess.PieceType.rook, True)
        brook = Chess.Piece(8, "H", True, Chess.PieceType.rook, False)
        wpawn = Chess.Piece(5, "G", True, Chess.PieceType.pawn, True)
        bpawn = Chess.Piece(5, "H", True, Chess.PieceType.pawn, False)
        bpawn2 = Chess.Piece(7, "F", True, Chess.PieceType.pawn, False)

        self.board.addpieces(wking, bking, wrook, brook, wpawn, bpawn, bpawn2)

        newboard = self.logic.sim_move((5, 1), (3, 1, Chess.SpecialMove.queen_castle), self.board)
        self.assertTrue(newboard.getpos(3, 1).gettype() == Chess.PieceType.king)
        self.assertTrue(newboard.getpos(4, 1).gettype() == Chess.PieceType.rook)
        newboard = self.logic.sim_move((5, 8), (7, 8, Chess.SpecialMove.king_castle), self.board)
        self.assertTrue(newboard.getpos(7, 8).gettype() == Chess.PieceType.king)
        self.assertTrue(newboard.getpos(6, 8).gettype() == Chess.PieceType.rook)
        newboard = self.logic.sim_move((7, 5), (8, 6, Chess.SpecialMove.en_passant), self.board)
        self.assertTrue(newboard.getpos(8, 6).gettype() == Chess.PieceType.pawn)
        self.assertTrue(newboard.getpos(8, 5).gettype() == Chess.PieceType.empty)
        newboard = self.logic.sim_move((8, 5), (7, 4, Chess.SpecialMove.en_passant), self.board)
        self.assertTrue(newboard.getpos(7, 4).gettype() == Chess.PieceType.pawn)
        self.assertTrue(newboard.getpos(7, 5).gettype() == Chess.PieceType.empty)
        newboard = self.logic.sim_move((6, 7), (6, 5, Chess.SpecialMove.en_passant_trigger), self.board)
        self.assertTrue(newboard.getpos(6, 5).getEnPassant())




    def test_getValidPawnMoves(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        wpawn = Chess.Piece(7, "H", True, Chess.PieceType.pawn, True)
        bpawn = Chess.Piece(4, "G", True, Chess.PieceType.pawn, False)
        wpawn2 = Chess.Piece(3, "H", True, Chess.PieceType.pawn, True)
        bpawn2 = Chess.Piece(3, "F", True, Chess.PieceType.pawn, False)
        wpawn3 = Chess.Piece(3, "E", True, Chess.PieceType.pawn, True)
        wpawn4 = Chess.Piece(2, "A", True, Chess.PieceType.pawn, True)
        wpawn5 = Chess.Piece(2, "B", True, Chess.PieceType.pawn, True)
        bpawn3 = Chess.Piece(4, "C", True, Chess.PieceType.pawn, False)
        wpawn3.setEnPassant(True)
        self.board.addpieces(wking, bking, wpawn, wpawn2, wpawn3, wpawn4, wpawn5, bpawn, bpawn2, bpawn3)
        self.assertTrue(
            self.logic.getValidPawnMoves(wpawn.getpos().getPosAsPair(), self.board) == [((8, 7), (8, 8))])
        self.assertTrue(
            self.logic.getValidPawnMoves(bpawn.getpos().getPosAsPair(), self.board) == [((7, 4), (7, 3)),
                                                                                        ((7, 4), (8, 3))])
        self.assertTrue(
            self.logic.getValidPawnMoves(wpawn2.getpos().getPosAsPair(), self.board) == [((8, 3), (8, 4)),
                                                                                         ((8, 3), (7, 4))])
        self.assertTrue(
            self.logic.getValidPawnMoves(wpawn3.getpos().getPosAsPair(), self.board) == [((5, 3), (5, 4))])
        self.assertTrue(
            self.logic.getValidPawnMoves(
                bpawn2.getpos().getPosAsPair(), self.board) == [((6, 3), (6, 2)),
                                                           ((6, 3), (5, 2, Chess.SpecialMove.en_passant))])
        self.assertTrue(
            self.logic.getValidPawnMoves(wpawn4.getpos().getPosAsPair(), self.board) == [((1, 2), (1, 3)),
                                                                                         ((1, 2), (1, 4))])
        self.assertTrue(
            self.logic.getValidPawnMoves(wpawn5.getpos().getPosAsPair(), self.board) == [((2, 2), (2, 3)), (
                (2, 2), (2, 4, Chess.SpecialMove.en_passant_trigger))])

    def test_getValidKingMoves(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        wking2 = Chess.Piece(4, "E", True, Chess.PieceType.king, True)
        wking3 = Chess.Piece(8, "H", True, Chess.PieceType.king, True)
        wking4 = Chess.Piece(4, "H", True, Chess.PieceType.king, True)
        wpawn = Chess.Piece(7, "E", True, Chess.PieceType.pawn, True)
        bpawn = Chess.Piece(7, "D", True, Chess.PieceType.pawn, False)
        wrook = Chess.Piece(1, "A", True, Chess.PieceType.rook, True)
        wrook2 = Chess.Piece(1, "H", True, Chess.PieceType.rook, True)

        self.board.addpieces(wking, bking, wking2, wking3, wking4, wpawn, bpawn, wrook, wrook2)
        wkingmoves = [((5, 1), (6, 1)),
                      ((5, 1), (6, 2)),
                      ((5, 1), (4, 1)),
                      ((5, 1), (4, 2)),
                      ((5, 1), (5, 2)),
                      ((5, 1), (7, 1, Chess.SpecialMove.king_castle)),
                      ((5, 1), (3, 1, Chess.SpecialMove.queen_castle))]
        bkingmoves = [((5, 8), (6, 8)),
                      ((5, 8), (6, 7)),
                      ((5, 8), (4, 8)),
                      ((5, 8), (5, 7))]
        wking2moves = [((5, 4), (6, 4)),
                       ((5, 4), (6, 3)),
                       ((5, 4), (4, 4)),
                       ((5, 4), (4, 5)),
                       ((5, 4), (5, 5)),
                       ((5, 4), (5, 3)),
                       ((5, 4), (6, 5)),
                       ((5, 4), (4, 3))]
        self.assertTrue(set(self.logic.getValidKingMoves(wking.getpos().getPosAsPair(), self.board)) == set(wkingmoves))
        self.assertTrue(set(self.logic.getValidKingMoves(bking.getpos().getPosAsPair(), self.board)) == set(bkingmoves))
        self.assertTrue(
            set(self.logic.getValidKingMoves(wking2.getpos().getPosAsPair(), self.board)) == set(wking2moves))

    def test_getValidKnightMoves(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        bknight = Chess.Piece(6, "D", True, Chess.PieceType.knight, False)
        self.board.addpieces(wking, bking, bknight)
        bknightmoves = [((4, 6), (6, 7)),
                        ((4, 6), (6, 5)),
                        ((4, 6), (5, 4)),
                        ((4, 6), (2, 5)),
                        ((4, 6), (2, 7)),
                        ((4, 6), (3, 4)),
                        ((4, 6), (3, 8))]

        self.assertTrue(
            set(self.logic.getValidKnightMoves(bknight.getpos().getPosAsPair(), self.board)) == set(bknightmoves))

    def test_getValidRookMoves(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        brook = Chess.Piece(4, "E", True, Chess.PieceType.rook, False)
        wpawn = Chess.Piece(4, "B", True, Chess.PieceType.pawn, True)
        bpawn = Chess.Piece(4, "G", True, Chess.PieceType.pawn, False)

        self.board.addpieces(wking, bking, brook, wpawn, bpawn)

        brookmoves = [((5, 4), (4, 4)),
                      ((5, 4), (3, 4)),
                      ((5, 4), (2, 4)),
                      ((5, 4), (6, 4)),
                      ((5, 4), (5, 3)),
                      ((5, 4), (5, 2)),
                      ((5, 4), (5, 1)),
                      ((5, 4), (5, 5)),
                      ((5, 4), (5, 6)),
                      ((5, 4), (5, 7))]
        val = self.logic.getValidRookMoves(brook.getpos().getPosAsPair(), self.board)
        self.assertTrue(set(self.logic.getValidRookMoves(brook.getpos().getPosAsPair(), self.board)) == set(brookmoves))

    def test_getValidBishopMoves(self):
        wking = Chess.Piece(1, "H", True, Chess.PieceType.king, True)
        bking = Chess.Piece(7, "H", True, Chess.PieceType.king, False)
        wbishop = Chess.Piece(4, "E", True, Chess.PieceType.bishop, True)
        wpawn = Chess.Piece(2, "C", True, Chess.PieceType.pawn, True)
        bpawn = Chess.Piece(6, "C", True, Chess.PieceType.pawn, False)

        self.board.addpieces(wking, bking, wbishop, wpawn, bpawn)

        wbishopmoves = [((5, 4), (6, 5)),
                        ((5, 4), (7, 6)),
                        ((5, 4), (8, 7)),
                        ((5, 4), (4, 3)),
                        ((5, 4), (4, 5)),
                        ((5, 4), (3, 6)),
                        ((5, 4), (6, 3)),
                        ((5, 4), (7, 2))]

        val = self.logic.getValidBishopMoves(wbishop.getpos().getPosAsPair(), self.board)
        self.assertTrue(
            set(self.logic.getValidBishopMoves(wbishop.getpos().getPosAsPair(), self.board)) == set(wbishopmoves))

    def test_getValidQueenMoves(self):
        wking = Chess.Piece(1, "H", True, Chess.PieceType.king, True)
        bking = Chess.Piece(7, "H", True, Chess.PieceType.king, False)
        wqueen = Chess.Piece(4, "E", True, Chess.PieceType.queen, True)
        wpawn = Chess.Piece(2, "C", True, Chess.PieceType.pawn, True)
        bpawn = Chess.Piece(6, "C", True, Chess.PieceType.pawn, False)

        self.board.addpieces(wking, bking, wqueen, wpawn, bpawn)

        wqueenmoves = [((5, 4), (6, 5)),
                       ((5, 4), (7, 6)),
                       ((5, 4), (8, 7)),
                       ((5, 4), (4, 3)),
                       ((5, 4), (4, 5)),
                       ((5, 4), (3, 6)),
                       ((5, 4), (6, 3)),
                       ((5, 4), (7, 2)),
                       ((5, 4), (4, 4)),
                       ((5, 4), (3, 4)),
                       ((5, 4), (2, 4)),
                       ((5, 4), (1, 4)),
                       ((5, 4), (6, 4)),
                       ((5, 4), (7, 4)),
                       ((5, 4), (8, 4)),
                       ((5, 4), (5, 3)),
                       ((5, 4), (5, 2)),
                       ((5, 4), (5, 1)),
                       ((5, 4), (5, 5)),
                       ((5, 4), (5, 6)),
                       ((5, 4), (5, 7)),
                       ((5, 4), (5, 8))]

        self.assertTrue(
            set(self.logic.getValidQueenMoves(wqueen.getpos().getPosAsPair(), self.board)) == set(wqueenmoves))

    def test_getAnyMoves(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        wrook1 = Chess.Piece(8, "A", True, Chess.PieceType.rook, True)
        wrook2 = Chess.Piece(7, "B", True, Chess.PieceType.rook, True)
        self.board.addpiece(wking)
        self.board.addpiece(bking)
        self.board.addpiece(wrook1)
        self.board.addpiece(wrook2)
        self.assertFalse(self.logic.getAnyMoves(False, self.board))
        self.assertTrue(self.logic.getAnyMoves(True, self.board))

    def test_checkState(self):
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        brook = Chess.Piece(3, "E", True, Chess.PieceType.rook, False)
        bqueen = Chess.Piece(2, "E", True, Chess.PieceType.queen, False)
        wrook = Chess.Piece(6, "E", True, Chess.PieceType.rook, True)
        wqueen = Chess.Piece(7, "E", True, Chess.PieceType.queen, True)
        wqueen2 = Chess.Piece(6, "E", True, Chess.PieceType.queen, True)
        wbishop = Chess.Piece(7, "E", True, Chess.PieceType.bishop, True)
        bqueen2 = Chess.Piece(3, "E", True, Chess.PieceType.queen, False)
        bbishop = Chess.Piece(2, "E", True, Chess.PieceType.bishop, False)
        self.board.addpieces(wking, bking)
        self.assertTrue(self.logic.checkState(self.board, True) == Chess.ChessState.inProgress)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, bqueen)
        self.assertTrue(self.logic.checkState(self.board, True) == Chess.ChessState.whiteChecked)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, brook)
        self.assertTrue(self.logic.checkState(self.board, True) == Chess.ChessState.whiteChecked)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, brook, bqueen)
        self.assertTrue(self.logic.checkState(self.board, True) == Chess.ChessState.whiteCheckmated)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wqueen)
        self.assertTrue(self.logic.checkState(self.board, False) == Chess.ChessState.blackChecked)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wrook)
        self.assertTrue(self.logic.checkState(self.board, False) == Chess.ChessState.blackChecked)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wrook, wqueen)
        self.assertTrue(self.logic.checkState(self.board, False) == Chess.ChessState.blackCheckmated)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wbishop, wqueen2)
        self.assertTrue(self.logic.checkState(self.board, False) == Chess.ChessState.draw)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, bbishop, bqueen2)
        self.assertTrue(self.logic.checkState(self.board, True) == Chess.ChessState.draw)
