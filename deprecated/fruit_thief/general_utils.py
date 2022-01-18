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
emptySlot = Image.open('screens/empty_slot.png')

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

def captureScreenshot():
    screenshotBox = calculateClickbox()
    print('sc box', screenshotBox)
    im = ImageGrab.grab([screenshotBox[0],screenshotBox[2],screenshotBox[1],screenshotBox[3]])
    # save image file
    im.save(r'screens\\' + sys.argv[1] + '.png', 'png')
def captureSpecificScreenCoords(screenshotBox):
    im = ImageGrab.grab([screenshotBox[0],screenshotBox[2],screenshotBox[1],screenshotBox[3]])
    # save image file
    im.save(r'screens\\' + sys.argv[1] + '.png', 'png')

def checkBag():
    ironOreCoords = showInvCoords(0)
    im = ImageGrab.grab([ironOreCoords[0],ironOreCoords[2],ironOreCoords[1],ironOreCoords[3]])
    diff = calcImgDiff(im, emptySlot)
    if diff > 5:
        return True
    else:
        return False
