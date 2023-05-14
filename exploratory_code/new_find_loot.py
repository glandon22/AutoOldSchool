import numpy as np
import pyautogui
from PIL import ImageGrab
import cv2
import time
from autoscape import general_utils


def find_highlighted_item_on_ground_draw(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])

    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160, 100, 20])
    upper2 = np.array([179, 255, 255])

    lower_mask = cv2.inRange(image, lower1, upper1)
    upper_mask = cv2.inRange(image, lower2, upper2)

    mask = lower_mask + upper_mask

    output = cv2.bitwise_and(image, image, mask=mask)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        print('iter')
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, 255, 3)
        ## find all contours that look like highlighted tiles
        print('len', len(contours))
        distance = 999999999
        closest_coords = [0, 0, 0, 0]
        closest_contour = None
        center = None
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)

            if 70 >= w >= 20 and 70 >= h >= 20:
                current_distance = general_utils.point_dist(1275, 715, x, y)
                if current_distance < distance:
                    closest_coords = [x, y, w, h]
                    distance = current_distance
                    closest_contour = c
        if closest_contour is not None:
            center = general_utils.find_contour_center(closest_contour)
            cv2.drawContours(output, [c], -1, (0, 255, 0), 2)
            cv2.circle(output, (center[0], center[1]), 7, (0, 0, 255), -1)
            cv2.putText(output, "center", (center[0] - 20, center[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return np.array(output)


def find_highlighted_item_on_ground(image, x_off, y_off):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])

    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160, 100, 20])
    upper2 = np.array([179, 255, 255])

    lower_mask = cv2.inRange(image, lower1, upper1)
    upper_mask = cv2.inRange(image, lower2, upper2)

    mask = lower_mask + upper_mask
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        ## find all contours that look like highlighted tiles
        distance = 999999999
        closest_coords = [0, 0, 0, 0]
        closest_contour = None
        center = None
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)

            if 70 >= w >= 20 and 70 >= h >= 20:
                current_distance = general_utils.point_dist(1275, 715, x, y)
                if current_distance < distance:
                    closest_coords = [x, y, w, h]
                    distance = current_distance
                    closest_contour = c
        if closest_contour is not None:
            center = general_utils.find_contour_center(closest_contour)
            return [center[0] + x_off, center[1] + y_off]
    return None


while True:
    screen = np.array(ImageGrab.grab([468, 102, 2150, 1224]))
    start_time = time.time()
    new_screen = find_highlighted_item_on_ground(screen, 468, 102)
    if new_screen:
        pyautogui.moveTo(new_screen[0], new_screen[1])
    print('ns', new_screen)
    print("FPS: ", 1.0 / (time.time() - start_time))