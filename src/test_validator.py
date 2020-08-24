from unittest import TestCase
import chess


class TestValidator(TestCase):
    def setUp(self):
        self.board = chess.ChessBoard()
        self.logic = chess.ChessLogic()
        self.board.setEmptyBoard()

    def test_validator_pawn_opening(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wpawn = chess.Piece(2, "H", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(7, "H", True, chess.PieceType.pawn, False)
        self.board.addpieces(bking, wking, wpawn, bpawn)

        new_board = self.logic.validateMove((8, 2), (8, 3), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(8, 2).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 3).gettype() == chess.PieceType.pawn)

        new_board = self.logic.validateMove((8, 2), (8, 4), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(8, 2).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 3).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 4).gettype() == chess.PieceType.pawn)

        new_board = self.logic.validateMove((8, 7), (8, 6), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(8, 7).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 6).gettype() == chess.PieceType.pawn)

        new_board = self.logic.validateMove((8, 7), (8, 5), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(8, 7).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 6).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 5).gettype() == chess.PieceType.pawn)

    def test_validator_pawn_standard(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wpawn = chess.Piece(3, "H", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(6, "H", True, chess.PieceType.pawn, False)
        self.board.addpieces(bking, wking, wpawn, bpawn)

        new_board = self.logic.validateMove((8, 3), (8, 4), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(8, 3).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 4).gettype() == chess.PieceType.pawn)

        new_board = self.logic.validateMove((8, 6), (8, 5), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(8, 6).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 5).gettype() == chess.PieceType.pawn)

    def test_validator_pawn_capture(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wpawn = chess.Piece(3, "G", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(6, "G", True, chess.PieceType.pawn, False)
        wpawn2 = chess.Piece(5, "H", True, chess.PieceType.pawn, True)
        wpawn3 = chess.Piece(5, "F", True, chess.PieceType.pawn, True)
        bpawn2 = chess.Piece(4, "F", True, chess.PieceType.pawn, False)
        bpawn3 = chess.Piece(4, "H", True, chess.PieceType.pawn, False)


        self.board.addpieces(bking, wking, wpawn, bpawn, wpawn2, wpawn3, bpawn2, bpawn3)

        new_board = self.logic.validateMove((7, 3), (6, 4), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(7, 3).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(6, 4).gettype() == chess.PieceType.pawn)
        self.assertTrue(new_board.getpos(6, 4).getColor())

        new_board = self.logic.validateMove((7, 3), (8, 4), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(7, 3).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 4).gettype() == chess.PieceType.pawn)
        self.assertTrue(new_board.getpos(8, 4).getColor())

        new_board = self.logic.validateMove((7, 6), (6, 5), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(7, 6).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(6, 5).gettype() == chess.PieceType.pawn)
        self.assertFalse(new_board.getpos(6, 5).getColor())

        new_board = self.logic.validateMove((7, 6), (8, 5), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(7, 6).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 5).gettype() == chess.PieceType.pawn)
        self.assertFalse(new_board.getpos(8, 5).getColor())

    def test_validator_pawn_en_passant(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wpawn = chess.Piece(3, "G", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(6, "G", True, chess.PieceType.pawn, False)
        wpawn2 = chess.Piece(6, "H", True, chess.PieceType.pawn, True)
        wpawn3 = chess.Piece(6, "F", True, chess.PieceType.pawn, True)
        bpawn2 = chess.Piece(3, "F", True, chess.PieceType.pawn, False)
        bpawn3 = chess.Piece(3, "H", True, chess.PieceType.pawn, False)

        self.board.addpieces(bking, wking, wpawn, bpawn, wpawn2, wpawn3, bpawn2, bpawn3)
        bpawn2.setEnPassant(True)
        bpawn3.setEnPassant(True)
        wpawn2.setEnPassant(True)
        wpawn3.setEnPassant(True)


        new_board = self.logic.validateMove((7, 3), (6, 4), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(7, 3).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(6, 4).gettype() == chess.PieceType.pawn)
        self.assertTrue(new_board.getpos(6, 4).getColor())

        new_board = self.logic.validateMove((7, 3), (8, 4), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(7, 3).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 4).gettype() == chess.PieceType.pawn)
        self.assertTrue(new_board.getpos(8, 4).getColor())

        new_board = self.logic.validateMove((7, 6), (6, 5), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(7, 6).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(6, 5).gettype() == chess.PieceType.pawn)
        self.assertFalse(new_board.getpos(6, 5).getColor())

        new_board = self.logic.validateMove((7, 6), (8, 5), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(7, 6).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 5).gettype() == chess.PieceType.pawn)
        self.assertFalse(new_board.getpos(8, 5).getColor())

    def test_validator_pawn_promotion(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wpawn = chess.Piece(7, "H", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(2, "H", True, chess.PieceType.pawn, False)
        self.board.addpieces(bking, wking, wpawn, bpawn)

        new_board = self.logic.validateMove((8, 7), (8, 8), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(8, 7).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 8).gettype() == chess.PieceType.queen)

        new_board = self.logic.validateMove((8, 2), (8, 1), self.board)
        self.assertTrue(new_board)
        self.assertTrue(new_board.getpos(8, 2).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(8, 1).gettype() == chess.PieceType.queen)




    def test_validator_rook_standard(self):
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
        self.assertTrue(set(self.logic.getValidRookMoves(brook.getpos().getPosAsPair(), self.board)) == set(brookmoves))

    def test_validator_rook_capture(self):
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
        new_board = self.logic.validateMove((5, 4), (2, 4), self.board)
        self.assertTrue(new_board.getpos(5, 4).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(2, 4).gettype() == chess.PieceType.rook)

    def test_validator_rook_castle(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        wrook = chess.Piece(1, "A", True, chess.PieceType.rook, True)
        brook = chess.Piece(8, "H", True, chess.PieceType.rook, False)
        self.board.addpieces(wking, bking, wrook, brook)

        newboard = self.logic.validateMove((5, 1), (3, 1), self.board)
        self.assertTrue(newboard.getpos(3, 1).gettype() == chess.PieceType.king)
        self.assertTrue(newboard.getpos(4, 1).gettype() == chess.PieceType.rook)
        newboard = self.logic.validateMove((5, 8), (7, 8), self.board)
        self.assertTrue(newboard.getpos(7, 8).gettype() == chess.PieceType.king)
        self.assertTrue(newboard.getpos(6, 8).gettype() == chess.PieceType.rook)

    def test_validator_knight_standard(self):
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

    def test_validator_knight_capture(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        bknight = chess.Piece(6, "D", True, chess.PieceType.knight, False)
        wpawn = chess.Piece(7, "F", True, chess.PieceType.pawn, True)

        self.board.addpieces(wking, bking, bknight)
        bknightmoves = [((4, 6), (6, 7)),
                        ((4, 6), (6, 5)),
                        ((4, 6), (5, 4)),
                        ((4, 6), (2, 5)),
                        ((4, 6), (2, 7)),
                        ((4, 6), (3, 4)),
                        ((4, 6), (3, 8))]

        new_board = self.logic.validateMove((4, 6), (6, 7), self.board)
        self.assertTrue(new_board.getpos(4, 6).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(6, 7).gettype() == chess.PieceType.knight)

    def test_validator_bishop_standard(self):
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

        self.assertTrue(
            set(self.logic.getValidBishopMoves(wbishop.getpos().getPosAsPair(), self.board)) == set(wbishopmoves))

    def test_validator_bishop_capture(self):
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

        new_board = self.logic.validateMove((5, 4), (3, 6), self.board)
        self.assertTrue(new_board.getpos(5, 4).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(3, 6).gettype() == chess.PieceType.bishop)


    def test_validator_queen_standard(self):
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

    def test_validator_queen_capture(self):
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

        new_board = self.logic.validateMove((5, 4), (3, 6), self.board)
        self.assertTrue(new_board.getpos(5, 4).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(3, 6).gettype() == chess.PieceType.queen)

    def test_validator_king_standard(self):
        wking = chess.Piece(4, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(7, "H", True, chess.PieceType.king, False)
        wpawn = chess.Piece(4, "D", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(4, "F", True, chess.PieceType.pawn, False)

        self.board.addpieces(wking, bking, wpawn, bpawn)

        wkingmoves = [((5, 4), (6, 5)),
                       ((5, 4), (4, 3)),
                       ((5, 4), (4, 5)),
                       ((5, 4), (6, 3)),
                       ((5, 4), (6, 4)),
                       ((5, 4), (5, 3)),
                       ((5, 4), (5, 5))]

        self.assertTrue(
            set(self.logic.getValidKingMoves(wking.getpos().getPosAsPair(), self.board)) == set(wkingmoves))

    def test_validator_king_capture(self):
        wking = chess.Piece(4, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(7, "H", True, chess.PieceType.king, False)
        wpawn = chess.Piece(4, "D", True, chess.PieceType.pawn, True)
        bpawn = chess.Piece(4, "F", True, chess.PieceType.pawn, False)

        self.board.addpieces(wking, bking, wpawn, bpawn)

        wkingmoves = [((5, 4), (6, 5)),
                      ((5, 4), (4, 3)),
                      ((5, 4), (4, 5)),
                      ((5, 4), (6, 3)),
                      ((5, 4), (6, 4)),
                      ((5, 4), (5, 3)),
                      ((5, 4), (5, 5))]

        new_board = self.logic.validateMove((5, 4), (6, 4), self.board)
        self.assertTrue(new_board.getpos(5, 4).gettype() == chess.PieceType.empty)
        self.assertTrue(new_board.getpos(6, 4).gettype() == chess.PieceType.king)

    def test_validator_check_state(self):
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
        self.board.addpieces(wking, bking, bqueen)
        self.assertTrue(self.logic.checkState(self.board, True) == chess.ChessState.whiteChecked)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wqueen)
        self.assertTrue(self.logic.checkState(self.board, False) == chess.ChessState.blackChecked)

    def test_validator_checkmate_state(self):
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

        self.board.addpieces(wking, bking, brook, bqueen)
        self.assertTrue(self.logic.checkState(self.board, True) == chess.ChessState.whiteCheckmated)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, wrook, wqueen)
        self.assertTrue(self.logic.checkState(self.board, False) == chess.ChessState.blackCheckmated)


    def test_validator_stalemate_state(self):
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
        self.board.addpieces(wking, bking, wbishop, wqueen2)

        self.assertTrue(self.logic.checkState(self.board, False) == chess.ChessState.draw)
        self.board.setEmptyBoard()
        self.board.addpieces(wking, bking, bbishop, bqueen2)
        self.assertTrue(self.logic.checkState(self.board, True) == chess.ChessState.draw)

    def test_validator_check_move(self):
        wking = chess.Piece(1, "E", True, chess.PieceType.king, True)
        bking = chess.Piece(8, "E", True, chess.PieceType.king, False)
        bqueen = chess.Piece(2, "E", True, chess.PieceType.queen, False)
        self.board.addpieces(wking, bking, bqueen)
        self.assertTrue(self.logic.checkState(self.board, True) == chess.ChessState.whiteChecked)
        pos = wking.getpos().getPosAsPair()
        for move in self.logic.getValidKingMoves(pos, self.board):
            new_board = self.logic.validateMove(move[0], (move[1][0], move[1][1]), self.board)
            if new_board:
                self.assertFalse(self.logic.checkState(new_board, True) == chess.ChessState.whiteChecked)
