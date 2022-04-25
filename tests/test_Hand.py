import pytest

from model.Hand import Hand
from model.Point import Point

x_fail = pytest.mark.xfail


class TestHand:
    @pytest.mark.parametrize("index_tip", [(Point(0, 0)), (Point(35, 103)), (Point(-82, 7)),
                                           (Point(5, -9)), (Point(7374, -27432))])
    def test_get_index_tip(self, index_tip):
        # Arrange
        hand: Hand = Hand.__new__(Hand)
        hand.fingers = {"THUMB": Hand.Finger(),
                        "INDEX_FINGER": Hand.Finger(),
                        "MIDDLE_FINGER": Hand.Finger(),
                        "RING_FINGER": Hand.Finger(),
                        "PINKY": Hand.Finger()}
        hand.fingers["INDEX_FINGER"].tip = index_tip

        # Act
        actual: Point = hand.get_index_tip()

        # Assert
        assert actual == index_tip

    # TODO: Write test case
    def test_get_mask_points(self):
        pass

    @pytest.mark.parametrize("mcp, pip, dip, tip", [(Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)),
                                                    (Point(-6, 9), Point(8, -35), Point(634, -824), Point(1, 1)),
                                                    (None, None, None, None)])
    def test_update_finger(self, mcp, pip, dip, tip):
        # Arrange
        finger: Hand.Finger = Hand.Finger()

        # Act
        finger.update_finger(mcp, pip, dip, tip)

        # Assert
        assert finger.mcp == mcp
        assert finger.pip == pip
        assert finger.dip == dip
        assert finger.tip == tip
