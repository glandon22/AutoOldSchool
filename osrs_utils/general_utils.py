import datetime
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
import ctypes
import keyboard as kb
from secret_keepr import get_config
import requests

mouseeventf_absolute = 0x8000
mouseeventf_leftdown = 0x0002
mouseeventf_leftup = 0x0004
mouseeventf_leftclick = mouseeventf_leftdown + mouseeventf_leftup

# Establish session with my backend server, this cuts latency after the first call from 2 seconds to 1 ms
session = requests.Session()
establish_conn = {
    'helloWorld': True
}
session.get(url='http://localhost:56799/osrs', json=establish_conn)


def point_dist(x1, y1, x2, y2):
    return abs(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def bezier_movement(x_min, y_min, x_max, y_max):
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
    duration = round(random.uniform(min_time, max_time), 6)
    print('Sleeping for ', duration)
    time.sleep(duration)


def rough_img_compare(img, confidence, region):
    while True:
        try:
            loc = pyautogui.locateOnScreen(img, confidence=confidence, region=region)
            if loc:
                return loc
            else:
                return False
        except:
            print('error calling screenshot, retrying.')


def hop_worlds():
    kb.send('alt + shift + x')
    random_sleep(3.3, 3.9)
    if calc_img_diff(pyscreenshot.grab([22, 1212, 590, 1337]), Image.open('..\\screens\\w319.png'), 3) == 'same':
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
    POSE_ANIMATION = {
        'poseAnimation': True
    }
    while True:
        data = query_game_data(POSE_ANIMATION)
        # i am not moving
        if 'poseAnimation' in data and data['poseAnimation'] == 808:
            break
        else:
            random_sleep(0.1, 0.2)


def type_something(phrase):
    keyboard.write(phrase)


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


def antiban_rest(short=10, med=25, long=75):
    if random.randint(0, short) == 1:
        print('Taking a short break.')
        random_sleep(5.1, 6.8)
    elif random.randint(0, med) == 1:
        print('Taking a medium break.')
        random_sleep(27.2, 39.9)
    elif random.randint(0, long) == 1:
        print('Taking a long break.')
        random_sleep(64.5, 83.9)


def get_player_info(port=1488):
    import socket
    import re
    import json

    host = 'localhost'
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host, port))
    socket.listen(1)
    conn, addr = socket.accept()
    data = bytearray()
    while True:
        data.extend(conn.recv(1024))
        try:
            decoded = data.decode('utf-8')
            body = re.split(r"\s(?=[{\[])", decoded)[-1]
            parsed = json.loads(body)
            # print(json.dumps(parsed, sort_keys=True, indent=4))
            return parsed
        except ValueError:
            continue
    conn.close()


def move_and_click(x, y, w, h, button='left'):
    bezier_movement(x - w, y - h, x + w, y + h)
    random_sleep(0.15, 0.25)
    pyautogui.click() if button == 'left' else pyautogui.click(button='right')
    random_sleep(0.15, 0.25)


def click_off_screen(x1=3000, x2=3100, y1=100, y2=200, click=True):
    bezier_movement(x1, y1, x2, y2)
    random_sleep(0.15, 0.25)
    if click:
        pyautogui.click()
        random_sleep(0.15, 0.25)


def move_around_center_screen(x1=800, y1=400, x2=1000, y2=600):
    bezier_movement(x1, y1, x2, y2)
    random_sleep(0.15, 0.25)


def power_drop(inv, slots_to_skip, items_to_drop):
    patterns = [
        [
            0, 1, 2, 3,
            7, 6, 5, 4,
            8, 9, 10, 11,
            15, 14, 13, 12,
            16, 17, 18, 19,
            23, 22, 21, 20,
            24, 25, 26, 27
        ],
        [
            0, 4, 8, 12, 16, 20, 24,
            25, 21, 17, 13, 9, 5, 1,
            2, 6, 10, 14, 18, 22, 26,
            27, 23, 19, 15, 11, 7, 3
        ],
        [
            0, 4, 5, 1,
            2, 3, 7, 6,
            11, 10, 9, 8,
            12, 16, 20, 24,
            25, 21, 17, 13,
            14, 15, 19, 18,
            22, 23, 27, 26
        ],
        [
            3, 7, 11, 15,
            19, 23, 27, 26,
            25, 24, 20, 21,
            22, 18, 17, 16,
            12, 13, 14, 10,
            6, 2, 1, 5,
            9, 8, 4, 0
        ]
    ]
    pattern = random.randint(0, len(patterns * 2) - 1)
    # reverse the array
    if pattern >= len(patterns):
        pattern = patterns[math.floor(pattern / 2)]
        pattern = pattern[::-1]
        print('here', pattern)
    else:
        pattern = patterns[pattern]
    for num in pattern:
        # dont drop whatever is in this slot
        if len(slots_to_skip) != 0 and num in slots_to_skip:
            continue
        # make sure slot is in range
        elif num > len(inv):
            continue
        # dont drop this item type
        elif inv[num]["id"] in items_to_drop:
            move_and_click(inv[num]["x"], inv[num]["y"], 5, 5)


def check_and_dismiss_random(random_data):
    print('d', random_data)
    if len(random_data) == 0:
        return 'no randoms'
    move_and_click(math.floor(random_data[0]['x']), math.floor(random_data[0]['y']), 7, 7, 'right')
    random_sleep(1, 1.1)
    dismiss = rough_img_compare('..\\screens\\dismiss.png', .9, (0, 0, 1920, 1080))
    if dismiss:
        move_and_click(int(dismiss[0]), int(dismiss[1]), 4, 4)
        return 'success'
    else:
        return 'didnt find the dismiss option'


# check if one particular item is in inventory
def is_item_in_inventory(inv, item_to_find):
    if not inv:
        return False
    for item in inv:
        if item['id'] == item_to_find:
            return [item['x'], item['y']]
    return False


# check for presence of one of multiple items
# this is useful for supporting multiple food types in combat
# if you don't care which food is consumed
def are_items_in_inventory(inv, items_to_find):
    if not inv:
        return False
    for item in inv:
        if item['id'] in items_to_find:
            return [item['x'], item['y']]
    return False


# Get screen size
def _size():
    return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)


def _send_mouse_event(ev, x, y, dw_data=0):
    width, height = _size()

    converted_x = 65536 * x // width + 1
    converted_y = 65536 * y // height + 1
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.01)
    ctypes.windll.user32.mouse_event(ev, ctypes.c_long(converted_x), ctypes.c_long(converted_y), dw_data, 0)


def quick_click(x, y):
    _send_mouse_event(mouseeventf_leftclick, x, y)


def find_closest_npc(npcs, ignore=-1):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for npc in npcs:
        if npc['id'] != ignore and npc["dist"] < closest["dist"]:
            closest = {
                "dist": npc["dist"],
                "x": math.floor(npc["x"]),
                "y": math.floor(npc["y"]),
                "id": npc["id"]
            }
    return closest


def find_closest_target(targs):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for targ in targs:
        if targ["dist"] < closest["dist"]:
            closest = {
                "dist": targ["dist"],
                "x": math.floor(targ["x"]),
                "y": math.floor(targ["y"]),
            }
    return closest

def break_every_hour(max_run, start_time=-1):
    if start_time == -1:
        start_time = datetime.datetime.now()
    random_sleep(0.5, 0.9)
    run_time = (datetime.datetime.now() - start_time).total_seconds()
    print('Current Script Runtime: ', run_time, '. Maximum Script Runtime: ', max_run * 60)
    if run_time > max_run * 60:
        return True
    else:
        return False


def logout():
    LOGOUT_ICON = {
        'widget': '161,52'
    }
    LOGOUT_BUTTON = {
        'widget': '182,12'
    }
    WORLD_SWITCHER_LOGOUT = {
        'widget': '69,23'
    }
    icon = query_game_data(LOGOUT_ICON)
    move_and_click(icon['widget']['x'], icon['widget']['y'], 10, 10)
    random_sleep(1, 1.4)
    logout_button = query_game_data(LOGOUT_BUTTON)
    if 'widget' in logout_button:
        move_and_click(logout_button['widget']['x'], logout_button['widget']['y'], 10, 10)
        random_sleep(0.3, 0.4)
    else:
        logout_button = query_game_data(WORLD_SWITCHER_LOGOUT)
        move_and_click(logout_button['widget']['x'], logout_button['widget']['y'], 10, 10)
        random_sleep(0.3, 0.4)


def login(password):
    existing_user = rough_img_compare('C:\\Users\\gland\\osrs_yolov3\\screens\\existing_user.png', 0.8, (0, 0, 1920, 1080))
    while True:
        existing_user = rough_img_compare('C:\\Users\\gland\\osrs_yolov3\\screens\\existing_user.png', 0.8, (0, 0, 1920, 1080))
        if existing_user:
            break
        time.sleep(1)
    move_and_click(
        existing_user[0] + math.floor(existing_user[2] / 4),
        existing_user[1] + math.floor(existing_user[3] / 4),
        math.floor(existing_user[2] / 4),
        math.floor(existing_user[3] / 4)
    )
    random_sleep(1, 2)
    type_something(get_config(password))
    random_sleep(0.2, 0.4)
    login_button = rough_img_compare('C:\\Users\\gland\\osrs_yolov3\\screens\\login_button.png', 0.8, (0, 0, 1920, 1080))
    while True:
        login_button = rough_img_compare('C:\\Users\\gland\\osrs_yolov3\\screens\\login_button.png', 0.8, (0, 0, 1920, 1080))
        if login_button:
            break
        time.sleep(1)
    move_and_click(
        login_button[0] + math.floor(login_button[2] / 4),
        login_button[1] + math.floor(login_button[3] / 4),
        math.floor(login_button[2] / 4),
        math.floor(login_button[3] / 4)
    )

    coords = {
        'x': 0,
        'y': 0
    }

    while True:
        q = {
            'clickToPlay':  True
        }
        r = query_game_data(q)
        if 'clickToPlay' in r:
            ctp = r['clickToPlay']
            # once the click to play button is loaded, it takes a couple seconds to get accurate coords
            # due to some underlying game mechanics (i guess)
            if ctp['x'] == coords['x'] and ctp['y'] == coords['y']:
                move_and_click(r['clickToPlay']['x'], r['clickToPlay']['y'], 15, 15)
                break
            else:
                coords['x'] = ctp['x']
                coords['y'] = ctp['y']
        random_sleep(0.6, 0.7)


def dump_items_in_bank():
    # wait for interface and withdraw item
    while True:
        loc = rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
        if loc:
            loc = rough_img_compare('..\\screens\\dump.png', .9, (0, 0, 1920, 1080))
            move_and_click(loc[0] + 15, loc[1] + 15, 4, 4)
            random_sleep(.5, .6)
            keyboard.send('esc')
            random_sleep(.5, .6)
            break


def break_manager(start_time, min_session, max_session, min_rest, max_rest, password, post_login_steps):
    take_break = break_every_hour(random.randint(min_session, max_session), start_time)
    if take_break:
        print('Taking extended break, signing off.')
        logout()
        break_start_time = datetime.datetime.now()
        while (datetime.datetime.now() - break_start_time).total_seconds() < random.randint(min_rest, max_rest):
            print(
                'Break has currently run for: ',
                (datetime.datetime.now() - break_start_time).total_seconds(),
                ' and can run for up to: ',
                max_rest
            )
            time.sleep(30)
            click_off_screen()
        login(password)
        random_sleep(0.4, 0.5)
        if post_login_steps:
            post_login_steps()
        return datetime.datetime.now()
    return start_time


def query_game_data(q):
    while True:
        try:
            r = session.get(url='http://localhost:56799/osrs', json=q)
            return r.json()
        except:
            print('Got an error trying to query the db.')

def deposit_box_dump_inv():
    q = {
        'widget': '192,5'
    }
    # wait to first see the button,
    # since there is a lag from its first appearance
    # to actually being on screen in the correct location
    while True:
        data = query_game_data(q)
        if 'widget' in data:
            break
    random_sleep(0.5, 0.61)
    while True:
        data = query_game_data(q)
        if 'widget' in data:
            move_and_click(data['widget']['x'], data['widget']['y'], 6, 6)
            break
    keyboard.send('esc')

