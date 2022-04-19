from typing import Optional

from HandTracking.DictConverter import DictConverter
from HandTracking.JsonHandler import JsonHandler
from HandTracking.Point import Point


class PersistenceHandler:
    file_handler: JsonHandler = JsonHandler("./drawing.json")

    @classmethod
    def load(cls) -> Optional[dict]:
        """
        Loads the drawing.

        :return: A dictionary symbolizing the saved drawing, or None if it cannot be parsed or doesn't exist
        """
        return cls.file_handler.load()

    @classmethod
    def save(cls, drawing: dict) -> None:
        """
        Saves the drawing.

        :param drawing: The drawing to save
        """
        cls.file_handler.write(drawing)

    # TODO: also make save as image
    @classmethod
    def save_drawing(cls, lines: list[tuple[list[int], list[Point]]]) -> None:
        """
        Saves the lines making up the current drawing.

        :param lines: The lines to save as the current drawing
        """
        drawing: dict = {}

        for i, line in enumerate(lines):
            drawing[f"line{i}"] = DictConverter.line_tuple_to_dict(line)

        cls.save(drawing)

    @classmethod
    def load_drawing(cls) -> list[tuple[list[int], list[Point]]]:
        """
        Loads the drawing as a dictionary, into its proper representation.

        :return: The list of lines which make up the drawing
        """
        drawing: dict = cls.file_handler.load()
        line_list: list[tuple[list[int], list[Point]]] = []

        if not drawing:
            return [([150, 150, 150, 255], [])]

        for line in drawing:
            color_list: list = [drawing[line]["color"]["b"], drawing[line]["color"]["g"], drawing[line]["color"]["r"]]
            point_list: list = []

            for point in drawing[line]["points"]:
                point_list.append(Point.from_dict(drawing[line]["points"][point]))

            line_list.append((color_list, point_list))

        return line_list
