from rustshogi import Hand, ColorType, Piece, PieceType


class TestHand:
    def test_hand(self):
        # Act
        hand = Hand()

        # Assert
        assert hand.pieces == [
            Piece(ColorType.Black, PieceType.King),
            Piece(ColorType.Black, PieceType.Gold),
            Piece(ColorType.Black, PieceType.Rook),
            Piece(ColorType.Black, PieceType.Bishop),
            Piece(ColorType.Black, PieceType.Silver),
            Piece(ColorType.Black, PieceType.Knight),
            Piece(ColorType.Black, PieceType.Lance),
            Piece(ColorType.Black, PieceType.Pawn),
            Piece(ColorType.White, PieceType.King),
            Piece(ColorType.White, PieceType.Gold),
            Piece(ColorType.White, PieceType.Rook),
            Piece(ColorType.White, PieceType.Bishop),
            Piece(ColorType.White, PieceType.Silver),
            Piece(ColorType.White, PieceType.Knight),
            Piece(ColorType.White, PieceType.Lance),
            Piece(ColorType.White, PieceType.Pawn),
        ]
        assert hand.counts == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def test_hand_add_piece(self):
        # Act
        hand = Hand()
        hand.add_piece(ColorType.Black, PieceType.Gold)
        hand.add_pieces(ColorType.White, PieceType.Gold, 2)

        # Assert
        assert hand.pieces == [
            Piece(ColorType.Black, PieceType.King),
            Piece(ColorType.Black, PieceType.Gold),
            Piece(ColorType.Black, PieceType.Rook),
            Piece(ColorType.Black, PieceType.Bishop),
            Piece(ColorType.Black, PieceType.Silver),
            Piece(ColorType.Black, PieceType.Knight),
            Piece(ColorType.Black, PieceType.Lance),
            Piece(ColorType.Black, PieceType.Pawn),
            Piece(ColorType.White, PieceType.King),
            Piece(ColorType.White, PieceType.Gold),
            Piece(ColorType.White, PieceType.Rook),
            Piece(ColorType.White, PieceType.Bishop),
            Piece(ColorType.White, PieceType.Silver),
            Piece(ColorType.White, PieceType.Knight),
            Piece(ColorType.White, PieceType.Lance),
            Piece(ColorType.White, PieceType.Pawn),
        ]
        assert hand.counts == [0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]

    def test_hand_decrease_piece(self):
        # Act
        hand = Hand()
        hand.add_pieces(ColorType.Black, PieceType.Gold, 2)
        hand.decrease_piece(ColorType.Black, PieceType.Gold)

        # Assert
        assert hand.pieces == [
            Piece(ColorType.Black, PieceType.King),
            Piece(ColorType.Black, PieceType.Gold),
            Piece(ColorType.Black, PieceType.Rook),
            Piece(ColorType.Black, PieceType.Bishop),
            Piece(ColorType.Black, PieceType.Silver),
            Piece(ColorType.Black, PieceType.Knight),
            Piece(ColorType.Black, PieceType.Lance),
            Piece(ColorType.Black, PieceType.Pawn),
            Piece(ColorType.White, PieceType.King),
            Piece(ColorType.White, PieceType.Gold),
            Piece(ColorType.White, PieceType.Rook),
            Piece(ColorType.White, PieceType.Bishop),
            Piece(ColorType.White, PieceType.Silver),
            Piece(ColorType.White, PieceType.Knight),
            Piece(ColorType.White, PieceType.Lance),
            Piece(ColorType.White, PieceType.Pawn),
        ]
        assert hand.counts == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def test_hand_get_player_pieces(self):
        # Act
        hand = Hand()
        hand.add_pieces(ColorType.Black, PieceType.Gold, 2)
        hand.add_pieces(ColorType.Black, PieceType.Pawn, 9)
        hand.add_pieces(ColorType.White, PieceType.Gold, 3)

        # Assert
        assert hand.get_player_pieces(ColorType.Black) == [
            Piece(ColorType.Black, PieceType.Gold),
            Piece(ColorType.Black, PieceType.Pawn),
        ]
        assert hand.get_player_pieces(ColorType.White) == [
            Piece(ColorType.White, PieceType.Gold)
        ]
