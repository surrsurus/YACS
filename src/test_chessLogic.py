from unittest import TestCase
import Chess


class TestChessLogic(TestCase):
    def setUp(self):
        board = Chess.ChessBoard()

    def test_validateMove(self):
        self.fail()

    def test_inCheck(self):
        self.fail()

    def test_move(self):
        # move piece, assert newpos, oldpos and value of pos
        board = Chess.ChessBoard()
        logic = Chess.ChessLogic()
        board.setEmptyBoard()
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        board.addpiece(wking)
        board.addpiece(bking)
        logic.move(wking, (6, 1), board)
        self.assertTrue(board.getpos(6, 1) is wking)
        self.assertTrue(board.getpos(5, 1).gettype() == Chess.PieceType.empty)
        self.assertTrue(wking.getpos().getPosAsPair() == (6, 1))

    def test_remove(self):
        board = Chess.ChessBoard()
        logic = Chess.ChessLogic()
        board.setEmptyBoard()
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        board.addpiece(wking)
        board.addpiece(bking)
        logic.remove(wking, board)
        self.assertFalse(wking.active)
        self.assertTrue(board.getpos(5, 1).gettype() == Chess.PieceType.empty)

    def test_move_side_effects(self):
        board = Chess.ChessBoard()
        logic = Chess.ChessLogic()
        board.setEmptyBoard()
        wking = Chess.Piece(1, "E", True, Chess.PieceType.king, True)
        bking = Chess.Piece(8, "E", True, Chess.PieceType.king, False)
        wpawn = Chess.Piece(7, "H", True, Chess.PieceType.pawn, True)
        bpawn = Chess.Piece(4, "H", True, Chess.PieceType.pawn, False)
        bpawn.setEnPassant(True)
        board.addpiece(wking)
        board.addpiece(bking)
        board.addpiece(wpawn)
        board.addpiece(bpawn)
        logic.move_side_effects(wpawn, (8, 8), board)
        self.assertTrue(wpawn.gettype() == Chess.PieceType.queen)
        self.assertFalse(bpawn.getEnPassant())
        logic.move_side_effects(wking, (6, 1), board)
        self.assertFalse(wking.getCanCastle())
        self.assertTrue(bking.getCanCastle())

    def test_handle_special_moves(self):
        self.fail()

    def test_sim_move(self):
        self.fail()

    def test_findking(self):
        self.fail()

    def test_getValidPawnMoves(self):
        board = Chess.ChessBoard()
        logic = Chess.ChessLogic()
        board.setEmptyBoard()
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
        bpawn.setEnPassant(True)
        board.addpiece(wking)
        board.addpiece(bking)
        board.addpiece(wpawn)
        board.addpiece(bpawn)
        board.addpiece(wpawn2)
        board.addpiece(wpawn3)
        board.addpiece(bpawn2)
        board.addpiece(wpawn4)
        board.addpiece(bpawn3)
        board.addpiece(wpawn5)
        self.assertTrue(
            logic.getValidPawnMoves(wpawn.getpos().getPosAsPair(), board) == [((8, 7), (8, 8))])
        self.assertTrue(
            logic.getValidPawnMoves(bpawn.getpos().getPosAsPair(), board) == [((7, 4), (7, 3)), ((7, 4), (8, 3))])
        self.assertTrue(
            logic.getValidPawnMoves(wpawn2.getpos().getPosAsPair(), board) == [((8, 3), (8, 4)), ((8, 3), (7, 4))])
        self.assertTrue(
            logic.getValidPawnMoves(wpawn3.getpos().getPosAsPair(), board) == [((5, 3), (5, 4))])
        self.assertTrue(
            logic.getValidPawnMoves(
                bpawn2.getpos().getPosAsPair(), board) == [((6, 3), (6, 2)),
                                                           ((6, 3), (5, 2, Chess.SpecialMove.en_passant))])
        self.assertTrue(
            logic.getValidPawnMoves(wpawn4.getpos().getPosAsPair(), board) == [((1, 2), (1, 3)), ((1, 2), (1, 4))])
        self.assertTrue(
            logic.getValidPawnMoves(wpawn5.getpos().getPosAsPair(), board) == [((2, 2), (2, 3)), (
            (2, 2), (2, 4, Chess.SpecialMove.en_passant_trigger))])

    def test_canEnPassantTrigger(self):
        self.fail()

    def test_getEnPassant(self):
        self.fail()

    def test_getValidKingMoves(self):
        self.fail()

    def test_canCastleKingSide(self):
        self.fail()

    def test_canCastleQueenSide(self):
        self.fail()

    def test_getValidKnightMoves(self):
        self.fail()

    def test_isEnemyOrEmpty(self):
        self.fail()

    def test_getValidRookMoves(self):
        self.fail()

    def test_getValidBishopMoves(self):
        self.fail()

    def test_getValidQueenMoves(self):
        self.fail()

    def test_iterateMoves(self):
        self.fail()

    def test_getAnyMoves(self):
        self.fail()

    def test_checkState(self):
        self.fail()
