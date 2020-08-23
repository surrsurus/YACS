from unittest import TestCase
import chess


class TestChessLogic(TestCase):
    def setUp(self):
        self.board = chess.ChessBoard()
        self.logic = chess.ChessLogic()
        self.board.setEmptyBoard()

    def test_validateMove(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wrook = chess.Piece(3, "C", True, chess.PieceType.rook, True)
        wbishop = chess.Piece(3, "G", True, chess.PieceType.bishop, True)
        wrook2 = chess.Piece(3, "E", True, chess.PieceType.rook, True)
        bqueen = chess.Piece(7, "E", True, chess.PieceType.queen, False)
        bbishop = chess.Piece(4, "H", True, chess.PieceType.bishop, False)
        bbishop2 = chess.Piece(5, "A", True, chess.PieceType.bishop, False)
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

        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        self.board.addpiece(wking)
        self.board.addpiece(bking)
        self.logic.move(wking, (6, 1), self.board)
        self.assertTrue(self.board.getpos(6, 1) is wking)
        self.assertTrue(self.board.getpos(5, 1).gettype() == chess.PieceType.empty)
        self.assertTrue(wking.getpos().getPosAsPair() == (6, 1))

    def test_remove(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        self.board.addpiece(wking)
        self.board.addpiece(bking)
        self.logic.remove(wking, self.board)
        self.assertFalse(wking.active)
        self.assertTrue(self.board.getpos(5, 1).gettype() == chess.PieceType.empty)

    def test_move_side_effects(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wpawn = chess.Piece(7, "H", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(4, "H", True, chess.PieceType.pawn, False)
        bpawn.setEnPassant(True)
        self.board.addpiece(wking)
        self.board.addpiece(bking)
        self.board.addpiece(wpawn)
        self.board.addpiece(bpawn)
        self.logic.move_side_effects(wpawn, (8, 8), self.board)
        self.assertTrue(wpawn.gettype() == chess.PieceType.queen)
        self.assertFalse(bpawn.getEnPassant())
        self.logic.move_side_effects(wking, (6, 1), self.board)
        self.assertFalse(wking.getHasNotMoved())
        self.assertTrue(bking.getHasNotMoved())

    def test_sim_move(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wrook = chess.Piece(1, "A", True, chess.PieceType.rook, True)
        brook = chess.Piece(8, "H", True, chess.PieceType.rook, False)
        wpawn = chess.Piece(5, "G", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(5, "H", True, chess.PieceType.pawn, False)
        bpawn2 = chess.Piece(7, "F", True, chess.PieceType.pawn, False)

        self.board.addpieces(wking, bking, wrook, brook, wpawn, bpawn, bpawn2)

        newboard = self.logic.sim_move((5, 1), (3, 1, chess.SpecialMove.queen_castle), self.board)
        self.assertTrue(newboard.getpos(3, 1).gettype() == chess.PieceType.king)
        self.assertTrue(newboard.getpos(4, 1).gettype() == chess.PieceType.rook)
        newboard = self.logic.sim_move((5, 8), (7, 8, chess.SpecialMove.king_castle), self.board)
        self.assertTrue(newboard.getpos(7, 8).gettype() == chess.PieceType.king)
        self.assertTrue(newboard.getpos(6, 8).gettype() == chess.PieceType.rook)
        newboard = self.logic.sim_move((7, 5), (8, 6, chess.SpecialMove.en_passant), self.board)
        self.assertTrue(newboard.getpos(8, 6).gettype() == chess.PieceType.pawn)
        self.assertTrue(newboard.getpos(8, 5).gettype() == chess.PieceType.empty)
        newboard = self.logic.sim_move((8, 5), (7, 4, chess.SpecialMove.en_passant), self.board)
        self.assertTrue(newboard.getpos(7, 4).gettype() == chess.PieceType.pawn)
        self.assertTrue(newboard.getpos(7, 5).gettype() == chess.PieceType.empty)
        newboard = self.logic.sim_move((6, 7), (6, 5, chess.SpecialMove.en_passant_trigger), self.board)
        self.assertTrue(newboard.getpos(6, 5).getEnPassant())




    def test_getValidPawnMoves(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wpawn = chess.Piece(7, "H", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(4, "G", True, chess.PieceType.pawn, False)
        wpawn2 = chess.Piece(3, "H", True, chess.PieceType.pawn, True)
        bpawn2 = chess.Piece(3, "F", True, chess.PieceType.pawn, False)
        wpawn3 = chess.Piece(3, "E", True, chess.PieceType.pawn, True)
        wpawn4 = chess.Piece(2, "A", True, chess.PieceType.pawn, True)
        wpawn5 = chess.Piece(2, "B", True, chess.PieceType.pawn, True)
        bpawn3 = chess.Piece(4, "C", True, chess.PieceType.pawn, False)
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
                                                                ((6, 3), (5, 2, chess.SpecialMove.en_passant))])
        self.assertTrue(
            self.logic.getValidPawnMoves(wpawn4.getpos().getPosAsPair(), self.board) == [((1, 2), (1, 3)),
                                                                                         ((1, 2), (1, 4))])
        self.assertTrue(
            self.logic.getValidPawnMoves(wpawn5.getpos().getPosAsPair(), self.board) == [((2, 2), (2, 3)), (
                (2, 2), (2, 4, chess.SpecialMove.en_passant_trigger))])

    def test_getValidKingMoves(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wking2 = chess.Piece(4, "E", True, chess.PieceType.king, True)
        wking3 = chess.Piece(8, "H", True, chess.PieceType.king, True)
        wking4 = chess.Piece(4, "H", True, chess.PieceType.king, True)
        wpawn = chess.Piece(7, "E", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(7, "D", True, chess.PieceType.pawn, False)
        wrook = chess.Piece(1, "A", True, chess.PieceType.rook, True)
        wrook2 = chess.Piece(1, "H", True, chess.PieceType.rook, True)

        self.board.addpieces(wking, bking, wking2, wking3, wking4, wpawn, bpawn, wrook, wrook2)
        wkingmoves = [((5, 1), (6, 1)),
                      ((5, 1), (6, 2)),
                      ((5, 1), (4, 1)),
                      ((5, 1), (4, 2)),
                      ((5, 1), (5, 2)),
                      ((5, 1), (7, 1, chess.SpecialMove.king_castle)),
                      ((5, 1), (3, 1, chess.SpecialMove.queen_castle))]
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
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        bknight = chess.Piece(6, "D", True, chess.PieceType.knight, False)
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
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        brook = chess.Piece(4, "E", True, chess.PieceType.rook, False)
        wpawn = chess.Piece(4, "B", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(4, "G", True, chess.PieceType.pawn, False)

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
        wking = chess.Piece(1, "H", True, chess.PieceType.king, True)
        bking = chess.Piece(7, "H", True, chess.PieceType.king, False)
        wbishop = chess.Piece(4, "E", True, chess.PieceType.bishop, True)
        wpawn = chess.Piece(2, "C", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(6, "C", True, chess.PieceType.pawn, False)

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
        wking = chess.Piece(1, "H", True, chess.PieceType.king, True)
        bking = chess.Piece(7, "H", True, chess.PieceType.king, False)
        wqueen = chess.Piece(4, "E", True, chess.PieceType.queen, True)
        wpawn = chess.Piece(2, "C", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(6, "C", True, chess.PieceType.pawn, False)

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
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wrook1 = chess.Piece(8, "A", True, chess.PieceType.rook, True)
        wrook2 = chess.Piece(7, "B", True, chess.PieceType.rook, True)
        self.board.addpiece(wking)
        self.board.addpiece(bking)
        self.board.addpiece(wrook1)
        self.board.addpiece(wrook2)
        self.assertFalse(self.logic.getAnyMoves(False, self.board))
        self.assertTrue(self.logic.getAnyMoves(True, self.board))

    def test_checkState(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        brook = chess.Piece(3, "E", True, chess.PieceType.rook, False)
        bqueen = chess.Piece(2, "E", True, chess.PieceType.queen, False)
        wrook = chess.Piece(6, "E", True, chess.PieceType.rook, True)
        wqueen = chess.Piece(7, "E", True, chess.PieceType.queen, True)
        wqueen2 = chess.Piece(6, "E", True, chess.PieceType.queen, True)
        wbishop = chess.Piece(7, "E", True, chess.PieceType.bishop, True)
        bqueen2 = chess.Piece(3, "E", True, chess.PieceType.queen, False)
        bbishop = chess.Piece(2, "E", True, chess.PieceType.bishop, False)
        self.board.addpieces(wking, bking)
        self.assertTrue(self.logic.checkState(self.board, True) == chess.ChessState.inProgress)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, bqueen)
        self.assertTrue(self.logic.checkState(self.board, True) == chess.ChessState.whiteChecked)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, brook)
        self.assertTrue(self.logic.checkState(self.board, True) == chess.ChessState.whiteChecked)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, brook, bqueen)
        self.assertTrue(self.logic.checkState(self.board, True) == chess.ChessState.whiteCheckmated)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wqueen)
        self.assertTrue(self.logic.checkState(self.board, False) == chess.ChessState.blackChecked)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wrook)
        self.assertTrue(self.logic.checkState(self.board, False) == chess.ChessState.blackChecked)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wrook, wqueen)
        self.assertTrue(self.logic.checkState(self.board, False) == chess.ChessState.blackCheckmated)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wbishop, wqueen2)
        self.assertTrue(self.logic.checkState(self.board, False) == chess.ChessState.draw)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, bbishop, bqueen2)
        self.assertTrue(self.logic.checkState(self.board, True) == chess.ChessState.draw)
