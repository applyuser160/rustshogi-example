from rustshogi import Address, Board, ColorType, Piece, PieceType


class TestBoard:
    def test_board_new(self):
        # Act
        board = Board("lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL -")

        # Assert
        assert (
            board.__repr__()
            == "Board(sfen=lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL)"
        )
        assert (
            board.__str__()
            == "Board(sfen=lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL)"
        )
        assert board.get_piece(Address(1, 1)) == Piece(ColorType.Black, PieceType.Lance)
        assert board.get_piece(Address(2, 1)) == Piece(
            ColorType.Black, PieceType.Knight
        )
        assert board.get_piece(Address(3, 1)) == Piece(
            ColorType.Black, PieceType.Silver
        )
        assert board.get_piece(Address(4, 1)) == Piece(ColorType.Black, PieceType.Gold)
        assert board.get_piece(Address(5, 1)) == Piece(ColorType.Black, PieceType.King)
        assert board.get_piece(Address(6, 1)) == Piece(ColorType.Black, PieceType.Gold)
        assert board.get_piece(Address(7, 1)) == Piece(
            ColorType.Black, PieceType.Silver
        )
        assert board.get_piece(Address(8, 1)) == Piece(
            ColorType.Black, PieceType.Knight
        )
        assert board.get_piece(Address(9, 1)) == Piece(ColorType.Black, PieceType.Lance)
        assert board.get_piece(Address(8, 2)) == Piece(ColorType.Black, PieceType.Rook)
        assert board.get_piece(Address(2, 2)) == Piece(
            ColorType.Black, PieceType.Bichop
        )
        assert board.get_piece(Address(1, 3)) == Piece(ColorType.Black, PieceType.Pawn)
        assert board.get_piece(Address(2, 3)) == Piece(ColorType.Black, PieceType.Pawn)
        assert board.get_piece(Address(3, 3)) == Piece(ColorType.Black, PieceType.Pawn)
        assert board.get_piece(Address(4, 3)) == Piece(ColorType.Black, PieceType.Pawn)
        assert board.get_piece(Address(5, 3)) == Piece(ColorType.Black, PieceType.Pawn)
        assert board.get_piece(Address(6, 3)) == Piece(ColorType.Black, PieceType.Pawn)
        assert board.get_piece(Address(7, 3)) == Piece(ColorType.Black, PieceType.Pawn)
        assert board.get_piece(Address(8, 3)) == Piece(ColorType.Black, PieceType.Pawn)
        assert board.get_piece(Address(9, 3)) == Piece(ColorType.Black, PieceType.Pawn)

        assert board.get_piece(Address(1, 9)) == Piece(ColorType.White, PieceType.Lance)
        assert board.get_piece(Address(2, 9)) == Piece(
            ColorType.White, PieceType.Knight
        )
        assert board.get_piece(Address(3, 9)) == Piece(
            ColorType.White, PieceType.Silver
        )
        assert board.get_piece(Address(4, 9)) == Piece(ColorType.White, PieceType.Gold)
        assert board.get_piece(Address(5, 9)) == Piece(ColorType.White, PieceType.King)
        assert board.get_piece(Address(6, 9)) == Piece(ColorType.White, PieceType.Gold)
        assert board.get_piece(Address(7, 9)) == Piece(
            ColorType.White, PieceType.Silver
        )
        assert board.get_piece(Address(8, 9)) == Piece(
            ColorType.White, PieceType.Knight
        )
        assert board.get_piece(Address(9, 9)) == Piece(ColorType.White, PieceType.Lance)
        assert board.get_piece(Address(8, 8)) == Piece(
            ColorType.White, PieceType.Bichop
        )
        assert board.get_piece(Address(2, 8)) == Piece(ColorType.White, PieceType.Rook)
        assert board.get_piece(Address(1, 7)) == Piece(ColorType.White, PieceType.Pawn)
        assert board.get_piece(Address(2, 7)) == Piece(ColorType.White, PieceType.Pawn)
        assert board.get_piece(Address(3, 7)) == Piece(ColorType.White, PieceType.Pawn)
        assert board.get_piece(Address(4, 7)) == Piece(ColorType.White, PieceType.Pawn)
        assert board.get_piece(Address(5, 7)) == Piece(ColorType.White, PieceType.Pawn)
        assert board.get_piece(Address(6, 7)) == Piece(ColorType.White, PieceType.Pawn)
        assert board.get_piece(Address(7, 7)) == Piece(ColorType.White, PieceType.Pawn)
        assert board.get_piece(Address(8, 7)) == Piece(ColorType.White, PieceType.Pawn)
        assert board.get_piece(Address(9, 7)) == Piece(ColorType.White, PieceType.Pawn)
