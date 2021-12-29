import pyautogui
import random
import numpy as np
import time
from scipy import interpolate
import math
import random
import pyautogui
from PIL import Image
from PIL import ImageChops
import pyscreenshot as ImageGrab
import operator
from functools import reduce
import cv2


def point_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def bezierMovement(xMin, xMax, yMin, yMax):
    # Any duration less than this is rounded to 0.0 to instantly move the mouse.
    pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
    # Minimal number of seconds to sleep between mouse moves.
    pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
    # The number of seconds to pause after EVERY public function call.
    pyautogui.PAUSE = 0  # Default: 0.1
    cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
    x1, y1 = pyautogui.position()
    x2 = random.randint(xMin, xMax)
    y2 = random.randint(yMin, yMax)
    print('clicking ', x2, y2)
    # Distribute control points between start and destination evenly.
    x = np.linspace(x1, x2, num=cp, dtype='int')
    y = np.linspace(y1, y2, num=cp, dtype='int')

    # Randomise inner points a bit (+-RND at most).
    RND = 10
    xr = [random.randint(-RND, RND) for k in range(cp)]
    yr = [random.randint(-RND, RND) for k in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr

    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
    # Must be less than number of control points.
    tck, u = interpolate.splprep([x, y], k=degree)
    # Move upto a certain number of points
    u = np.linspace(0, 1, num=2 + int(point_dist(x1, y1, x2, y2) / 50.0))
    points = interpolate.splev(u, tck)

    # Move mouse.
    duration = 0.1
    timeout = duration / len(points[0])
    point_list = zip(*(i.astype(int) for i in points))
    for point in point_list:
        pyautogui.moveTo(*point)
        time.sleep(timeout)
    return [x2, y2]


def calcImgDiff(im1, im2, acceptableDiff):
    imageDifference = ImageChops.difference(im1, im2).histogram()
    diff = math.sqrt(reduce(operator.add,
                            map(lambda h, i: h * (i ** 2), imageDifference, range(256))
                            ) / (float(im1.size[0]) * im2.size[1]))
    if diff > acceptableDiff:
        return 'different'
    else:
        return 'same'


def randomSleep(min, max):
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


def roughImgCompare(img, confidence, region):
    loc = pyautogui.locateOnScreen(img, confidence=confidence, region=region)
    if loc:
        return {'x': loc[0], 'y': loc[1]}
    return False


def didLevel():
    status = roughImgCompare('..\\screens\\level.png', .8, (2, 645, 1190, 1350))
    if status:
        return True
    else:
        return False


def dumpBag():
    location = roughImgCompare('..\\screens\\dump.png', .8, (0, 0, 2559, 1439))
    if not location:
        return False
    bezierMovement(location.get('x'), location.get('x') + 5, location.get('y'), location.get('y') + 5)
    randomSleep(0.2, 0.3)
    pyautogui.click()
    return True


def findFixedObject(image, xOffset, yOffset):
    # red color boundaries R,G,B
    lower = [255, 0, 0]
    upper = [255, 0, 0]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    _, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        # this movement must also account for the offset of the target area bbox, i.e. the image coordinates passed to the findFixedObject function
        bezierMovement(x + xOffset + (math.floor(w / 2)), x + xOffset + (math.floor(w / 2)),
                       y + yOffset + math.floor(h / 2), y + yOffset + math.floor(h / 2))
        randomSleep(0.1, 0.3)
        pyautogui.click()
        return True
    return False


def goToTarget(targArea):
    attempts = 0
    while True:
        print(attempts)
        screen = np.array(ImageGrab.grab(bbox=(targArea)))
        didIFind = findFixedObject(screen, targArea[0], targArea[1])
        if didIFind:
            randomSleep(0.5, 0.7)
            return True
        elif attempts > 10:
            print('exiting, was unable to find target')
            return False
        else:
            attempts += 1


def withdrawItemsFromBank(items, bankInterface):
    randomSleep(0.5, 0.9)
    for item in items:
        targ = roughImgCompare('..\\screens\\' + item, .75,
                               (bankInterface[0], bankInterface[2], bankInterface[1], bankInterface[3]))
        if targ:
            print('taking ', item, ' from the bank')
            bezierMovement(targ.get('x'), targ.get('x') + 6, targ.get('y'), targ.get('y') + 6)
            pyautogui.click()
            randomSleep(0.2, 0.4)
        else:
            return 'unable to find anymore ' + item
    return 'success'


def process_with_tool(slot, button, expected_last_slot, max_cycles):
    # click on knife
    bezierMovement(2317, 2343, 1030, 1056)
    pyautogui.click()
    randomSleep(0.2, 0.5)
    # click on log
    if slot == 1:
        bezierMovement(2371, 2395, 1034, 1058)
    else:
        bezierMovement(2476, 2500, 1304, 1324)
    pyautogui.click()
    randomSleep(1.2, 1.7)
    pyautogui.press(button)
    randomSleep(0.3, 0.7)
    # move off-screen
    bezierMovement(3500, 4000, 0, 250)
    randomSleep(0.4, 0.7)
    pyautogui.click()
    cycles_waiting = 0
    while True:
        last_slot = calcImgDiff(Image.open(expected_last_slot), ImageGrab.grab([2476, 1304, 2500, 1324]), 3)
        if last_slot == 'same':
            break
        elif didLevel():
            restart = process_with_tool(27, '7', '.\\screens\\lens_in_bag.png', 35)
            if restart != 'success':
                return 'after leveling, did not successfully finish processing'
        elif cycles_waiting > max_cycles:
            return 'did not finishing processing in acceptable number of cycles'
        else:
            cycles_waiting += 1
        randomSleep(1.4, 2.6)
    return 'success'
