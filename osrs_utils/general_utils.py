# chat box coords
# im = ImageGrab.grab([2,1190,645,1350])

# inv coords
# im = ImageGrab.grab([2299, 2510, 1024, 1324])
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
import keyboard as kb
import pytesseract

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


def dump_bag():
    location = roughImgCompare('..\\screens\\dump.png', .8, (0, 0, 2559, 1439))
    if not location:
        return False
    bezierMovement(location.get('x'), location.get('x') + 5, location.get('y'), location.get('y') + 5)
    randomSleep(0.2, 0.3)
    pyautogui.click()
    return 'success'


def find_fixed_object(image, x_offset, y_offset):
    # image = np.array(ImageGrab.grab(box))
    # red color boundaries R,G,B
    lower = [255, 255, 0]
    upper = [255, 255, 0]

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
        bezierMovement(x + x_offset + (math.floor(w / 2)), x + x_offset + (math.floor(w / 2)),
                       y + y_offset + math.floor(h / 2), y + y_offset + math.floor(h / 2))
        randomSleep(0.1, 0.3)
        pyautogui.click()
        return True
    return False


def goToTarget(targArea):
    attempts = 0
    while True:
        print(attempts)
        screen = np.array(ImageGrab.grab(targArea))
        didIFind = find_fixed_object(screen, targArea[0], targArea[1])
        if didIFind:
            randomSleep(0.5, 0.7)
            return True
        elif attempts > 10:
            print('exiting, was unable to find target')
            return False
        else:
            attempts += 1


def withdraw_items_from_bank(items, bank_interface):
    for item in items:
        targ = roughImgCompare('..\\screens\\' + item, .75,
                               (bank_interface[0], bank_interface[2], bank_interface[1], bank_interface[3]))
        if targ:
            print('taking ', item, ' from the bank')
            bezierMovement(targ.get('x'), targ.get('x') + 6, targ.get('y'), targ.get('y') + 6)
            pyautogui.click()
            randomSleep(0.2, 0.4)
        else:
            return 'unable to find any more ' + item
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


def hop_worlds():
    kb.send('alt + shift + x')
    randomSleep(3.3, 3.9)
    if calcImgDiff(ImageGrab.grab([22, 1212, 590, 1337]), Image.open('.\\screens\\w319.png'), 3) == 'same':
        print('hopping to world 319')
        kb.send('space')
        randomSleep(0.7, 0.9)
        kb.send('2')
    post_hop = Image.open('..\\screens\\post_hop.png')
    cycles_waiting = 0
    while True:
        if roughImgCompare(post_hop, .8, (2270, 971, 2546, 1382)):
            break
        elif cycles_waiting > 1000:
            return 'failed to hop worlds'
        else:
            cycles_waiting += 1
        randomSleep(0.2, 0.5)
    print('hitting esc')
    kb.send('esc')
    randomSleep(0.2, 0.4)
    return 'success'


def find_fixed_npc(box, x_offset, y_offset):
    image = np.array(ImageGrab.grab(bbox=box))
    # red color boundaries R,G,B
    lower = [0, 255, 255]
    upper = [0, 255, 255]

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
        # this movement must also account for the offset of the target area bbox, i.e. the image coordinates passed
        # to the findFixedObject function
        bezierMovement(x + x_offset + (math.floor(w / 2)), x + x_offset + (math.floor(w / 2)),
                       y + y_offset + math.floor(h / 2), y + y_offset + math.floor(h / 2))
        randomSleep(0.1, 0.3)
        pyautogui.click()
        return True
    return False


def wait_for_bank_interface(interface_loc, max_cycles):
    cycles_waiting = 0
    while True:
        location = roughImgCompare('..\\screens\\dump.png', .8,
                                   (interface_loc[0], interface_loc[2], interface_loc[1], interface_loc[3]))
        if location:
            break
        elif cycles_waiting > max_cycles:
            return 'did not see the bank interface in time'
        else:
            cycles_waiting += 1
        randomSleep(1.0, 1.1)
    return 'success'


def find_contour_center(contour):
    moment_temp = cv2.moments(contour)
    if moment_temp['m00'] != 0:
        cx = int(moment_temp['m10'] / moment_temp['m00'])
        cy = int(moment_temp['m01'] / moment_temp['m00'])
        return [cx, cy]
    else:
        return False


def find_moving_target_with_draw(image):
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
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, 255, 3)

        # find the biggest countour (c) by the area
        # c = max(contours, key = cv2.contourArea)
        distance = 999999999
        closest_coords = [0, 0, 0, 0]
        closest_contour = None
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            # pyautogui.moveTo((x + 805) + 10,(y + 36) + 10)
            # draw the biggest contour (c) in green
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
            current_distance = point_dist(1275, 715, x, y)
            if current_distance < distance:
                closest_coords = [x, y, w, h]
                distance = current_distance
                closest_contour = c
        center = find_contour_center(closest_contour)
        if center:
            cv2.drawContours(output, [closest_contour], -1, (0, 255, 0), 2)
            cv2.circle(output, (center[0], center[1]), 7, (0, 0, 255), -1)
            cv2.putText(output, "center", (center[0] - 20, center[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return np.array(output)


def find_moving_target(image, scouting):
    # failsafe to check if a monster aggro'd me
    did_click = find_click_x(image)
    if did_click:
        print('here1')
        return True
    # cyan color boundaries [B, G, R]
    lower = [0, 255, 255]
    upper = [0, 255, 255]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        # find the biggest contour (c) by the area
        # c = max(contours, key = cv2.contourArea)
        distance = 999999999
        closest_coords = [0, 0, 0, 0]
        closest_contour = None
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            current_distance = point_dist(1275, 715, x, y)
            if current_distance < distance:
                closest_coords = [x, y, w, h]
                distance = current_distance
                closest_contour = c
        center = find_contour_center(closest_contour)
        if center:
            if scouting:
                return True
            else:
                bezierMovement(center[0] - 10, center[0] + 10, center[1] - 10, center[1] + 10)
                pyautogui.click()
                # give the highlight a half second to pop up
                randomSleep(0.5, 0.7)
                # implement red x check ot make sure i clicked
                screen = np.array(ImageGrab.grab())
                did_click = find_click_x(screen)
                if did_click:
                    print('here1')
                    return True
                else:
                    return False
        return False
    return False


def find_fixed_object_while_moving(area, scouting):
    image = np.array(ImageGrab.grab(area))
    # yellow color
    lower = [255, 255, 0]
    upper = [255, 255, 0]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 1:
        if scouting:
            x, y, w, h = cv2.boundingRect(contours[0])
            return [x,y]
        print('found a bank, going to click')
        center = find_contour_center(contours[0])
        if center:
            bezierMovement(center[0] - 10, center[0] + 10, center[1] - 10, center[1] + 10)
            pyautogui.click()
            # give the highlight a half second to pop up
            randomSleep(0.2, 0.3)
            # implement red x check ot make sure i clicked
            screen = np.array(ImageGrab.grab())
            did_click = did_i_click_fixed_obj(screen)
            if did_click:
                print('here1')
                return True
            else:
                return False
        return False
    return False


def find_click_x_with_draw(image):
    # cyan color boundaries [B, G, R]
    lower = [19, 0, 255]
    upper = [19, 0, 255]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, 255, 3)
        center = find_contour_center(contours[0])
        if center:
            cv2.drawContours(output, [contours[0]], -1, (0, 255, 0), 2)
            cv2.circle(output, (center[0], center[1]), 7, (0, 0, 255), -1)
            cv2.putText(output, "center", (center[0] - 20, center[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return np.array(output)


def find_click_x(image):
    # red color boundaries [B, G, R]
    lower = [19, 0, 255]
    upper = [19, 0, 255]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        return True
    return False


def did_i_click_fixed_obj(image):
    # red color boundaries [B, G, R]
    lower = [255, 0, 255]
    upper = [255, 0, 255]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        return True
    return False


def experimental_find_click_x(image):
    # red color boundaries [B, G, R]
    lower = [19, 0, 255]
    upper = [19, 0, 255]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (cv2.__version__[0] > '3'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        center = find_contour_center(contours[0])
        if center:
            return [True, center]
        return True
    return False


def walk_north_minimap():
    bezierMovement(2443, 2462, 43, 64)
    randomSleep(0.1, 0.2)
    pyautogui.click()
    return True


def walk_south_minimap():
    bezierMovement(2446, 2459, 216, 223)
    randomSleep(0.1, 0.2)
    pyautogui.click()
    return True

def look_for_item_in_bag(item):
    is_in_bag = roughImgCompare('..\\screens\\' + item, .8, (2299, 1024, 2510, 1324))
    if is_in_bag:
        return is_in_bag
    else:
        return False


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
                current_distance = point_dist(1275, 715, x, y)
                if current_distance < distance:
                    closest_coords = [x, y, w, h]
                    distance = current_distance
                    closest_contour = c
        if closest_contour is not None:
            center = find_contour_center(closest_contour)
            return [center[0] + x_off, center[1] + y_off]
    return None


def check_health():
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
    img = ImageGrab.grab((2270,  1030,2286, 1044))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    health = pytesseract.image_to_string(img, config='--psm 6 -c tessedit_char_whitelist=0123456789')
    if health:
        try:
            health = int(health)
        except ValueError:
            health = None

    return health


def is_bag_full():
    last_slot_empty = Image.open('..\\screens\\last_slot_empty.png')
    slot_is_empty = roughImgCompare(last_slot_empty, .8, (2299, 1024, 2510, 1324))
    if not slot_is_empty:
        return True
    else:
        return False

