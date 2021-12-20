import numpy as np
from PIL import ImageGrab, Image
import cv2
import time
import pyautogui
from bezier import bezierMovement
from general_utils import randomSleep, calcImgDiff
import keyboard as kb

def sellBows():
    clickCoords = bezierMovement(1513, 1534, 303, 325)
    print('prev right click coords', clickCoords)
    randomSleep(0.1,0.2)
    pyautogui.click(button='RIGHT')
    randomSleep(0.2,0.4)
    #sell all bows
    bezierMovement(1513, 1534,clickCoords[1] + 100,clickCoords[1] + 108)
    randomSleep(0.1,0.2)
    pyautogui.click()
    randomSleep(0.3,0.5)
    kb.send('esc')
    randomSleep(0.3,0.5)

def hopWorlds():
    kb.send('alt + shift + x')
    randomSleep(10.6, 12.4)
    kb.send('esc')
    randomSleep(0.2,0.4)

def process_img(image):
    print('looking for martin')
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
        #cv2.drawContours(output, contours, -1, 255, 3)

        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        bezierMovement((x + 805) + 10, (x + 805) + 15, (y + 36) + 10, (y + 36) + 15)
        pyautogui.click()
        randomSleep(0.5,0.7)
        #pyautogui.moveTo((x + 805) + 10,(y + 36) + 10)
        # draw the biggest contour (c) in green
    expctedStore = ImageGrab.grab([996, 71, 1048, 84])
    if calcImgDiff(expctedStore, Image.open('.\\screens\\shop_interface.png')) < 5:
        return True
    else:
        return False

def findSingleTarget():
    found = False
    while not found:
        screen =  np.array(ImageGrab.grab(bbox=(805,36,1444,444)))
        didIFind = process_img(screen)
        if didIFind:
            found = True

def main():
    while True:
        findSingleTarget()
        sellBows()
        hopWorlds()
main()