import pytest

from utility.DictConverter import DictConverter
from model.Point import Point

x_fail = pytest.mark.xfail


class TestDictConverter:
    @pytest.mark.parametrize("point_list, expected_dict",
                             [([], {}),
                              ([Point(69, 420)], {"point0": {"x": 69, "y": 420}}),
                              ([Point(32, 8), Point(-3, 15)], {"point0": {"x": 32, "y": 8},
                                                               "point1": {"x": -3, "y": 15}}),
                              ([Point(0, 0), Point(0, 1), Point(1, 0)], {"point0": {"x": 0, "y": 0},
                                                                         "point1": {"x": 0, "y": 1},
                                                                         "point2": {"x": 1, "y": 0}})])
    def test_point_list_to_dict(self, point_list, expected_dict):
        # Arrange & Act
        dictionary: dict = DictConverter.point_list_to_dict(point_list)

        # Assert
        assert dictionary == expected_dict

    @pytest.mark.parametrize("color_list, expected_dict",
                             [([], {}),
                              ([0, 0, 0], {"b": 0, "g": 0, "r": 0}),
                              ([200, 7, -43], {"b": 200, "g": 7, "r": -43}),
                              ([255, 255, 255, 255], {"b": 255, "g": 255, "r": 255})])
    def test_color_list_to_dict(self, color_list, expected_dict):
        # Arrange & Act
        dictionary: dict = DictConverter.color_list_to_dict(color_list)

        # Assert
        assert dictionary == expected_dict

    # TODO: Write test case
    def test_line_tuple_to_dict(self):
        pass
