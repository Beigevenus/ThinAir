import numpy as np
import cv2
from numpy import ndarray

from HandTracking.Point import Point


def four_point_transform(points: list[Point], width: int, height: int):
    # TODO: Write docstring for function
    # put the points into an numpy array
    pts: list[list[float]] = []
    for p in points:
        pts.append([p.x, p.y])
    rect: ndarray = np.array(pts, dtype="float32")

    dst: ndarray = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    m = cv2.getPerspectiveTransform(rect, dst)

    # return the warped image
    return m, width, height
