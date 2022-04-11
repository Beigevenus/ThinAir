from HandTracking.Point import Point
from scipy import interpolate

import numpy as np
import cv2


# A basic min/max function
def limit(num: float, minimum: float = 0, maximum: float = 255) -> float:
    # TODO: Write docstring for function
    return max(min(num, maximum), minimum)


# Function to find blackboard in camera using the calibration points as reference, and
# then choosing the xv, that is closest to the given corner
# TODO: Maybe delete, since automatic calibration is not necessary since manual calibration does not take long.
# Needs to be done either way
def find_corners_from_color(image):
    # TODO: Change the names of EVERYTHING so that it makes sense
    image_height = 0
    image_width = 0

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define blue color range
    light_blue = np.array([255, 255, 0])
    dark_blue = np.array([220, 220, 20])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, light_blue, dark_blue)

    # Bitwise-AND mask and original image
    output = cv2.bitwise_and(image, image, mask=mask)

    # Row and columns
    for i in image:
        for j in i:
            if j[0] > image_width:
                image_width = j[0]
            if j[1] > image_height:
                image_height = j[1]

    corners = [
        Point(0, 0),
        Point(image_width, 0),
        Point(0, image_height),
        Point(image_width, image_height)
    ]

    # Gets the colored points from the image and
    x, y = np.where(np.all(output != [0, 0, 0], axis=2))
    # Converts them to the point objects
    colored_points = []
    for point in range(0, len(x)):
        colored_points[point].x = x[point]
        colored_points[point].y = y[point]

    actual_corners = [
        Point(image_width / 2, image_height / 2),
        Point(image_width / 2, image_height / 2),
        Point(image_width / 2, image_height / 2),
        Point(image_width / 2, image_height / 2)
    ]

    print(
        f'{actual_corners[0].x}, {actual_corners[0].y}, \n '
        f'{actual_corners[1].x}, {actual_corners[1].y}, \n '
        f'{actual_corners[2].x}, {actual_corners[2].y}, \n '
        f'{actual_corners[3].x}, {actual_corners[3].y},')

    for point in colored_points:
        for i in range(0, len(colored_points)):
            if point.distance_to(corners[i]) < corners[i].distance_to(actual_corners[i]):
                actual_corners[i] = point

    print(
        f'{actual_corners[0].x}, {actual_corners[0].y}, \n'
        f'{actual_corners[1].x}, {actual_corners[1].y}, \n'
        f'{actual_corners[2].x}, {actual_corners[2].y}, \n'
        f'{actual_corners[3].x}, {actual_corners[3].y},')

    return actual_corners


def b_spline(points):
    x = []
    y = []
    cp = []
    degree = 4

    for point in points:
        x.append(point.x)
        y.append(point.y)

    if len(points) <= degree:
        degree = 1

    tck, *rest = interpolate.splprep([x, y], k=degree)
    u = np.linspace(0, 1, num=len(points) * 4)
    smooth = interpolate.splev(u, tck)

    for i in range(0, len(smooth[0])):
        cp.append(Point(smooth[0][i], smooth[1][i]))

    return cp


def adjusted_r(x, y, degree):
    """
    Finds the adjusted squared R in order to find
    the most optimal n-degree polynomial over any
    amount of points.

    :param x: Array of the x-coordinates
    :param y: Array of the y-coordinates
    :param degree: The n-degree polynomial
    :return:
    """
    coeffs = np.polyfit(x, y, degree)
    p = np.poly1d(coeffs)
    yhat = p(x)
    ybar = np.sum(y) / len(y)
    ssreg = np.sum((yhat - ybar) ** 2)
    sstot = np.sum((y - ybar) ** 2)
    result = 1 - (((1 - (ssreg / sstot)) * (len(y) - 1)) / (len(y) - degree - 1))

    return result


def __calc_polynomials(x, y, degree):
    """
    This functions returns the functions made
    from the given points x and y values also
    known as models.

    :param x: Array of the x-coordinates
    :param y: Array of the y-coordinates
    :param degree: The n-degree polynomial
    :return: The "function" also called model
    """
    models = {}

    for i in range(0, degree):
        models[f'model{i}'] = [np.poly1d(np.polyfit(x, y, i)), adjusted_r(x, y, i)]

    return models


def __arr_from_points(points):
    """
    Makes two arrays from the array of points.
    One for the x-coordinates and one for the y.
    """
    x = []
    y = []

    for point in points:
        x.append(point.x)
        y.append(point.y)

    return x, y


def __find_optimal_polynomial(points, degree):
    x, y = __arr_from_points(points)
    models = __calc_polynomials(x, y, degree)

    best_model = [np.poly1d(np.polyfit(x, y, 1)), 0]

    for i in range(0, degree):
        if models[f'model{i}'][1] > best_model[1]:
            best_model = models[f'model{i}']

    return best_model


def smooth_points(points, degree):
    model = __find_optimal_polynomial(points, degree)

    # add fitted polynomial curve to scatterplot

    for point in points:
        point.y = model[0](point.x)

    return points
