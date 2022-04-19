class Point:
    def __init__(self, x, y) -> None:
        self.x: float = x
        self.y: float = y

    def __eq__(self, other: 'Point') -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    @classmethod
    def from_landmark(cls, landmark) -> 'Point':
        """
        Overload of the constructor, which gives a Point object from a landmark.

        :param landmark: The landmark to extract coordinates from
        :return: A Point object containing the x and y of the landmark
        """
        x: float = landmark.x
        y: float = landmark.y

        return cls(x, y)

    @classmethod
    def from_dict(cls, dictionary: dict) -> 'Point':
        """
        Overload of the constructor, which gives a Point object from a dictionary of coordinates.

        :param dictionary: The dictionary to extract coordinates from
        :return: A Point object containing the x and y of the dictionary
        """
        x: float = dictionary["x"]
        y: float = dictionary["y"]

        return cls(x, y)

    def distance_to(self, other: 'Point') -> float:
        """
        Calculates the distance between itself an another Point object.

        :param other: The other Point to calculate the distance to
        :return: The distance between self and other
        """
        calculation: float = (self.x - other.x) ** 2 + (self.y - other.y) ** 2
        return calculation

    def next_point_to(self, other: 'Point', precision: int = 3) -> 'Point':
        """
        Finds the midpoint between two points repeatedly in the range from 0 to the given precision.

        :param other: The other point to find the midpoint to
        :param precision: An integer determining how many times an additional midpoint will be calculated iteratively
        :return: The new midpoint
        """
        point: Point = self.__midpoint_to(other)

        for i in range(0, precision):
            point = self.__midpoint_to(point)

        return point

    def __midpoint_to(self, other) -> 'Point':
        """
        Finds the midpoint between two points.

        :param other: The point to find the midpoint to
        :return: The midpoint between self and other
        """
        return Point((self.x + other.x)/2, (self.y + other.y)/2)

    def as_list(self) -> list[float]:
        """
        Converts the Point object to a list of coordinates.

        :return: A list containing the Point object's coordinates
        """
        return [self.x, self.y]
