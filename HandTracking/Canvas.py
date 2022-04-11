import copy

import cv2
import numpy as np
from numpy import ndarray

from HandTracking.PersistenceHandler import PersistenceHandler
from HandTracking.Point import Point


class Canvas:
    def __init__(self, name, width: int = 1920, height: int = 1080) -> None:
        self.width: int = width
        self.height: int = height
        self.name: str = name
        self.image: ndarray = np.full(shape=[height, width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)

        self.color: list[int] = [150, 150, 150, 255]

        self.line_array: list[list[list[tuple[list[int], list[Point]]]]] = [[[] for _ in range(self.height)]
                                                                            for _ in range(self.width)]
        self.lines: list[tuple[list[int], list[Point]]] = PersistenceHandler.load_drawing()
        self.update_line_array()

        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)

    def init_line_array(self):
        # TODO: Write docstring for method
        self.line_array = list(map(list, map(list, self.line_array)))

    def update_line_array(self):
        # TODO: Write docstring for method
        for line in self.lines:
            for point in line[1]:
                self.line_array[int(point.x)][int(point.y)].append(line)

    def wipe(self) -> None:
        """
        Resets the values of all "pixels" in the layer, making them black.
        """
        self.image: ndarray = np.full(shape=[self.height, self.width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)

    def hard_wipe(self):
        # TODO: Write docstring for method
        if len(self.lines) > 1:
            self.image: ndarray = np.full(shape=[self.height, self.width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)
            self.init_line_array()
            self.lines = []
            self.new_line(force=True)

    def check_for_overlap(self, points):
        # TODO: Write docstring for method
        found = False
        for point in points:
            if self.line_array[point.x][point.y]:
                lines = copy.deepcopy(self.lines)
                for line in lines:
                    if point in line:
                        self.lines.remove(line)
                found = True

        return found

    def new_line(self, force=False):
        # TODO: Write docstring for method
        if force:
            color = copy.deepcopy(self.color)
            self.lines.append((color, []))
        elif self.lines[-1][1]:
            color = copy.deepcopy(self.color)
            self.lines.append((color, []))

    def remove_excess_line(self):
        # TODO: Write docstring for method
        if self.lines[-1][1]:
            color = copy.deepcopy(self.color)
            self.lines.append((color, []))

    def add_point(self, point):
        # TODO: Write docstring for method
        self.lines[-1][1].append(point)
        self.line_array[int(point.x)][int(point.y)].append(self.lines[-1])

    def draw(self):
        # TODO: Write docstring for method
        size = 3
        for color, line in self.lines:
            if line:
                previous_point = line[0]
                for point in line:
                    # Draws line between old index finger tip position, and actual position
                    self.draw_line(previous_point, point, color, size)
                    previous_point = point

    def erase(self, point, size):
        # TODO: Write docstring for method
        start_point_x_y = (point.x-size, point.y-size)
        for x in range(size*2):
            if self.width > (start_point_x_y[0] + x) >= 0:
                for y in range(size*2):
                    if self.height > (start_point_x_y[1] + y) >= 0:
                        if self.line_array[start_point_x_y[0] + x][start_point_x_y[1] + y]:
                            for line in self.line_array[start_point_x_y[0] + x][start_point_x_y[1] + y]:
                                self.delete_line(line)

    def delete_line(self, line):
        # TODO: Write docstring for method
        for point in line[1]:
            self.line_array[int(point.x)][int(point.y)].remove(line)
        self.lines.remove(line)

    def draw_line(self, previous_point: Point, point: Point, color, size: int) -> None:
        """
        Draws a circle at the current point, and a line between the old and current point.

        :param previous_point: The start position of the line segment
        :param point: The end position of the line segment
        :param color: The color to draw the line with
        :param size: The line size
        """
        if type(color) is str:
            color = [255, 225, 150, 255]

        self.draw_circle(point, color, int(size / 2))

        # Draws line between old index finger tip position, and actual position
        cv2.line(self.image, (int(previous_point.x), int(previous_point.y)), (int(point.x), int(point.y)),
                 color, size)

    def draw_circle(self, point: Point, color, size: int) -> None:
        """
        Draws a circle at the specified point's coordinates.

        :param point: The point to draw a circle at
        :param color: The color to draw the circle with
        :param size: The radius of the circle
        """
        if type(color) is str:
            color = [255, 225, 150, 255]

        cv2.circle(self.image, (int(point.x), int(point.y)), size, color, cv2.FILLED)

    def draw_mask_points(self, points: list[Point]) -> None:
        """
        Draws multiple circles on the MASK layer of the canvas corresponding to the given points' coordinates.

        :param points: The list of Points to draw circles at
        """

        for point in points:
            self.draw_circle(point, [1, 1, 1, 1], int(75/2))

    def show(self) -> None:
        """
        Updates the shown canvas in its window.
        """
        cv2.imshow(self.name, cv2.flip(self.image, 1))

    def fullscreen(self) -> None:
        """
        Switches the canvas window to fullscreen mode.
        """
        cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def move_window(self, offset_x: int, offset_y: int) -> None:
        """
        Moves the canvas window horizontally by the given offset.

        :param offset_x: The number of pixels to move the window in the horizontal plane
        :param offset_y: The number of pixels to move the window in the vertical plane
        """
        cv2.moveWindow(self.name, offset_x, offset_y)
