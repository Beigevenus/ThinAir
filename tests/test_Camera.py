from typing import Optional

from model.Camera import Camera
from model.Point import Point
import pytest

x_fail = pytest.mark.xfail


class TestCamera:
    # TODO: Fix test case. The expected output is different from when the test case was originally implemented
    @pytest.mark.parametrize('point1, point2, point3, point4, expected_order',
                             [(Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(50, 0), Point(20, 120), Point(70, 85),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(70, 85), Point(50, 0), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(70, 85), Point(20, 120), Point(50, 0),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(20, 120), Point(10, 11), Point(50, 0), Point(70, 85),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)]),
                              (Point(10, 11), Point(70, 85), Point(50, 0), Point(20, 120),
                               [Point(10, 11), Point(50, 0), Point(70, 85), Point(20, 120)])
                              ])
    def test_sort_calibration_points(self, point1: Point, point2: Point, point3: Point, point4: Point,
                                     expected_order: list[Point]):
        # Arrange
        calibration_points: list[Point] = [point1, point2, point3, point4]
        camera: Camera = Camera.__new__(Camera)
        camera.calibration_points = calibration_points

        # Act
        camera.sorted_calibration_points = camera.sort_calibration_points()

        # Assert
        assert camera.sorted_calibration_points[0] == expected_order[0]
        assert camera.sorted_calibration_points[1] == expected_order[1]
        assert camera.sorted_calibration_points[2] == expected_order[2]
        assert camera.sorted_calibration_points[3] == expected_order[3]

    @pytest.mark.parametrize('point1, expected',
                             [(Point(0.02, 0.03), None),
                              (Point(0.08, 0.10), Point(0.052631579, 0.078947368)),
                              (Point(0.0, 0.0), None),
                              (Point(0.30, 0.30), Point(0.342105263, 0.342105263)),
                              (Point(1.00, 1.00), None),
                              (Point(0.80, 0.80), Point(1.00, 1.00)),
                              (Point(0.04, 0.04), Point(0.00, 0.00)),
                              (Point(0.80, 0.04), Point(1.00, 0.00)),
                              (Point(0.40, 0.40), Point(0.473684211, 0.473684211))
                              ])
    def test_sort_calibration_points(self, point1: Point, expected: Optional[Point]):
        # Arrange
        calibration_points: list[Point] = [Point(0, 0), Point(500, 0), Point(500, 500), Point(0, 500)]
        camera: Camera = Camera.__new__(Camera)
        camera.calibration_points = calibration_points
        camera.width = 500
        camera.height = 500
        camera.boundary_points = []
        camera.boundaries = {"x_min": None, "x_max": None, "y_min": None, "y_max": None}
        # TODO: The following statement creates a config.json file, fix this
        camera.update_calibration_point(Point(20, 20), 0, 0)
        camera.update_calibration_point(Point(400, 400), 0, 0)

        # Act
        boundary_point = camera.normalise_in_boundary(point1)

        # Assert
        if expected:
            assert round(boundary_point.x, 9) == expected.x
            assert round(boundary_point.y, 9) == expected.y
        else:
            assert boundary_point == expected

    # TODO: Write test case
    def test_transform_point(self):
        pass

    @pytest.mark.parametrize("cal_points, expected", [([], False),
                                                      ([Point(0, 0)], False),
                                                      ([Point(0, 0), Point(0, 0)], False),
                                                      ([Point(0, 0), Point(0, 0), Point(0, 0)], False),
                                                      ([Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)], True)])
    def test_calibration_is_done(self, cal_points, expected):
        # Arrange
        camera: Camera = Camera.__new__(Camera)
        camera.calibration_points = cal_points

        # Act
        actual = camera.calibration_is_done()

        # Assert
        assert actual == expected
