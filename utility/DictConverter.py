from model.Point import Point


class DictConverter:
    @classmethod
    def point_list_to_dict(cls, point_list: list[Point]) -> dict:
        """
        Converts a list of Point objects to a dictionary representation.

        :param point_list: The list of Point objects to convert
        :return: A dictionary containing the given points
        """
        dictionary = {}
        for i, point in enumerate(point_list):
            dictionary[f"point{i}"] = point.__dict__

        return dictionary

    @classmethod
    def color_list_to_dict(cls, color_list: list[int]) -> dict:
        if color_list:
            return {"b": color_list[0], "g": color_list[1], "r": color_list[2]}
        else:
            return {}

    @classmethod
    def line_tuple_to_dict(cls, line_tuple: tuple) -> dict:
        return {"color": cls.color_list_to_dict(line_tuple[0]),
                "points": cls.point_list_to_dict(line_tuple[1])}
