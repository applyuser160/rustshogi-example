from rustshogi import Move, Address, ColorType, Piece, PieceType


class TestMove:
    def test_move_standart(self):
        # Act
        mv1 = Move(csa="1a2b")
        mv2 = Move(from_address=Address(1, 1), to_address=Address(2, 2))

        # Assert
        assert mv1.is_drop() is False
        assert mv1.is_promote() is False
        assert mv1.get_from() == Address(1, 1)
        assert mv1.get_to() == Address(2, 2)

        assert mv2.is_drop() is False
        assert mv2.is_promote() is False
        assert mv2.get_from() == Address(1, 1)
        assert mv2.get_to() == Address(2, 2)

    def test_move_drop(self):
        # Act
        mv1 = Move(csa="l*1a")
        mv2 = Move(
            piece=Piece(ColorType.White, PieceType.Lance), to_address=Address(1, 1)
        )

        # Assert
        assert mv1.is_drop() is True
        assert mv1.is_promote() is False
        assert mv1.get_piece() == Piece(ColorType.White, PieceType.Lance)
        assert mv1.get_to() == Address(1, 1)

        assert mv2.is_drop() is True
        assert mv2.is_promote() is False
        assert mv2.get_piece() == Piece(ColorType.White, PieceType.Lance)
        assert mv2.get_to() == Address(1, 1)

    def test_move_promote(self):
        # Act
        mv1 = Move(csa="1a2b+")
        mv2 = Move(from_address=Address(1, 1), to_address=Address(2, 2), promote=True)

        # Assert
        assert mv1.is_drop() is False
        assert mv1.is_promote() is True
        assert mv1.get_from() == Address(1, 1)
        assert mv1.get_to() == Address(2, 2)

        assert mv2.is_drop() is False
        assert mv2.is_promote() is True
        assert mv2.get_from() == Address(1, 1)
        assert mv2.get_to() == Address(2, 2)
