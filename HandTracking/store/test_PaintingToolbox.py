import pytest

from HandTracking.PaintingToolbox import PaintingToolbox

x_fail = pytest.mark.xfail


class TestPaintingToolbox:
    @pytest.mark.parametrize("new_color, expected_color", [("WHITE", [150, 150, 150, 255]),
                                                           ("BLACK", [1, 1, 1, 1]),
                                                           ("RED", [0, 0, 255, 255]),
                                                           ("GREEN", [0, 255, 0, 255]),
                                                           ("BLUE", [255, 0, 0, 255]),
                                                           ("RAINBOW", [150, 150, 150, 255])])
    def test_change_color(self, new_color, expected_color):
        # Arrange
        toolbox: PaintingToolbox = PaintingToolbox()

        # Act
        toolbox.change_color(new_color)

        # Assert
        assert toolbox.current_color == expected_color

    @pytest.mark.parametrize("new_color", [([55, 82, 0, 3]), ([98, 142, 247, 228]),
                                           ([7, 1, 3, 0]), [255, 255, 255, 255]])
    def test_change_color_rgba(self, new_color):
        # Arrange
        toolbox: PaintingToolbox = PaintingToolbox()

        # Act
        toolbox.change_color_rgba(new_color)

        # Assert
        assert toolbox.current_color == new_color

    @pytest.mark.parametrize("new_line_size, expected_circle_size", [(10, 5), (0, 0), (-15, -7),
                                                                     (17, 8), (6, 3)])
    def test_change_line_size(self, new_line_size, expected_circle_size):
        # Arrange
        toolbox: PaintingToolbox = PaintingToolbox()

        # Act
        toolbox.change_line_size(new_line_size)

        # Assert
        assert toolbox.line_size == new_line_size
        assert toolbox.circle_size == expected_circle_size
