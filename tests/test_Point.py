from model.Point import Point
import pytest

x_fail = pytest.mark.xfail


class TestPoint:
    @pytest.mark.parametrize("x1, y1, x2, y2, expected_distance", [(10, 23, 13, 7, 265),
                                                                   (10, 23, 2, -5, 848),
                                                                   (10, 23, -32, 0, 2293),
                                                                   (13, 7, 2, -5, 265),
                                                                   (13, 7, -32, 0, 2074),
                                                                   (2, -5, -32, 0, 1181)])
    def test_distance_to(self, x1, y1, x2, y2, expected_distance):
        # Arrange
        point1: Point = Point(x1, y1)
        point2: Point = Point(x2, y2)

        # Act
        distance: float = point1.distance_to(point2)

        # Assert
        assert round(distance, 4) == expected_distance

    @pytest.mark.parametrize("point1, point2, precision, expected_point",
                             [(Point(6, 32), Point(1, 22), -1, Point(3.5, 27)),
                              (Point(-2, 9), Point(22, 19), 0, Point(10, 14)),
                              (Point(0, 0), Point(0, 0), 1, Point(0, 0)),
                              (Point(0, 0), Point(10, 42), 1, Point(2.5, 10.5)),
                              (Point(15, -2), Point(82, 75), 2, Point(23.375, 7.625)),
                              (Point(-62, -17), Point(-5, -8), 3, Point(-58.4375, -16.4375))])
    def test_next_point_to(self, point1: Point, point2: Point, precision: int, expected_point: Point):
        # Arrange & Act
        actual = point1.next_point_to(point2, precision)

        # Assert
        assert actual == expected_point

    @pytest.mark.parametrize("point, expected_list", [(Point(0, 0), [0, 0]),
                                                      (Point(-73, -8), [-73, -8]),
                                                      (Point(52, 842), [52, 842])])
    def test_as_list(self, point, expected_list):
        # Arrange & Act
        actual = point.as_list()

        # Assert
        assert actual == expected_list
