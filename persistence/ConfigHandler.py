from typing import Optional, List

from utility.DictConverter import DictConverter
from persistence.JsonHandler import JsonHandler
from model.Point import Point


class ConfigHandler:
    file_handler: JsonHandler = JsonHandler("./config.json")
    empty_config: dict = {
        "startup": {},
        "cal_points": {},
        "bou_points": {}
    }

    @classmethod
    def load(cls) -> Optional[dict]:
        """
        Loads the config into a dictionary.

        :return: A dictionary symbolizing the config file, or None if it cannot be parsed or doesn't exist
        """
        return cls.file_handler.load()

    @classmethod
    def save(cls, settings: dict) -> None:
        """
        Saves the given setting configuration.

        :param settings: The settings to save
        """
        cls.file_handler.write(settings)

    @classmethod
    def load_calibration_points(cls) -> Optional[List[Point]]:
        """
        Converts calibration points from the config file to a list of Point objects.

        :return: A list of Point objects saved in the config file, or None if it doesn't exist
        """
        try:
            config: Optional[dict] = cls.load()
            point_list: List[Point] = [Point.from_dict(config["cal_points"]["point0"]),
                                       Point.from_dict(config["cal_points"]["point1"]),
                                       Point.from_dict(config["cal_points"]["point2"]),
                                       Point.from_dict(config["cal_points"]["point3"])]
            return point_list
        except (KeyError, TypeError):
            return None

    @classmethod
    def load_boundary_points(cls) -> Optional[List[Point]]:
        """
        Converts boundary points from the config file to a list of Point objects.

        :return: A list of Point objects saved in the config file, or None if it doesn't exist
        """
        try:
            config: Optional[dict] = cls.load()
            point_list: List[Point] = [Point.from_dict(config["bou_points"]["point0"]),
                                       Point.from_dict(config["bou_points"]["point1"])]
            return point_list
        except (KeyError, TypeError):
            return None

    @classmethod
    def load_startup_settings(cls) -> Optional[dict]:
        """
        Reads the config and returns the part relevant for startup settings.

        :return: A dictionary containing the startup settings from the config file, None if it doesn't exist
        """
        try:
            return cls.load()["startup"]
        except TypeError:
            return None

    @classmethod
    def save_startup_settings(cls, settings: dict) -> None:
        """
        Saves the new startup settings.

        :param settings: The dictionary of settings to save
        """
        config = cls.load()

        if not config:
            config = cls.empty_config

        config["startup"] = settings
        cls.save(config)

    @classmethod
    def save_calibration_points(cls, cal_points: List[Point]) -> None:
        """
        Saves the new calibration points.

        :param cal_points: A list of Point objects to save
        """
        config = cls.load()

        if not config:
            config = cls.empty_config

        cal_points = DictConverter.point_list_to_dict(cal_points)
        config["cal_points"] = cal_points
        cls.save(config)

    @classmethod
    def save_boundary_points(cls, bou_points: List[Point]) -> None:
        """
        Saves the new boundary points.

        :param bou_points: A list of Point objects to save
        """
        config = cls.load()

        if not config:
            config = cls.empty_config

        bou_points = DictConverter.point_list_to_dict(bou_points)
        config["bou_points"] = bou_points
        cls.save(config)
