import numpy as np
from PIL import ImageGrab, Image
import cv2
import time
import pyautogui
from bezier import bezierMovement
from general_utils import randomSleep, calcImgDiff
import keyboard as kb
storeInterface = [822, 1422, 427, 790]
bankInterface = [844, 1402, 438, 774]
sodaInStore = [1254, 1276, 606, 616]
seaweedInstore = [1196, 1220, 607, 620]
emptyLastslot = Image.open('.\\screens\\empty_slot.png')

def findFixedObject(image):
    expectedStore = ImageGrab.grab([980, 442, 1054, 463])
    img = Image.open('.\\screens\\bank_interface.png')
    if calcImgDiff(img, expectedStore) < 5:
        return True
    print('looking for martin')
    # red color boundaries [r, g, b]
    lower = [255, 0, 0]
    upper = [255, 0, 0]

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
        pyautogui.moveTo(x + 400,y)
        # draw the biggest contour (c) in green
        cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)
    return np.hstack([image, output])
while True:
    screen =  np.array(ImageGrab.grab(bbox=([400, 0, 2096, 966])))
    new_screen = findFixedObject(screen)
    cv2.imshow('window', new_screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break