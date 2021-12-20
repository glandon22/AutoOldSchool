"""
buys sea weed and soda ash from the traders in port khazard
full screen on the 2560x1440 screen
looking due north with view at max altitude
"""
import random
import numpy as np
from PIL import ImageGrab, Image
import cv2
import time
import pyautogui
from bezier import bezierMovement
from general_utils import randomSleep, calcImgDiff, roughImgCompare
import keyboard as kb
import math
import sys

storeInterface = [822, 1422, 427, 790]
bankInterface = [844, 1402, 438, 774]
sodaInStore = [1254, 1276, 606, 616]
seaweedInstore = [1196, 1220, 607, 620]
emptyLastslot = Image.open('.\\screens\\empty_slot.png')
seaweedInBag = [1176, 1199, 558, 576]
sodaInBag = [1177, 1198, 497, 513]
def findFixedObject(image):
    expectedStore = ImageGrab.grab([980, 442, 1054, 463])
    img = Image.open('.\\screens\\bank_interface.png')
    if calcImgDiff(img, expectedStore) < 5:
        return True
    print('looking for martin')
    # cyan color boundaries [B, G, R]
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
        #cv2.drawContours(output, contours, -1, 255, 3)

        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        #this movement must also account for the offset of the target area bbox, i.e. the image coordinates passed to the findFixedObject function
        print(x,y,w,h)
        bezierMovement(x + 400 + (math.floor(w/2)), x + 400 + (math.floor(w/2)), y + math.floor(h / 2), y + math.floor(h / 2))
        randomSleep(0.1,0.3)
        pyautogui.click()
        randomSleep(9.6,10.5)
    return False

def goToBank():
    found = False
    while not found:
        screen =  np.array(ImageGrab.grab(bbox=([400, 0, 2096, 966])))
        didIFind = findFixedObject(screen)
        if didIFind:
            found = True
            randomSleep(0.5,0.7)

def buyStoreItems(shopCoords):
    clickCoords = bezierMovement(shopCoords[0], shopCoords[1], shopCoords[2], shopCoords[3])
    randomSleep(0.2,0.3)
    pyautogui.click(button="right")
    randomSleep(0.1,0.2)
    bezierMovement(clickCoords[0], clickCoords[0] + 15, clickCoords[1] + 100, clickCoords[1] + 108)
    randomSleep(0.2,0.3)
    pyautogui.click()
    randomSleep(0.5,0.7)
    
def isBagFull():
    currSlot = ImageGrab.grab([2474, 1306, 2512, 1330])
    currSlot.save('.\\screens\\currSlot.png')

    if calcImgDiff(currSlot, emptyLastslot) < 2:
        return False
    else:
        return True
def walkToDock():
    bezierMovement(1787, 1883, 1320, 1372)
    randomSleep(0.1,0.2)
    pyautogui.click()
    randomSleep(7.6,8.3)

def hopWorlds():
    kb.send('alt + shift + x')
    randomSleep(3.3,3.9)
    if calcImgDiff(ImageGrab.grab([22, 1212, 590, 1337]), Image.open('.\\screens\\w319.png')) < 3:
        kb.send('space')
        randomSleep(0.4,0.6)
        kb.send('2')
    randomSleep(10.6, 12.4)
    kb.send('esc')
    randomSleep(0.2,0.4)

def process_img(image, iters):
    if iters > 75:
        print('failed to find traders after 150 iterations, program terminating')
        sys.exit()
    elif iters > 50:
        print('checking to see if we are on the ship')
        map = ImageGrab.grab([2450, 76, 2486, 108])
        map.save('.\\screens\\currMap.png')
        if calcImgDiff(map, Image.open('.\\screens\\ship_map.png')) < 2:
            print('on ship')
            bezierMovement(1277, 1290, 672, 685)
            pyautogui.click()
            randomSleep(2.4,3.2)
    expectedStore = ImageGrab.grab([1016, 436, 1064, 450])
    img = Image.open('.\\screens\\stan.png')
    if calcImgDiff(img, expectedStore) < 5:
        return True
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
        bezierMovement((x + 926) + 10, (x + 926) + 15, (y + 344) + 10, (y + 344) + 15)
        randomSleep(0.1,0.2)
        pyautogui.click()
        randomSleep(2.7,3.1)
        #pyautogui.moveTo((x + 926) + 10,(y + 344) + 10)
        # draw the biggest contour (c) in green
    return False

def findSingleTarget():
    iters = 0
    found = False
    while not found:
        iters = iters + 1
        screen =  np.array(ImageGrab.grab(bbox=(926, 344, 1664, 1114)))
        didIFind = process_img(screen, iters)
        if didIFind:
            found = True
            randomSleep(0.5,0.7)
def dumpBag():
    seaweed = roughImgCompare('.\\screens\\sand_in_bag.png', .75, (844, 438, 1402, 774))
    if seaweed:
        bezierMovement(seaweed.get('x'), seaweed.get('x') + 7, seaweed.get('y'), seaweed.get('y') + 9)
        pyautogui.click()
        randomSleep(0.2,0.4)
    soda = roughImgCompare('.\\screens\\soda_in_bag.png', .75, (844, 438, 1402, 774))
    if soda:
        bezierMovement(soda.get('x'), soda.get('x') + 6, soda.get('y'), soda.get('y') + 6)
        pyautogui.click()
        randomSleep(0.2,0.4)
    kb.send('esc')
    randomSleep(0.4,0.6)
def main():
    while True:
        walkToDock()
        #find charter ship traders
        findSingleTarget()
        #buy sand
        buyStoreItems([1138, 1156, 606, 620])
        kb.send('esc')
        bagStatus = isBagFull()
        print('bs', bagStatus)
        #go bank
        while not bagStatus:
            randomSleep(0.2,0.4)
            hopWorlds()
            findSingleTarget()
            #buy sand
            buyStoreItems([1138, 1156, 606, 620])
            bagStatus = isBagFull()
            print('bs1', bagStatus)
            kb.send('esc')
        goToBank()
        dumpBag()
        randomSleep(4.3,5.8)
        if random.randint(1,10) == 2:
            randomSleep(20.3,25.9)
main()
