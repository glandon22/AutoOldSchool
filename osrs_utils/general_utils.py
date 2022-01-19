# chat box coords
# im = ImageGrab.grab([2,1190,645,1350])

# inv coords
# im = ImageGrab.grab([2299, 1024, 2510, 1324])
import keyboard
import numpy as np
import time
from scipy import interpolate
import math
import random
import pyautogui
from PIL import Image, ImageChops
import pyscreenshot
import operator
from functools import reduce
import cv2
import keyboard as kb
import pytesseract


def point_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def bezier_movement(x_min, x_max, y_min, y_max):
    # Any duration less than this is rounded to 0.0 to instantly move the mouse.
    pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
    # Minimal number of seconds to sleep between mouse moves.
    pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
    # The number of seconds to pause after EVERY public function call.
    pyautogui.PAUSE = 0  # Default: 0.1
    cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
    x1, y1 = pyautogui.position()
    x2 = random.randint(x_min, x_max)
    y2 = random.randint(y_min, y_max)
    print('clicking ', x2, y2)
    # Distribute control points between start and destination evenly.
    x = np.linspace(x1, x2, num=cp, dtype='int')
    y = np.linspace(y1, y2, num=cp, dtype='int')

    # Randomise inner points a bit (+-RND at most).
    rnd = random.randint(9, 11)
    xr = [random.randint(-rnd, rnd) for _ in range(cp)]
    yr = [random.randint(-rnd, rnd) for _ in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr

    print('x,y', x, y)
    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
    # Must be less than number of control points.
    tck, u = [None, None]
    try:
        # noinspection PyTupleAssignmentBalance
        tck, u = interpolate.splprep([x, y], k=degree)
    except ValueError:
        print('bezier movement blew up')
        pyautogui.moveTo(x2, y2)
        return [x2, y2]
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


def calc_img_diff(im1, im2, acceptable_diff):
    image_difference = ImageChops.difference(im1, im2).histogram()
    diff = math.sqrt(reduce(operator.add,
                            map(lambda h, i: h * (i ** 2), image_difference, range(256))
                            ) / (float(im1.size[0]) * im2.size[1]))
    if diff > acceptable_diff:
        return 'different'
    else:
        return 'same'


def random_sleep(min_time, max_time):
    duration = round(random.uniform(min_time, max_time), 3)
    print("Sleeping for ", duration, ' seconds')
    time.sleep(duration)


def show_inv_coords(slot):
    inv_coords = [
        [2317, 2343, 1030, 1056], [2371, 2395, 1034, 1058], [2424, 2448, 1034, 1060], [2476, 2500, 1036, 1058],
        [2320, 2344, 1082, 1103], [2372, 2394, 1082, 1102], [2425, 2448, 1082, 1100], [2478, 2499, 1082, 1102],
        [2320, 2340, 1128, 1144], [2372, 2395, 1126, 1146], [2422, 2446, 1126, 1144], [2476, 2500, 1127, 1142],
        [2323, 2340, 1168, 1190], [2372, 2396, 1172, 1192], [2424, 2446, 1174, 1192], [2478, 2503, 1173, 1190],
        [2320, 2342, 1216, 1238], [2374, 2394, 1215, 1238], [2425, 2447, 1216, 1233], [2479, 2500, 1220, 1238],
        [2320, 2342, 1259, 1282], [2372, 2394, 1261, 1280], [2425, 2446, 1262, 1280], [2478, 2500, 1261, 1280],
        [2319, 2342, 1305, 1326], [2370, 2393, 1306, 1322], [2426, 2445, 1306, 1324], [2476, 2500, 1304, 1324]
    ]
    return [inv_coords[slot][0], inv_coords[slot][2], inv_coords[slot][1], inv_coords[slot][3],]


def rough_img_compare(img, confidence, region):
    loc = pyautogui.locateOnScreen(img, confidence=confidence, region=region)
    if loc:
        return loc
    else:
        return False


def did_level():
    status = rough_img_compare('..\\screens\\level.png', .8, (2, 645, 1190, 1350))
    if status:
        return True
    else:
        return False


def dump_bag():
    location = rough_img_compare('..\\screens\\dump.png', .8, (0, 0, 2559, 1439))
    if not location:
        return False
    bezier_movement(location[0], location[0] + 5, location[1], location[1] + 5)
    random_sleep(0.2, 0.3)
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
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        closest_contour = find_closest_contour(contours)
        center = find_contour_center(closest_contour)
        bezier_movement(center[0] - 3, center[0] + 3, center[1] - 3, center[1] + 3)
        random_sleep(0.2, 0.3)
        pyautogui.click()
        return True
    return False


def go_to_target(targ_area):
    attempts = 0
    while True:
        print(attempts)
        screen = np.array(pyscreenshot.grab(targ_area))
        did_i_find = find_fixed_object(screen, targ_area[0], targ_area[1])
        if did_i_find:
            random_sleep(0.5, 0.7)
            return True
        elif attempts > 10:
            print('exiting, was unable to find target')
            return False
        else:
            attempts += 1


def withdraw_items_from_bank(items, bank_interface):
    for item in items:
        targ = rough_img_compare('..\\screens\\' + item, .75,
                                             (bank_interface[0], bank_interface[2], bank_interface[1],
                                              bank_interface[3]))
        if targ:
            print('taking ', item, ' from the bank')
            bezier_movement(targ[0], targ[0] + 6, targ[1], targ[1] + 6)
            random_sleep(0.3, 0.4)
            print('clicking')
            pyautogui.click()
        else:
            return 'unable to find any more ' + item
    return 'success'


def process_with_tool(slot, button, expected_last_slot, max_cycles):
    # click on knife
    bezier_movement(2317, 2343, 1030, 1056)
    pyautogui.click()
    random_sleep(0.2, 0.5)
    # click on log
    if slot == 1:
        bezier_movement(2371, 2395, 1034, 1058)
    else:
        bezier_movement(2476, 2500, 1304, 1324)
    pyautogui.click()
    random_sleep(1.2, 1.7)
    pyautogui.press(button)
    random_sleep(0.3, 0.7)
    # move off-screen
    bezier_movement(3500, 4000, 0, 250)
    random_sleep(0.4, 0.7)
    pyautogui.click()
    cycles_waiting = 0
    while True:
        last_slot = calc_img_diff(Image.open(expected_last_slot), pyscreenshot.grab([2476, 1304, 2500, 1324]), 3)
        if last_slot == 'same':
            break
        elif did_level():
            restart = process_with_tool(27, button, expected_last_slot, max_cycles)
            if restart != 'success':
                return 'after leveling, did not successfully finish processing'
        elif cycles_waiting > max_cycles:
            return 'did not finishing processing in acceptable number of cycles'
        else:
            cycles_waiting += 1
        random_sleep(1.4, 2.6)
    return 'success'


def hop_worlds():
    kb.send('alt + shift + x')
    random_sleep(3.3, 3.9)
    if calc_img_diff(pyscreenshot.grab([22, 1212, 590, 1337]), Image.open('.\\screens\\w319.png'), 3) == 'same':
        print('hopping to world 319')
        kb.send('space')
        random_sleep(0.7, 0.9)
        kb.send('2')
    post_hop = Image.open('..\\screens\\post_hop.png')
    cycles_waiting = 0
    while True:
        if rough_img_compare(post_hop, .8, (2270, 971, 2546, 1382)):
            break
        elif cycles_waiting > 1000:
            return 'failed to hop worlds'
        else:
            cycles_waiting += 1
        random_sleep(0.2, 0.5)
    print('hitting esc')
    kb.send('esc')
    random_sleep(0.2, 0.4)
    return 'success'


def find_fixed_npc(box, x_offset, y_offset):
    image = np.array(pyscreenshot.grab(bbox=box))
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
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        # this movement must also account for the offset of the target area bbox, i.e. the image coordinates passed
        # to the findFixedObject function
        bezier_movement(x + x_offset + (math.floor(w / 2)), x + x_offset + (math.floor(w / 2)),
                        y + y_offset + math.floor(h / 2), y + y_offset + math.floor(h / 2))
        random_sleep(0.1, 0.3)
        pyautogui.click()
        return True
    return False


def wait_for_bank_interface(interface_loc, max_cycles):
    cycles_waiting = 0
    while True:
        location = rough_img_compare('..\\screens\\dump.png', .8,
                                                 (interface_loc[0], interface_loc[2], interface_loc[1],
                                                  interface_loc[3]))
        if location:
            break
        elif cycles_waiting > max_cycles:
            return 'did not see the bank interface in time'
        else:
            cycles_waiting += 1
        random_sleep(1.0, 1.1)
    return 'success'


def find_contour_center(contour):
    moment_temp = cv2.moments(contour)
    if moment_temp['m00'] != 0:
        cx = int(moment_temp['m10'] / moment_temp['m00'])
        cy = int(moment_temp['m01'] / moment_temp['m00'])
        return [cx, cy]
    else:
        return False


def find_closest_contour(contours):
    # find the biggest contour (c) by the area
    # c = max(contours, key = cv2.contourArea)
    distance = 999999999
    closest_coords = [0, 0, 0, 0]
    closest_contour = None
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        # pyautogui.moveTo((x + 805) + 10,(y + 36) + 10)
        # draw the biggest contour (c) in green
        current_distance = point_dist(1275, 715, x, y)
        if current_distance < distance:
            closest_coords = [x, y, w, h]
            distance = current_distance
            closest_contour = c
    return closest_contour


def find_closest_contour_draw(contours, output):
    # find the biggest contour (c) by the area
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
    return closest_contour, output


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
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, 255, 3)

        closest_contour, output = find_closest_contour_draw(contours, output)
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
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
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
                bezier_movement(center[0] - 10, center[0] + 10, center[1] - 10, center[1] + 10)
                pyautogui.click()
                # give the highlight a half second to pop up
                random_sleep(0.5, 0.7)
                # implement red x check ot make sure i clicked
                screen = np.array(pyscreenshot.grab())
                did_click = find_click_x(screen)
                if did_click:
                    print('here1')
                    return True
                else:
                    return False
        return False
    return False


def find_fixed_object_while_moving(area, scouting):
    image = np.array(pyscreenshot.grab(area))
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
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 1:
        if scouting:
            x, y, w, h = cv2.boundingRect(contours[0])
            return [x, y]
        print('found a bank, going to click')
        center = find_contour_center(contours[0])
        if center:
            bezier_movement(center[0] - 2, center[0] + 2, center[1] - 2, center[1] + 2)
            pyautogui.click()
            # give the highlight a half second to pop up
            random_sleep(0.2, 0.3)
            # implement red x check ot make sure i clicked
            screen = np.array(pyscreenshot.grab())
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
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
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
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
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
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        return True
    return False


def walk_north_minimap():
    bezier_movement(2443, 2462, 43, 64)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    return True


def walk_south_minimap():
    bezier_movement(2446, 2459, 216, 223)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    return True


def look_for_item_in_bag(item):
    is_in_bag = rough_img_compare('..\\screens\\' + item, .8, (2299, 1024, 2510, 1324))
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
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        # find all contours that look like highlighted tiles
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
    img = pyscreenshot.grab((2270, 1030, 2286, 1044))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    health = pytesseract.image_to_string(img, config='--psm 6 -c tessedit_char_whitelist=0123456789')
    if health:
        try:
            health = int(health)
        except ValueError:
            health = None

    return health


def is_bag_full():
    # loop backwards
    for slot in range(27, -1, -1):
        if calc_img_diff(
                pyscreenshot.grab(show_inv_coords(slot)),
                Image.open('..\\screens\\empty_bag\\slot' + str(slot) + '.png'),
                3
        ) == 'same':
            return False
    return True



def walking_with_full_run_energy():
    full_run = Image.open('..\\screens\\run_energy.png')
    run_energy = rough_img_compare(full_run, .8, (2276, 32, 2548, 273))
    print('run: ', run_energy)
    if run_energy:
        bezier_movement(run_energy[0] - 2, run_energy[0] + 2, run_energy[1] - 2, run_energy[1] + 2)
        random_sleep(0.1, 0.2)
        pyautogui.click()
    else:
        return False


def solve_bank_pin():
    for i in range(4):
        num = None
        if i == 0 or i == 3:
            num = '8'
        else:
            num = '7'

        loc = rough_img_compare('..\\screens\\bank_pin_' + num + '.png', .8, [641, 306, 1648, 1008])
        if loc:
            bezier_movement(loc[0], loc[0] + 1, loc[1], loc[1] + 1)
            random_sleep(0.2, 0.3)
            pyautogui.click()
            random_sleep(0.2, 0.3)
            bezier_movement(1200, 1700, 12, 209)
        else:
            return 'couldnt find ' + num
        random_sleep(1.1, 1.2)


def wait_until_stationary():
    cycles = 0
    same_frame_count = 0
    prev_img = pyscreenshot.grab((2082, 36, 2238, 100))
    time.sleep(.5)
    while True:
        print('running', same_frame_count)
        curr_img = pyscreenshot.grab((2082, 36, 2238, 100))
        player_loc = calc_img_diff(prev_img, curr_img, 3)
        if player_loc == 'same' and same_frame_count > 8:
            return 'success'
        elif player_loc == 'same':
            same_frame_count += 1
            print('frame count', same_frame_count)
            continue
        elif cycles > 1500:
            return 'never stopped moving'
        cycles += 1
        same_frame_count = 0
        prev_img = curr_img


def find_moving_target_no_verify(image):
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
    # noinspection PyUnresolvedReferences
    if cv2.__version__[0] > '3':
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        print('here')
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
            print('here')
            bezier_movement(center[0] - 3, center[0] + 3, center[1] - 3, center[1] + 3)
            pyautogui.click()
            return True
        return False
    return False


def change_npc_highlights(npc):
    bezier_movement(2444, 2453, 8, 17)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    bezier_movement(2278, 2337, 54, 68)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    keyboard.send('ctrl + a')
    keyboard.send('del')
    type_something('npc indi')
    bezier_movement(2452, 2458, 108, 114)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    bezier_movement(2232, 2286, 452, 464)
    random_sleep(0.2, 0.3)
    pyautogui.click()
    keyboard.send('ctrl + a')
    keyboard.send('del')
    type_something(npc)
    bezier_movement(2229, 2240, 45, 56)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    bezier_movement(2444, 2453, 8, 17)
    random_sleep(0.1, 0.2)
    pyautogui.click()


def type_something(phrase):
    for char in phrase:
        keyboard.send(char)
        random_sleep(0.1, 0.2)


def change_fishing_settings():
    bezier_movement(2444, 2453, 8, 17)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    bezier_movement(2278, 2337, 54, 68)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    keyboard.send('ctrl + a')
    keyboard.send('del')
    type_something('fishing')
    bezier_movement(2452, 2458, 108, 114)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    bezier_movement(2477, 2486, 135, 142)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    bezier_movement(2479, 2488, 174, 178)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    bezier_movement(2230, 2239, 46, 54)
    random_sleep(0.1, 0.2)
    pyautogui.click()
    bezier_movement(2444, 2453, 8, 17)
    random_sleep(0.1, 0.2)
    pyautogui.click()

def click_inv_slot(slot):
    slot = show_inv_coords(slot)
    bezier_movement(slot[0], slot[2], slot[1], slot[3])
    random_sleep(0.2, 0.3)
    pyautogui.click()

