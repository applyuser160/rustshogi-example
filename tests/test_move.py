from rustshogi import Move, Address, ColorType, Piece, PieceType


class TestMove:
    def test_move_standart(self):
        mv = Move("1a2b")
        assert mv.is_drop() is False
        assert mv.is_promote() is False
        assert mv.get_from() == Address(1, 1)
        assert mv.get_to() == Address(2, 2)

    def test_move_drop(self):
        mv = Move("l*1a")
        assert mv.is_drop() is True
        assert mv.is_promote() is False
        assert mv.get_piece() == Piece(ColorType.White, PieceType.Lance)
        assert mv.get_to() == Address(1, 1)

    def test_move_promote(self):
        mv = Move("1a2b+")
        assert mv.is_drop() is False
        assert mv.is_promote() is True
        assert mv.get_from() == Address(1, 1)
        assert mv.get_to() == Address(2, 2)
