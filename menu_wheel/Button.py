import cv2
from model.Point import Point


class Button:
    def __init__(self, callback, color: str = 'WHITE', active: bool = False, icon: str = None):
        self.size: int = 25
        self.location: Point = Point(0, 0)
        self.active: bool = active
        self.color = color
        self.callback = callback
        self.icon: str = icon

        if self.icon is not None:
            self.set_icon(self.icon)

    def set_location(self, point: Point) -> None:
        self.location = point

    def is_point_in_circle(self, point: Point) -> bool:
        """
        Determines whether a given point exists within the button's boundaries.

        :param point: The point to check
        :return: True if the point is within the button's boundaries, False if not
        """
        return pow(point.x - self.location.x, 2) + pow(point.y - self.location.y, 2) < pow(self.size / 2, 2)

    def set_icon(self, icon: str) -> None:
        self.icon = cv2.imread("menu_wheel/resources/{img_name}".format(img_name=icon), -1)
