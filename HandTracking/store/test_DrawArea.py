from HandTracking.store.DrawArea import DrawArea
from HandTracking.Point import Point
import pytest

x_fail = pytest.mark.xfail


class TestDrawArea:
    @pytest.mark.parametrize('point1, point2, expected_line', [(Point(10, 11), Point(50, 0), [-0.275, 13.750]),
                                                               (Point(20, 120), Point(80, 85), [-0.583, 131.667]),
                                                               (Point(0, 0), Point(0, 0), [None, 0]),
                                                               (Point(-2, -57), Point(32, -15), [1.235, -54.529])])
    def test_get_line_attributes(self, point1: Point, point2: Point, expected_line: list[float]):
        # Arrange & Act
        attributes = DrawArea.get_line_attributes(point1, point2)

        # Assert
        if attributes[0]:
            assert round(attributes[0], 3) == expected_line[0]
        assert round(attributes[1], 3) == expected_line[1]

    # TODO: Reconsider how to test this
    def test_is_position_in_calibration_area_for_vertical_borders(self):
        point1 = Point(0, 0)
        point2 = Point(30, 0)
        point3 = Point(0, 30)
        point4 = Point(30, 30)
        test_pont = Point(20, 20)

        draw_area = DrawArea([point1, point2, point3, point4])

        assert draw_area.left_border[0] is None
        assert draw_area.right_border[0] is None
        assert draw_area.is_position_in_calibration_area(test_pont) is True

    # TODO: Reconsider how to test this
    @pytest.mark.parametrize('point', [(Point(20, 10)),
                                       (Point(18, 9)),
                                       (Point(60, 70)),
                                       (Point(20, 54)),
                                       (Point(40, 35)),
                                       (Point(14, 17))
                                       ])
    def test_is_position_in_calibration_area_when_inside(self, point):
        point1 = Point(10, 11)
        point2 = Point(50, 0)
        point3 = Point(20, 120)
        point4 = Point(70, 85)

        draw_area = DrawArea([point1, point2, point3, point4])

        assert draw_area.is_position_in_calibration_area(point) is True

    # TODO: Reconsider how to test this
    @pytest.mark.parametrize('point', [(Point(17, 8)),
                                       (Point(-10, 5)),
                                       (Point(90, 80)),
                                       (Point(110, 20)),
                                       (Point(5, 5))
                                       ])
    def test_is_position_in_calibration_area_when_outside(self, point):
        point1 = Point(10, 11)
        point2 = Point(50, 0)
        point3 = Point(70, 85)
        point4 = Point(20, 120)

        draw_area = DrawArea([point1, point2, point3, point4])

        assert draw_area.is_position_in_calibration_area(point) is False
