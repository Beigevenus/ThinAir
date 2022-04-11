from HandTracking.ConfigHandler import ConfigHandler
import pytest

from HandTracking.Point import Point

x_fail = pytest.mark.xfail


class TestConfig:
    pass
    # TODO: Method was moved to DictConverter, reconsider test cases for ConfigHandler
    # @pytest.mark.parametrize("point_list, expected_dict",
    #                          [([], {}),
    #                           ([Point(69, 420)], {"point0": {"x": 69, "y": 420}}),
    #                           ([Point(32, 8), Point(-3, 15)], {"point0": {"x": 32, "y": 8},
    #                                                            "point1": {"x": -3, "y": 15}}),
    #                           ([Point(0, 0), Point(0, 1), Point(1, 0)], {"point0": {"x": 0, "y": 0},
    #                                                                      "point1": {"x": 0, "y": 1},
    #                                                                      "point2": {"x": 1, "y": 0}})])
    # def test_point_list_to_dict(self, point_list, expected_dict):
    #     # Act
    #     dictionary: dict = ConfigHandler.point_list_to_dict(point_list)
    #
    #     # Assert
    #     assert dictionary == expected_dict
