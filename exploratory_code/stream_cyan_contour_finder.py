import numpy as np
from PIL import ImageGrab
import cv2
import time
from autoscape import general_utils
mini_map_north_click = [2440, 2458, 42, 54]
# click north every couple seconds until i see the cyan blobs
# click a cyan blob
# have to figure out how to pick up drops
# it appears my character sstays generally with then 1260-1290 for x and 700-730 for y
# next id liek to try to highlight the monster that is closest to me

def my_func(image):
    lower = [170, 0, 255]
    upper = [170, 0, 255]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    return np.array(image)

def main():
    while True:
        screen = np.array(ImageGrab.grab())
        start_time = time.time()
        new_screen = general_utils.find_moving_target_with_draw(screen)
        cv2.imshow('window', new_screen)
        print("FPS: ", 1.0 / (time.time() - start_time))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def main1():
    while True:
        screen = np.array(ImageGrab.grab())
        start_time = time.time()
        new_screen = general_utils.find_click_x_with_draw(screen)
        cv2.imshow('window', new_screen)
        print("FPS: ", 1.0 / (time.time() - start_time))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
def main2():
    while True:
        screen = np.array(ImageGrab.grab((100, 100, 2460, 1340)))
        start_time = time.time()
        new_screen = my_func(screen)
        cv2.imshow('window', new_screen)
        print("FPS: ", 1.0 / (time.time() - start_time))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
main1()

