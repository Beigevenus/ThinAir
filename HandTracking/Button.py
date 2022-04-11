from HandTracking.Point import Point


class Button:
    def __init__(self, callback, color: str = 'WHITE', active: bool = False):
        self.size: int = 25
        self.location: Point = Point(0, 0)
        self.active: bool = active
        self.color = color
        self.callback = callback

    def set_location(self, point: Point):
        self.location = point

    def is_point_in_circle(self, point: Point) -> bool:
        # TODO: Write docstring for method
        return pow(point.x - self.location.x, 2) + pow(point.y - self.location.y, 2) < pow(self.size / 2, 2)
