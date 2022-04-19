from collections import namedtuple
from typing import Optional

import numpy as np

from HandTracking.ConfigHandler import ConfigHandler
from HandTracking.PersistenceHandler import PersistenceHandler
from HandTracking.Point import Point
from HandTracking.Canvas import Canvas
from HandTracking.Hand import Hand
from HandTracking.Camera import Camera
from HandTracking.Settings import run_settings as run_settings, Settings
from HandTracking.MenuWheel import MenuWheel

import cv2
import mediapipe as mp

# import cProfile
import bezier

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands


def main(config: Settings) -> int:
    # TODO: Remove when auto calibration is implemented
    drawing_point: Optional[Point] = None
    drawing_precision: int = 5
    point_on_canvas: Optional[Point] = None
    white_screen = np.full(shape=[480, 720, 4], fill_value=[255, 255, 255, 255], dtype=np.uint8)
    hand: Hand = Hand(mp_hand)
    canvas: Canvas = Canvas("Canvas", config.monitor.width, config.monitor.height)
    canvas.move_window(config.monitor.x, config.monitor.y)
    if config.is_fullscreen == 1:
        canvas.fullscreen()

    cal_points: list[Point] = ConfigHandler.load_calibration_points()
    if cal_points:
        camera = Camera(cal_points, camera=config.camera)
    else:
        camera = Camera([Point(1, 0), Point(canvas.width, 0), Point(0, canvas.height),
                         Point(canvas.width - 1, canvas.height)], camera=config.camera)

    camera.update_image_ptm(canvas.width, canvas.height)
    canvas.print_calibration_cross(camera)
    cv2.setMouseCallback(camera.name, lambda event, x, y, flags, param: mouse_click(camera, canvas.width,
                                                                                    canvas.height, event, x,
                                                                                    y))

    menu_wheel = MenuWheel(canvas)

    hands = mp_hand.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.4,
        min_tracking_confidence=0.4)

    counter = 0

    while camera.capture.isOpened():
        camera.update_frame()
        if camera.frame is None:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        camera.show_frame()

        if counter % 2 == 0:
            canvas.wipe()
            canvas.draw()
            drawing_point, point_on_canvas = analyse_frame(camera, hands, hand, canvas, drawing_point,
                                                           drawing_precision, point_on_canvas,
                                                           menu_wheel)
            if len(camera.boundary_points) > 1:
                canvas.show()
            else:
                cv2.imshow(canvas.name, white_screen)


        # TODO: Save the black spots so we can remember the last seen hand position

        status = check_key_presses(canvas, camera)

        counter += 1

        if status == 1:
            return 0
        elif status == 2:
            return 1

    camera.capture.release()


def write_text(image, text):
    cv2.putText(img=image, text=text, org=(50, 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 255, 255), thickness=2)
    cv2.getTextSize(text=text, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, thickness=2)


def analyse_frame(camera, hands, hand, canvas, drawing_point, drawing_precision,
                  point_on_canvas: Optional[Point], menu_wheel):
    camera.frame = cv2.cvtColor(camera.frame, cv2.COLOR_BGR2RGB)

    camera.frame.flags.writeable = False
    hand_position: namedtuple = hands.process(camera.frame)
    camera.frame.flags.writeable = True

    # TODO: figure out the structure of the hand position and landmarks
    if hand_position.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(hand_position.multi_hand_landmarks,
                                              hand_position.multi_handedness):

            # TODO: Remove call when no longer needed. For debugging only
            # draw_hand_landmarks(hand_landmarks, camera.frame)

            hand.update(hand_landmarks)

            # The actual check whether the program should be drawing or not
            if camera.calibration_is_done():
                hand_sign: str = hand.get_hand_sign(camera.frame, hand_landmarks)

                if hand_sign == "Open" or hand_sign == "Pointer":
                    if menu_wheel.is_open:
                        canvas.new_line(force=True)
                        menu_wheel.close_menu()

                # TODO: Add erasing when working on the wheel
                if hand_sign == "Pointer":
                    if menu_wheel.current_tool == "DRAW":
                        normalised_point = camera.normalise_in_boundary(hand.get_index_tip())
                        if normalised_point is not None:
                            point_on_canvas = camera.transform_point(normalised_point, canvas.width, canvas.height)

                        # drawing_point = get_next_drawing_point(point_on_canvas, drawing_point, drawing_precision)
                        # if drawing_point is not None:
                        #     canvas.add_point(drawing_point)
                        canvas.add_point(point_on_canvas)
                    else:
                        normalised_point = camera.normalise_in_boundary(hand.get_index_tip())
                        if normalised_point is not None:
                            point_on_canvas = camera.transform_point(normalised_point, canvas.width, canvas.height)

                        canvas.erase(point_on_canvas, 15)

                else:
                    drawing_point = None

                if hand_sign == "Close":
                    normalised_point = camera.normalise_in_boundary(hand.fingers["INDEX_FINGER"].tip)
                    if normalised_point is not None:
                        menu_point = camera.transform_point(normalised_point, canvas.width, canvas.height)
                        if not menu_wheel.is_open:
                            menu_wheel.center_point = menu_point

                        menu_wheel.open_menu()
                        canvas.draw_circle(menu_point, [0, 255, 0, 255], 5)
                        menu_wheel.check_button_click(menu_point)

                if hand_sign == "Close" or hand_sign == "Open":
                    canvas.new_line()

            # Mask for removing the hand
            mask_points = []
            for point in hand.get_mask_points():
                if camera.normalise_in_boundary(point) is not None:
                    mask_points.append(
                        camera.transform_point(camera.normalise_in_boundary(point), canvas.width, canvas.height))

            canvas.draw_mask_points(mask_points)
            if camera.normalise_in_boundary(hand.fingers["INDEX_FINGER"].tip) is not None:
                canvas.draw_circle(
                    camera.transform_point(camera.normalise_in_boundary(hand.fingers["INDEX_FINGER"].tip), canvas.width,
                                           canvas.height), color=[0, 255, 0, 255], size=3)

    return drawing_point, point_on_canvas


def check_key_presses(canvas, camera):
    # TODO: Write docstring for function
    # Exit program when Esc is pressed
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        return 1
    elif key == 115:  # S
        camera.capture.release()
        cv2.destroyAllWindows()
        PersistenceHandler.save_drawing(canvas.lines)
        return 2
    elif key == 116:    # T
        PersistenceHandler.save_drawing(canvas.lines)

    return 0


def mouse_click(camera, width, height, event, x, y) -> None:
    """
    Callback function for mouse clicks in the camera window.
    Left-clicking will update the calibration points.

    :param camera: A reference to the camera
    :param width: The width of the canvas
    :param height: The height of the canvas
    :param event: The event object, specifying the type of event
    :param x: The x position of the mouse when the event is triggered
    :param y: The y position of the mouse when the event is triggered
    """
    if event == cv2.EVENT_LBUTTONUP:
        camera.update_calibration_point(Point(x, y), width, height)


def get_next_drawing_point(point_on_canvas: Point, drawing_point: Point,
                           drawing_precision: int):
    # TODO: Write docstring for function

    if drawing_point is None:
        drawing_point = point_on_canvas

    if drawing_point is not None:
        if drawing_point.distance_to(point_on_canvas) > drawing_precision:
            drawing_point = drawing_point.next_point_to(point_on_canvas, 1)

    return drawing_point


def draw_hand_landmarks(hand_landmarks, frame) -> None:
    """
    TEMPORARY FUNCTION. Draws the hand landmarks in the camera window, for ease of debugging.

    :param hand_landmarks: The hand landmarks to draw
    :param frame: The frame to draw the landmarks in
    """
    mp_drawing.draw_landmarks(
        frame,
        hand_landmarks,
        mp_hand.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style())

def other_main_stuff():
    startup_dict: dict = ConfigHandler.load_startup_settings()
    settings: Optional[Settings] = None

    if startup_dict:
        settings = Settings.from_dict(startup_dict)
    else:
        settings = run_settings()

    running = main(settings)
    while running:
        settings = run_settings()
        running = main(settings)


if __name__ == "__main__":
    # cProfile.run('other_main_stuff()', "output.dat")
    #
    # import pstats
    #
    # with open("prof_out.prof", "w+") as f:
    #     p = pstats.Stats("output.dat", stream=f)
    #     p.sort_stats("cumtime").print_stats()
    other_main_stuff()

