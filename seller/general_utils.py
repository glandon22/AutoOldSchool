import random
import time
import pyautogui
import mouse
from PIL import Image
from PIL import ImageChops
import pyscreenshot as ImageGrab
import math,operator
from functools import reduce
import sys
import numpy
import cv2
from bezier import bezierMovement
import sys
numpy.set_printoptions(threshold=sys.maxsize)
#chat box coords
#im = ImageGrab.grab([2,1190,645,1350])

#inv coords
#im = ImageGrab.grab([2299, 2510, 1024, 1324])

def calcImgDiff(im1, im2):
    imageDifference = ImageChops.difference(im1,im2).histogram()
    diff = math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), imageDifference, range(256))
    ) / (float(im1.size[0]) * im2.size[1]))
    return diff

def randomSleep(min,max):
    duration = round(random.uniform(min, max), 3)
    print("Sleeping for ", duration, ' seconds')
    time.sleep(duration)

def showInvCoords(slot):
    invCoords = [
        [2317, 2343, 1030, 1056], [2371, 2395, 1034, 1058], [2424, 2448, 1034, 1060], [2476, 2500, 1036, 1058],
        [2320, 2344, 1082, 1103], [2372, 2394, 1082, 1102], [2425, 2448, 1082, 1100], [2478, 2499, 1082, 1102],
        [2320, 2340, 1128, 1144], [2372, 2395, 1126, 1146], [2422, 2446, 1126, 1144], [2476, 2500, 1127, 1142],
        [2323, 2340, 1168, 1190], [2372, 2396, 1172, 1192], [2424, 2446, 1174, 1192], [2478, 2503, 1173, 1190],
        [2320, 2342, 1216, 1238], [2374, 2394, 1215, 1238], [2425, 2447, 1216, 1233], [2479, 2500, 1220, 1238],
        [2320, 2342, 1259, 1282], [2372, 2394, 1261, 1280], [2425, 2446, 1262, 1280], [2478, 2500, 1261, 1280],
        [2319, 2342, 1305, 1326], [2370, 2393, 1306, 1322], [2426, 2445, 1306, 1324], [2476, 2500, 1304, 1324]
    ]
    return invCoords[slot]

def calculateClickbox():
    i = 0
    points = list()
    while i < 4:
        print('position mouse for click ', i, ' in 3 seconds')
        time.sleep(3)
        points.append(pyautogui.position())
        i = i + 1
    x1 = round((points[0].x + points[3].x) / 2)
    x2 = round((points[1].x + points[2].x) / 2)
    y1 = round((points[0].y + points[1].y) / 2)
    y2 = round((points[2].y + points[3].y) / 2)
    print([x1,x2,y1,y2])
    return [x1,x2,y1,y2]    

def getInvCoords():
    fullCoords = []
    i = 0
    while i < 28:
        print('getting inv slot ', i + 1)
        fullCoords.append(calculateClickbox())
        print('full coords ', fullCoords)
        print(i + 1, ' completed. moving to next slot')
        i = i + 1

def captureScreenshot(name):
    screenshotBox = calculateClickbox()
    print('sc box', screenshotBox)
    im = ImageGrab.grab([screenshotBox[0],screenshotBox[2],screenshotBox[1],screenshotBox[3]])
    # save image file
    im.save(r'screens\\' +name + '.png', 'png')

def captureSpecificScreenCoords(screenshotBox, name):
    im = ImageGrab.grab([screenshotBox[0],screenshotBox[2],screenshotBox[1],screenshotBox[3]])
    # save image file
    im.save(r'screens\\' + name + '.png', 'png')
    return im

def checkBag():
    ironOreCoords = showInvCoords(0)
    im = ImageGrab.grab([ironOreCoords[0],ironOreCoords[2],ironOreCoords[1],ironOreCoords[3]])
    diff = calcImgDiff(im, emptySlot)
    if diff > 5:
        return True
    else:
        return False
def testImgDetect():
    myScreen = ImageGrab.grab([0,0,1560,1440])
    myScreen.save(r'screens\\' + 'test_screen' + '.png', 'png')
    big = Image.open('.\\screens\\test_screen.png')
    here = Image.open('.\\screens\\test_box.png')
    herear = numpy.asarray(here)
    bigar  = numpy.asarray(big) 
    hereary, herearx = herear.shape[:2]
    bigary,  bigarx  = bigar.shape[:2]

    stopx = bigarx - herearx + 1
    stopy = bigary - hereary + 1

    for x in range(0, stopx):
        for y in range(0, stopy):
            x2 = x + herearx
            y2 = y + hereary
            pic = bigar[y:y2, x:x2]
            test = (pic == herear)
            if test.all():
                print(x,y)

def isInvFull(currInv, fullInv):
    diff = calcImgDiff(currInv, fullInv)
    print('bag diff', diff)
    if diff < 2: return True
    else: return False
def nextTreeIsUp(curr, expected):
    diff = calcImgDiff(curr, expected)
    print('next tree status diff', diff)
    if diff < 57: return True
    else: return False
def amChopping(curr, expected):
    diff = calcImgDiff(curr, expected)
    print('chop status diff', diff)
    if diff < 10: return True
    else: return False
def chopTree(coords):
    print('beginning to chop tree')
    bezierMovement(coords[0],coords[1],coords[2],coords[3])
    randomSleep(0.1,0.2)
    pyautogui.click()
    bezierMovement(3100,3700,500,1000)
    randomSleep(0.1,0.2)
    pyautogui.click()
    return 'chopping'
def captureUnderMouse(name):
    print('capturing hover bar')
    currentMouseX, currentMouseY = pyautogui.position()
    hover = ImageGrab.grab([currentMouseX + 1,currentMouseY + 31,currentMouseX + 140,currentMouseY + 49])
    hover.save(r'screens\\' +  name + '.png', 'png')
    return hover
def roughImgCompare(img, confidence, region):
    loc = pyautogui.locateOnScreen(img, confidence=confidence, region=region)
    if loc:
        return {'x': loc[0], 'y': loc[1]}
    return False
def cutStatus():
    status = ImageGrab.grab([0,  0, 200,200])
    status = numpy.asarray(status)
    greenPixels = 0
    for row in status:
        for val in row:
            if numpy.all(val == [0,255,0]):
                print('here')
                greenPixels = greenPixels + 1
            if greenPixels > 10:
                break
def quickScreenshot(name, add):
    print('ready in 3')
    time.sleep(3)
    x,y = pyautogui.position()
    print('sc box', x,y)
    im = ImageGrab.grab([x,y,x + add,y + add])
    # save image file
    im.save(r'screens\\' +name + '.png', 'png')
def getPos():
    time.sleep(2)
    print(pyautogui.position())
def testfunc():
    screen = ImageGrab.grab([750,0,1900,1440])
    screen.save('.\\screens\\test.png')
    screen = numpy.asarray(screen)
def roughImgCompare(img, confidence, region):
    loc = pyautogui.locateOnScreen(img, confidence=confidence, region=region)
    if loc:
        return {'x': loc[0], 'y': loc[1]}
    return False
