from menu_wheel.Button import Button
import pytest

from model.Point import Point

x_fail = pytest.mark.xfail


class TestButton:
    @pytest.mark.parametrize("point, location, expected", [(Point(0, 0), Point(30, 30), False),
                                                           (Point(30, 30), Point(0, 0), False),
                                                           (Point(-22, -89), Point(42, 3), False),
                                                           (Point(32, 48), Point(30, 40), True),
                                                           (Point(0, 0), Point(0, 0), True)])
    def test_is_point_in_circle(self, point, location, expected):
        # Arrange
        button: Button = Button(None)
        button.set_location(location)

        # Act
        actual = button.is_point_in_circle(point)

        # Assert
        assert actual == expected
