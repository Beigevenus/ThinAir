import cv2
from model.Point import Point


class Button:
    def __init__(self, callback, color: str = 'WHITE', active: bool = False, icon: str = None, offset: tuple = (0, 0)):
        self.size: int = 25
        self.location: Point = Point(0, 0)
        self.active: bool = active
        self.color = color
        self.callback = callback
        self.icon: str = icon
        self.offset = offset
        self.click_location: Point = Point(0, 0)

        if self.icon is not None:
            self.set_icon(self.icon)

    def set_location(self, point: Point):
        self.location = point
        self.click_location = Point(point.x + self.offset[0], point.y + self.offset[1])

    def is_point_in_circle(self, point: Point) -> bool:
        """
        Determines whether a given point exists within the button's boundaries.

        :param point: The point to check
        :return: True if the point is within the button's boundaries, False if not
        """
        return pow(point.x - self.click_location.x, 2) + pow(point.y - self.click_location.y, 2) < pow(self.size / 2, 2)

    def set_icon(self, icon: str):
        self.icon = cv2.imread("menu_wheel/resources/{img_name}".format(img_name=icon), -1)
