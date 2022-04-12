import copy
from hashlib import new

import cv2
import numpy as np
from numpy import ndarray

from HandTracking.Camera import Camera
from HandTracking.PersistenceHandler import PersistenceHandler
from HandTracking.Point import Point
import bezier as bz


class Canvas:
    def __init__(self, name, width: int = 1920, height: int = 1080) -> None:
        self.width: int = width
        self.height: int = height
        self.name: str = name
        self.image: ndarray = np.full(shape=[height, width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)

        self.color: list[int] = [150, 150, 150, 255]

        self.line_array: list[list[list[tuple[list[int], list[Point]]]]] = [[[] for y in range(self.height)] for x in range(self.width)]
        self.lines: list[tuple[list[int], list[Point]]] = PersistenceHandler.load_drawing()
        self.new_line()
        self.update_line_array()

        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)

    def update_line_array(self):
        for line in self.lines:
            for point in line[1]:
                self.line_array[int(point.x)][int(point.y)].append(line)

    def wipe(self) -> None:
        """
        Resets the values of all "pixels" in the layer, making them black.
        """
        self.image: ndarray = np.full(shape=[self.height, self.width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)

    def hard_wipe(self):
        if len(self.lines) > 1:
            self.image: ndarray = np.full(shape=[self.height, self.width, 4], fill_value=[0, 0, 0, 0], dtype=np.uint8)
            self.line_array = list(map(list, map(list, self.line_array)))
            self.lines = []
            self.new_line(force=True)

    def check_for_overlap(self, points):
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
        if force:
            color = copy.deepcopy(self.color)
            self.lines.append((color, []))
        elif self.lines[-1][1]:
            color = copy.deepcopy(self.color)
            self.lines.append((color, []))
            if len(self.lines) > 1:
                points = [[point.x, point.y] for point in self.lines[-2][1]]
                new_points = bz.bezier_curve(points)
                print(new_points)
                self.lines[-2] = (self.lines[-2][0], [Point(x, y) for x, y in new_points])

    def remove_excess_line(self):
        if self.lines[-1][1]:
            color = copy.deepcopy(self.color)
            self.lines.append((color, []))

    def add_point(self, point):
        self.lines[-1][1].append(point)
        self.line_array[int(point.x)][int(point.y)].append(self.lines[-1])

    def draw(self):
        size = 3
        for color, line in self.lines:
            if line:
                previous_point = line[0]
                for point in line:
                    # Draws line between old index finger tip position, and actual position
                    self.draw_line(previous_point, point, color, size)
                    previous_point = point

    def erase(self, point, size):
        start_point_x_y = (point.x-size, point.y-size)
        for x in range(size*2):
            if self.width > (start_point_x_y[0] + x) >= 0:
                for y in range(size*2):
                    if self.height > (start_point_x_y[1] + y) >= 0:
                        if self.line_array[start_point_x_y[0] + x][start_point_x_y[1] + y]:
                            for line in self.line_array[start_point_x_y[0] + x][start_point_x_y[1] + y]:
                                self.delete_line(line)

    def delete_line(self, line):
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

    # def create_layer(self, name: str, colors: dict[str, list[int]] = None, position: int = -1) -> None:
    #     """
    #     Creates a new Layer object and adds it to the canvas' list of layers, at the specified position.
    #
    #     :param name: The name of the layer
    #     :param colors: The additional colors to add to the layer's color palette
    #     :param position: The position of the layer in the order of layers
    #     """
    #     if colors:
    #         actual_colors = colors
    #     else:
    #         actual_colors = {}
    #
    #     try:
    #         if position == -1:
    #             self.layers.append((name, Layer(self.width, self.height, actual_colors)))
    #         else:
    #             self.layers.insert(position, (name, Layer(self.width, self.height, actual_colors)))
    #     except IndexError:
    #         self.layers.append((name, Layer(self.width, self.height, actual_colors)))

    # def delete_layer(self, name: str) -> None:
    #     """
    #     Removes the specified layer from the list of layers.
    #
    #     :param name: The name of the layer to remove
    #     """
    #     layer: tuple[str, Layer] = self.__find_layer(name)
    #
    #     if layer:
    #         self.layers.remove(layer)
    #
    # def get_layer(self, name: str) -> Optional[Layer]:
    #     """
    #     Returns a reference to a Layer object given its name if it exists in the list of layers.
    #
    #     :param name: The name of the layer to get the reference of
    #     :return: A reference to the layer matching the specified name, or None if it doesn't exist
    #     """
    #     layer: tuple[str, Layer] = self.__find_layer(name)
    #
    #     if layer:
    #         return self.__find_layer(name)[1]
    #     else:
    #         return None
    #
    # def __find_layer(self, name: str) -> Optional[tuple[str, Layer]]:
    #     """
    #     Returns a tuple containing a layer's name and object reference given its name.
    #
    #     :param name: The name of the layer to find
    #     :return: A tuple containing the name and object reference of the layer, or None if it doesn't exist
    #     """
    #     for layer_name, layer in self.layers:
    #         if name == layer_name:
    #             return layer_name, layer
    #     return None
    #
    # def combine_layers(self) -> ndarray:
    #     """
    #     Merges all layers in the list of layers together, to create *one* layer containing the images of all combined
    #     layers.
    #
    #     :return: An ndarray representing the image of the merged layers
    #     """
    #     combined_image: ndarray = np.zeros(shape=[self.height, self.width, 4], dtype=np.uint8)
    #
    #     for name, layer in self.layers[::-1]:
    #         src_a: ndarray = layer.image[..., 3] > 0
    #
    #         combined_image[src_a] = layer.image[src_a]
    #
    #     return combined_image

    # def resize(self, width: int, height: int) -> None:
    #     """
    #     Changes the width and height of the canvas resolution and its layers to the given lengths.
    #
    #     :param width: The desired width
    #     :param height: The desired height
    #     """
    #     if width <= 0 or height <= 0:
    #         raise ValueError("Width and height of a resized canvas must be larger than 0.")
    #
    #     # for name, layer in self.layers:
    #     #     layer.width = width
    #     #     layer.height = height
    #     self.image = cv2.resize(self.image, (width, height), interpolation=cv2.INTER_AREA)
    #
    #     self.width = width
    #     self.height = height

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
        # self.__check_for_resize()

    # def __check_for_resize(self) -> None:
    #     """
    #     Checks if the dimensions of the canvas window has changed and update its resolution accordingly.
    #     """
    #     width: int
    #     height: int
    #     width, height = cv2.getWindowImageRect(self.name)[2:]
    #     if width != self.width or height != self.height:
    #         self.resize(width, height)

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

    # TODO: Remove when it is no longer necessary
    def print_calibration_cross(self, camera: Camera) -> None:
        """
        TEMPORARY METHOD: Creates the calibration cross drawing on the CAL_CROSS layer.

        :param camera: A reference to the camera
        """
        color: str = "WHITE"
        size: int = 5

        # print("top left:")
        top_left = camera.transform_point(Point(0, 0), self.width, self.height)
        # print(int(top_left.x), int(top_left.y))

        # print("top right:")
        top_right = camera.transform_point(Point(0, 1), self.width, self.height)
        # print(int(top_right.x), int(top_right.y))

        # print("bot left:")
        bot_left = camera.transform_point(Point(1, 0), self.width, self.height)
        # print(int(bot_left.x), int(bot_left.y))

        # print("bot right:")
        bot_right = camera.transform_point(Point(1, 1), self.width, self.height)
        # print(int(bot_right.x), int(bot_right.y))
