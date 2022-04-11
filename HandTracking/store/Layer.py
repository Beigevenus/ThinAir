import cv2
import numpy as np
from numpy import ndarray

from HandTracking.Point import Point


class Layer:
    def __init__(self, width: int, height: int, colors: dict[str, list[int]] = None):
        self.width: int = width
        self.height: int = height
        self.image: ndarray = np.full(shape=[height, width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)
        self.lines: list[list[tuple[str, Point]]] = []

        self.color_palette = {'WHITE': [150, 150, 150, 255], 'BLACK': [1, 1, 1, 1], 'RED': [0, 0, 255, 255],
                              'GREEN': [0, 255, 0, 255], 'BLUE': [255, 0, 0, 255], 'ERASER': [0, 0, 0, 0]}

        if colors:
            for name, color in colors.items():
                self.color_palette[name] = color

    def wipe(self) -> None:
        """
        Resets the values of all "pixels" in the layer, making them black.
        """
        self.image: ndarray = np.full(shape=[self.height, self.width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)

    # TODO: Make it so that the smoothing is an option, so that you can erase with ease
    def draw_line(self, previous_point: Point, point: Point, color: str, size: int) -> None:
        """
        Draws a circle at the current point, and a line between the old and current point.

        :param previous_point: The start position of the line segment
        :param point: The end position of the line segment
        :param color: The color to draw the line with
        :param size: The line size
        """
        try:
            actual_color: list[int] = self.color_palette[color]
            if color == "ERASER":
                size = 50
        except KeyError:
            actual_color: list[int] = self.color_palette["WHITE"]

        if previous_point is None:
            previous_point = point

        self.draw_circle(point, color, int(size / 2))

        # Draws line between old index finger tip position, and actual position
        cv2.line(self.image, (int(previous_point.x), int(previous_point.y)), (int(point.x), int(point.y)),
                 actual_color, size)

    def draw_circle(self, point: Point, color: str, size: int) -> None:
        """
        Draws a circle at the specified point's coordinates.

        :param point: The point to draw a circle at
        :param color: The color to draw the circle with
        :param size: The radius of the circle
        """
        try:
            actual_color: list[int] = self.color_palette[color]
        except KeyError:
            actual_color: list[int] = self.color_palette["WHITE"]

        cv2.circle(self.image, (int(point.x), int(point.y)), size, actual_color, cv2.FILLED)
