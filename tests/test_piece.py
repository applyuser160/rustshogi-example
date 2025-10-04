import pytest
from rustshogi import PieceType, Piece, ColorType


class TestPiece:
    @pytest.mark.parametrize(
        "piece_type, expected",
        [
            (1, PieceType.King),
            (2, PieceType.Gold),
            (3, PieceType.Rook),
            (4, PieceType.Bichop),
            (5, PieceType.Silver),
            (6, PieceType.Knight),
            (7, PieceType.Lance),
            (8, PieceType.Pawn),
            (9, PieceType.Dragon),
            (10, PieceType.Horse),
            (11, PieceType.ProSilver),
            (12, PieceType.ProKnight),
            (13, PieceType.ProLance),
            (14, PieceType.ProPawn),
        ],
    )
    def test_piece_type(self, piece_type: int, expected: PieceType):
        # Act
        result = PieceType(piece_type)

        # Assert
        assert result == expected
        assert result.__repr__() == f"<PieceType.{expected.name}: {expected.value}>"

    def test_piece(self):
        # Act
        result = Piece(ColorType.Black, PieceType.King)

        # Assert
        assert result.owner == ColorType.Black
        assert result.piece_type == PieceType.King
        assert (
            result.__repr__()
            == "Piece(owner=<ColorType.Black: 0>, piece_type=<PieceType.King: 1>)"
        )
        assert (
            result.__str__()
            == "Piece(owner=ColorType.Black, piece_type=PieceType.King)"
        )
