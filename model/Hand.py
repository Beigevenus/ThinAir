from typing import Optional

from model.Point import Point
from keypoint_classifier.keypoint_classifier import KeyPointClassifier


class Hand:
    def __init__(self, mp_hand) -> None:
        self.mp_hand = mp_hand
        self.wrist: Optional[Point] = None
        self.fingers: dict = {"THUMB": self.Finger(),
                              "INDEX_FINGER": self.Finger(),
                              "MIDDLE_FINGER": self.Finger(),
                              "RING_FINGER": self.Finger(),
                              "PINKY": self.Finger()}
        self.keypoint_classifier = KeyPointClassifier()

    def update(self, landmarks) -> None:
        """
        Given hand landmarks from Mediapipe, this method updates the position of each of the Finger objects pertaining
        to the hand.

        :param landmarks: Hand landmarks from Mediapipe
        """
        self.wrist = Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark.WRIST])
        # TODO: Make thumb great again
        for key in self.fingers.keys():
            if key == "THUMB":
                self.fingers["THUMB"].update_finger(
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_CMC"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_MCP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_IP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"THUMB_TIP"]]))
            else:
                self.fingers[key].update_finger(
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_MCP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_PIP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_DIP"]]),
                    Point.from_landmark(landmarks.landmark[self.mp_hand.HandLandmark[f"{key}_TIP"]]))

    def get_index_tip(self) -> Point:
        """
        Returns the position of the part of the hand that is used for drawing.
        Currently, this is the tip of the index finger.

        :return: The Point that is used for drawing
        """
        return self.fingers["INDEX_FINGER"].tip

    def get_mask_points(self) -> list[Point]:
        """
        Returns a list of points corresponding to the position of the user's fingers and wrist.

        :return: A list of points
        """
        points: list[Point] = []

        for finger in self.fingers.values():
            points.append(finger.mcp)
            points.append(finger.pip)
            points.append(finger.dip)

        wrist = self.wrist
        imcp = self.fingers["INDEX_FINGER"].mcp
        pmcp = self.fingers["PINKY"].mcp

        points.append(Point((imcp.x + wrist.x) / 2, (imcp.y + wrist.y) / 2))
        points.append(Point((pmcp.x + wrist.x) / 2, (pmcp.y + wrist.y) / 2))

        points.append(self.wrist)
        return points

    def get_hand_sign(self, camera_frame, landmarks) -> str:
        return self.keypoint_classifier.get_hand_sign(camera_frame, landmarks)

    class Finger:
        def __init__(self, mcp: Point = None, pip: Point = None, dip: Point = None, tip: Point = None):
            self.mcp: Point = mcp
            self.pip: Point = pip
            self.dip: Point = dip
            self.tip: Point = tip
            self.distance_to_wrist: float = 0
            self.length: float = 0
            self.stretched_guard: float = 0

        def __str__(self) -> str:
            return f"({self.mcp}, {self.pip}, {self.dip}, {self.tip})"

        def update_finger(self, mcp: Point = None, pip: Point = None, dip: Point = None, tip: Point = None) -> None:
            """
            Updates the coordinates of each part of the finger.

            :param mcp: A point corresponding to the MCP position
            :param pip: A point corresponding to the PIP position
            :param dip: A point corresponding to the DIP position
            :param tip: A point corresponding to the TIP position
            """
            self.mcp = mcp
            self.pip = pip
            self.dip = dip
            self.tip = tip
