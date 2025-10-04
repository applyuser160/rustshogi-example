import pytest
from rustshogi import ColorType


class TestColor:
    @pytest.mark.parametrize(
        "color_type, expected",
        [
            (0, ColorType.Black),
            (1, ColorType.White),
            (2, ColorType.ColorNumber),
        ],
    )
    def test_color_init(self, color_type: int, expected: ColorType):
        # Act
        result = ColorType(color_type)

        # Assert
        assert result == expected
        assert result.__repr__() == f"<ColorType.{expected.name}: {expected.value}>"
