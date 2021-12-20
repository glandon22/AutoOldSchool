#this program looks for a cyan shape and highlights it then tracks it with the mouse
import numpy as np
from PIL import ImageGrab
import cv2
import time

import pyautogui

def process_img(image):
    # cyan color boundaries [B, G, R]
    lower = [0, 255, 255]
    upper = [0, 255, 255]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    ret,thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, 255, 3)

        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        print(x,y,w,h)
        pyautogui.moveTo((x + 805) + 10,(y + 36) + 10)
        # draw the biggest contour (c) in green
        cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)
    return np.hstack([image, output])

def main():
    while True:
        screen =  np.array(ImageGrab.grab(bbox=(805,36,1444,444)))
        start_time = time.time()
        new_screen = process_img(screen)
        cv2.imshow('window', new_screen)
        print("FPS: ", 1.0 / (time.time() - start_time))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
main()