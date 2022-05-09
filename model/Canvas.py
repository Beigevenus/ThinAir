import copy
from math import sqrt

import cv2
import numpy as np
from numpy import ndarray

from model.Camera import Camera
from persistence.PersistenceHandler import PersistenceHandler
from model.Point import Point
from bezier.bezier import split_line


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
        self.new_line()
        self.update_line_array()

        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)

    def update_line_array(self) -> None:
        # TODO: Write docstring for method
        for line in self.lines:
            for point in line[1]:
                self.line_array[int(point.x)][int(point.y)].append(line)

    def wipe(self) -> None:
        """
        Resets the values of all "pixels" in the layer, making them black.
        """
        self.image: ndarray = np.full(shape=[self.height, self.width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)
        cv2.rectangle(self.image, (0, 0),
                      (self.width, self.height),
                      [80, 80, 80], 10)

    def hard_wipe(self) -> None:
        # TODO: Write docstring for method
        if len(self.lines) > 1:
            self.image: ndarray = np.full(shape=[self.height, self.width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)
            self.line_array = list(map(list, map(list, self.line_array)))
            self.lines = []
            self.new_line(force=True)

    def check_for_overlap(self, points: list[Point]) -> bool:
        # TODO: Write docstring for method
        found: bool = False
        for point in points:
            try:
                if self.line_array[int(point.x)][int(point.y)]:
                    lines = copy.deepcopy(self.lines)
                    for line in lines:
                        if point in line:
                            self.lines.remove(line)
                    found = True
            except IndexError:
                pass

        return found

    def new_line(self, force: bool = False) -> None:
        # TODO: Write docstring for method
        if force:
            try:
                if not self.lines[-1][1]:
                    self.lines.pop()
            except Exception:
                pass
            color = copy.deepcopy(self.color)
            self.lines.append((color, []))
        elif self.lines[-1][1]:
            color = copy.deepcopy(self.color)
            self.lines.append((color, []))
            if len(self.lines) > 1:
                newest_points = split_line(self.lines[-2][1])

                # TODO: Confirm that the following is fixed: problem with index out of range when drawing on the edge
                self.lines[-2] = (self.lines[-2][0], [Point(x, y) for x, y in newest_points])
                for point in self.lines[-2][1]:
                    try:
                        self.line_array[int(point.x)][int(point.y)].append(self.lines[-2])
                    except IndexError:
                        pass

    def remove_excess_line(self) -> None:
        # TODO: Write docstring for method
        if self.lines[-1][1]:
            color = copy.deepcopy(self.color)
            self.lines.append((color, []))

    def add_point(self, point: Point) -> None:
        # TODO: Write docstring for method
        if point:
            self.lines[-1][1].append(point)

    def draw(self) -> None:
        # TODO: Write docstring for method
        size: int = 2
        for color, line in self.lines:
            if line:
                previous_point = line[0]
                for point in line:
                    # Draws line between old index finger tip position, and actual position
                    self.draw_line(previous_point, point, color, size)
                    previous_point = point

    def erase(self, point: Point, size: int) -> None:
        # TODO: Write docstring for method
        start_point_x_y = (point.x-size, point.y-size)
        for x in range(size*2):
            if self.width > (start_point_x_y[0] + x) >= 0:
                for y in range(size*2):
                    if self.height > (start_point_x_y[1] + y) >= 0:
                        if self.line_array[int(start_point_x_y[0] + x)][int(start_point_x_y[1] + y)]:
                            for line in self.line_array[int(start_point_x_y[0] + x)][int(start_point_x_y[1] + y)]:
                                self.delete_line(line)

    def delete_line(self, line) -> None:
        # TODO: Write docstring for method
        for point in line[1]:
            self.line_array[int(point.x)][int(point.y)].remove(line)
        try:
            self.lines.remove(line)
        except ValueError:
            pass

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

    def draw_img(self, img, size: int, pos: Point) -> None:
        # TODO: Write docstring for method
        size = int(size*sqrt(2))
        s_img = img
        s_img = cv2.resize(s_img, (size, size))

        y_offset = int(pos.y - size/2)
        x_offset = int(pos.x - size/2)
        y1, y2 = y_offset, y_offset + s_img.shape[0]
        x1, x2 = x_offset, x_offset + s_img.shape[1]

        alpha_s = s_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            self.image[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                           alpha_l * self.image[y1:y2, x1:x2, c])

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
