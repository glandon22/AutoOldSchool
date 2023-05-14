import datetime
import numpy as np
import time
from scipy import interpolate
import math
import random
import pyautogui
from PIL import ImageChops
import operator
from functools import reduce
import ctypes
from secret_keepr import get_config
import requests
from pynput.keyboard import Key, Controller
import platform

keyboard = Controller()
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
        print(point[0])
        if point[0] > 1920 or point[0] < 0 or point[1] < 20 or point[1] > 1040:
            print('point: {} out of bounds, rejecting movement request.'.format(point))
            return False
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
        except Exception as e:
            print('error calling screenshot, retrying.', e)


'''def hop_worlds():
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
'''


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


def wait_until_stationary(port='56799'):
    POSE_ANIMATION = {
        'poseAnimation': True
    }
    while True:
        data = query_game_data(POSE_ANIMATION, port)
        # i am not moving
        if 'poseAnimation' in data and (data['poseAnimation'] == 808 or data['poseAnimation'] == 813 or data['poseAnimation'] == 4591):
            break
        else:
            random_sleep(0.1, 0.2)


def am_stationary(port='56799'):
    POSE_ANIMATION = {
        'poseAnimation': True
    }
    data = query_game_data(POSE_ANIMATION, port)
    if 'poseAnimation' in data and data['poseAnimation'] == 808:
        return True
    else:
        return False


def type_something(phrase):
    keyboard.type(phrase)


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
    movement = bezier_movement(x - w, y - h, x + w, y + h)
    random_sleep(0.15, 0.25)
    curr_pos = pyautogui.position()
    print('pos', curr_pos, curr_pos[1])
    # DO NOT CLICK ON THE TASK BAR
    if not movement:
        print('movement was unsuccessful, target was off screen. Rejecting click.')
        return
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
        elif num >= len(inv):
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


# check if one particular item is in inventory
def is_item_in_inventory_v2(inv, item_to_find):
    if not inv:
        return False
    for item in inv:
        if item['id'] == int(item_to_find):
            return item
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


def are_items_in_inventory_v2(inv, items_to_find):
    if not inv:
        return False
    for item in inv:
        if item['id'] in items_to_find:
            return item
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


def find_an_npc(npcs, min_dist):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for npc in npcs:
        if closest["dist"] > npc["dist"] >= min_dist:
            closest = {
                "dist": npc["dist"],
                "x": math.floor(npc["x"]),
                "y": math.floor(npc["y"]),
                "id": npc["id"]
            }
    if closest['x'] is None:
        return False
    else:
        return closest


def find_closest_target(targs):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for targ in targs:
        if int(targ["dist"]) < int(closest["dist"]):
            closest = targ
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


def logout(port='56799'):
    LOGOUT_ICON = {
        'widget': '161,52'
    }
    LOGOUT_BUTTON = {
        'widget': '182,12'
    }
    WORLD_SWITCHER_LOGOUT = {
        'widget': '69,23'
    }
    icon = query_game_data(LOGOUT_ICON, port)
    move_and_click(icon['widget']['x'], icon['widget']['y'], 10, 10)
    random_sleep(1, 1.4)
    logout_button = query_game_data(LOGOUT_BUTTON, port)
    if 'widget' in logout_button:
        move_and_click(logout_button['widget']['x'], logout_button['widget']['y'], 10, 10)
        random_sleep(0.3, 0.4)
    else:
        logout_button = query_game_data(WORLD_SWITCHER_LOGOUT, port)
        move_and_click(logout_button['widget']['x'], logout_button['widget']['y'], 10, 10)
        random_sleep(0.3, 0.4)


def login(password, port='56799'):
    existing_user_paths = {
        'Linux': '../screens/existing_user.png',
        'Windows': 'C:\\Users\\gland\\osrs_yolov3\\screens\\existing_user.png'
    }
    login_paths = {
        'Linux': '../screens/login.png',
        'Windows': 'C:\\Users\\gland\\osrs_yolov3\\screens\\login_button.png'
    }
    existing_user = rough_img_compare(existing_user_paths[platform.system()], 0.8,
                                      (0, 0, 1920, 1080))
    while True:
        existing_user = rough_img_compare(existing_user_paths[platform.system()], 0.8,
                                          (0, 0, 1920, 1080))
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
    login_button = rough_img_compare(login_paths[platform.system()], 0.8,
                                     (0, 0, 1920, 1080))
    while True:
        login_button = rough_img_compare(login_paths[platform.system()], 0.8,
                                         (0, 0, 1920, 1080))
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
            'widget': '378,72'
        }
        widget = query_game_data(q, port)
        if 'widget' in widget:
            ctp = widget['widget']
            # once the click to play button is loaded, it takes a couple seconds to get accurate coords
            # due to some underlying game mechanics (i guess)
            if ctp['x'] == coords['x'] and ctp['y'] == coords['y']:
                move_and_click(ctp['x'], ctp['y'], 15, 15)
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
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            random_sleep(.5, .6)
            break


def break_manager(start_time, min_session, max_session, min_rest, max_rest, password, post_login_steps=None, port='56799', pre_logout_steps=None):
    take_break = break_every_hour(random.randint(min_session, max_session), start_time)
    if take_break:
        print('Taking extended break, signing off.')
        if pre_logout_steps:
            pre_logout_steps()
        random_sleep(20, 30)
        logout(port)
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
        login(password, port)
        random_sleep(0.4, 0.5)
        if post_login_steps:
            post_login_steps()
        return datetime.datetime.now()
    return start_time


def multi_break_manager(start_time, min_session, max_session, min_rest, max_rest, acc_configs):
    take_break = break_every_hour(random.randint(min_session, max_session), start_time)
    if take_break:
        print('Taking extended break, signing off. Current time: ', datetime.datetime.now())
        random_sleep(20, 30)
        for acc in acc_configs:
            print(acc)
            logout(acc['port'])
            random_sleep(3, 3.1)
            if len(acc_configs) > 1:
                with keyboard.pressed(Key.alt):
                    keyboard.press(Key.tab)
                    keyboard.release(Key.tab)
        break_start_time = datetime.datetime.now()
        while (datetime.datetime.now() - break_start_time).total_seconds() < random.randint(min_rest, max_rest):
            print(
                'Break has currently run for: ',
                (datetime.datetime.now() - break_start_time).total_seconds(),
                ' and can run for up to: ',
                max_rest
            )
            time.sleep(30)
            click_off_screen(200, 250, 200, 250)
        for acc in acc_configs:
            login(acc['password'], acc['port'])
            if len(acc_configs) > 1:
                with keyboard.pressed(Key.alt):
                    keyboard.press(Key.tab)
                    keyboard.release(Key.tab)
            random_sleep(3, 3.1)
        random_sleep(0.4, 0.5)
        for acc in acc_configs:
            if acc['post_login_steps']:
                acc['post_login_steps']()
                if len(acc_configs) > 1:
                    with keyboard.pressed(Key.alt):
                        keyboard.press(Key.tab)
                        keyboard.release(Key.tab)
                random_sleep(3, 3.1)
        return datetime.datetime.now()
    return start_time


def query_game_data(q, port='56799'):
    while True:
        try:
            r = session.get(url='http://localhost:{}/osrs'.format(port), json=q)
            return r.json()
        except Exception as e:
            print('Got an error trying to query the db: ', e)


def sleep_one_tick():
    random_sleep(0.6, 0.7)


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
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)


#  this call occasionally fails on the backend, so if we know there should be something in inventory,
#  retry until its returned
def get_inv(port='56799', reject_empty=True):
    while True:
        q = {
            'inv': True
        }
        data = query_game_data(q, port)
        if 'inv' in data:
            if len(data['inv']) > 0 or not reject_empty:
                return data['inv']


def get_game_object(tile, obj, port='56799'):
    """

    :param tile: string
    :param obj: string
    :param port: string
    :return: {'x': 1088, 'y': 572, 'dist': 1, 'x_coord': 2197, 'y_coord': 2792}
    """
    q = {
        'gameObjects': [
            {
                'tile': tile,
                'object': obj
            }
        ]
    }
    data = query_game_data(q, port)
    if 'gameObjects' in data and obj in data['gameObjects']:
        return data['gameObjects'][obj]
    else:
        return False


def get_wall_object(tile, obj, port='56799'):
    q = {
        'wallObjects': [
            {
                'tile': tile,
                'object': obj
            }
        ]
    }
    data = query_game_data(q, port)
    if 'wallObjects' in data and obj in data['wallObjects']:
        return data['wallObjects'][obj][0]
    else:
        return False


def get_ground_object(tile, obj, port='56799'):
    q = {
        'groundObjects': [
            {
                'tile': tile,
                'object': obj
            }
        ]
    }
    data = query_game_data(q, port)
    if 'groundObjects' in data and obj in data['groundObjects']:
        return data['groundObjects'][obj]
    else:
        return False


def get_game_objects(lookup, port='56799'):
    q = {
        'gameObjects': lookup
    }
    data = query_game_data(q, port)
    if 'gameObjects' in data:
        return data['gameObjects']
    else:
        return False


def get_widget(widget_string, port='56799'):
    q = {
        'widget': widget_string
    }
    data = query_game_data(q, port)
    if 'widget' in data:
        return data['widget']
    else:
        return False


def wait_for_bank_interface(port='56799'):
    q = {
        'dumpInvButton': True
    }
    while True:
        data = query_game_data(q, port)
        if 'dumpInvButton' in data:
            random_sleep(0.9, 0.8)
            return


def bank_dump_inv(port='56799'):
    q = {
        'dumpInvButton': True
    }
    while True:
        data = query_game_data(q, port)
        if 'dumpInvButton' in data:
            move_and_click(data['dumpInvButton']['x'], data['dumpInvButton']['y'], 3, 4)
            break


def find_item_in_bank(item_to_find, port='56799'):
    q = {
        'bank': True
    }
    while True:
        data = query_game_data(q, port)
        if 'bankItems' in data:
            for item in data['bankItems']:
                if item['id'] == item_to_find:
                    return item
            return False


def get_world_location(port='56799'):
    """

    :param port:
    :return: {'x': 2638, 'y': 2653, 'z': 0}
    """
    q = {
        'playerWorldPoint': True
    }
    while True:
        data = query_game_data(q, port)
        if 'playerWorldPoint' in data:
            return data['playerWorldPoint']


def get_bank_data(port='56799'):
    q = {
        'bank': True
    }
    while True:
        data = query_game_data(q, port)
        if 'bankItems' in data:
            return data['bankItems']


def get_skill_data(skill, port='56799'):
    """

    :param skill:
    :return:
    {'level': 98, 'xp': 12164703, 'boostedLevel': 98}
    """
    while True:
        q = {
            'skills': [skill]
        }
        skill_data = query_game_data(q, port)
        if 'skills' in skill_data and skill in skill_data['skills']:
            return skill_data['skills'][skill]


def generate_surrounding_tiles(dist, port='56799'):
    player_loc = get_world_location(port)
    tiles = []
    for x in range(player_loc['x'] - dist, player_loc['x'] + dist):
        for y in range(player_loc['y'] - dist, player_loc['y'] + dist):
            tiles.append('{},{},{}'.format(x, y, player_loc['z']))
    return tiles


def generate_game_tiles_in_coords(x_min, x_max, y_min, y_max, z, port='56799'):
    tiles = []
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            tiles.append('{},{},{}'.format(x, y, z))
    return tiles


# t bow 20997
def get_ground_items_in_coords(x_min, x_max, y_min, y_max, z, items, port='56799'):
    tiles = generate_game_tiles_in_coords(x_min, x_max, y_min, y_max, z,)
    q = {
        'groundItems': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['groundItems'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'groundItems' in data:
        return data['groundItems']


def handle_marks(x_min, x_max, y_min, y_max, z, port):
    retries = 0
    while retries < random.randint(3, 8):
        marks = get_ground_items_in_coords(x_min, x_max, y_min, y_max, z, ['11849'], port)
        if '11849' in marks:
            loc = get_world_location(port)
            if 'x' in loc and x_min <= loc['x'] <= x_max and y_min <= loc['y'] <= y_max and loc['z'] == z:
                move_and_click(marks['11849'][0]['x'], marks['11849'][0]['y'], 2, 3)
                random_sleep(0.5, 0.6)
                wait_until_stationary()
                retries += 1
            else:
                break
        else:
            break


# t bow 20997
def get_surrounding_ground_items(dist, items, port='56799'):
    tiles = generate_surrounding_tiles(dist)
    q = {
        'groundItems': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['groundItems'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'groundItems' in data:
        return data['groundItems']


# t bow 20997
def get_surrounding_game_objects(dist, items, port='56799'):
    """

    :param dist: integer, how many tiles around to look for items, ie 7x7
    :param items: array of strings of item codes to search for
    :param port: default is 56799
    :return: {'9345': {'x': 881, 'y': 538, 'dist': 1}}
    """
    tiles = generate_surrounding_tiles(dist, port)
    q = {
        'gameObjects': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['gameObjects'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'gameObjects' in data:
        return data['gameObjects']

# t bow 20997
def get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, items, port='56799'):
    """

    :param dist: integer, how many tiles around to look for items, ie 7x7
    :param items: array of strings of item codes to search for
    :param port: default is 56799
    :return: {'9345': {'x': 881, 'y': 538, 'dist': 1}}
    """
    tiles = generate_game_tiles_in_coords(x_min, x_max, y_min, y_max, z)
    q = {
        'multipleGameObjects': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['multipleGameObjects'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'multipleGameObjects' in data:
        return data['multipleGameObjects']


# t bow 20997
def get_surrounding_wall_objects(dist, items, port='56799'):
    tiles = generate_surrounding_tiles(dist, port)
    q = {
        'wallObjects': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['wallObjects'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'wallObjects' in data:
        return data['wallObjects']


# t bow 20997
def get_multiple_surrounding_game_objects(dist, items, port='56799'):
    tiles = generate_surrounding_tiles(dist, port)
    q = {
        'multipleGameObjects': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['multipleGameObjects'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'multipleGameObjects' in data:
        return data['multipleGameObjects']

def run_to_loc(steps, port='56799'):
    # dont click on squares hidden by my inventory
    q = {
        'widget': '161,95'
    }
    inv = query_game_data(q, port)
    inv_container = {
        'x_max': inv['widget']['x'] + 130,
        'x_min': inv['widget']['x'] - 130,
        'y_max': inv['widget']['y'] + 175,
        'y_min': inv['widget']['y'] - 175,
    }
    for step in steps:
        start_time = datetime.datetime.now()
        while True:
            data = query_game_data({
                'tiles': [step]
            }, port)
            formatted_step = step.replace(',', '')
            if 'tiles' in data and formatted_step in data['tiles'] and \
                    75 < data['tiles'][formatted_step]['y'] < 1005 and \
                    (data['tiles'][formatted_step]['x'] < inv_container['x_min'] or
                     data['tiles'][formatted_step]['y'] < inv_container['y_min']):
                move_and_click(data['tiles'][formatted_step]['x'], data['tiles'][formatted_step]['y'], 3, 3)
                break
            elif (datetime.datetime.now() - start_time).total_seconds() > 5:
                break
        random_sleep(1.5, 1.6)
    wait_until_stationary(port)
    random_sleep(0.5, 0.6)

def run_to_loc_v2(steps, port='56799'):
    # dont click on squares hidden by my inventory
    q = {
        'widget': '161,95'
    }
    inv = query_game_data(q, port)
    inv_container = {
        'x_max': inv['widget']['x'] + 130,
        'x_min': inv['widget']['x'] - 130,
        'y_max': inv['widget']['y'] + 175,
        'y_min': inv['widget']['y'] - 175,
    }
    for step in steps:
        start_time = datetime.datetime.now()
        while True:
            data = query_game_data({
                'tiles': [step]
            }, port)
            formatted_step = step.replace(',', '')
            if 'tiles' in data and formatted_step in data['tiles'] and \
                    75 < data['tiles'][formatted_step]['y'] < 1005 and \
                    (data['tiles'][formatted_step]['x'] < inv_container['x_min'] or
                     data['tiles'][formatted_step]['y'] < inv_container['y_min']):
                move_and_click(data['tiles'][formatted_step]['x'], data['tiles'][formatted_step]['y'], 3, 3)
                break
            elif (datetime.datetime.now() - start_time).total_seconds() > 5:
                return
        sleep_one_tick()
    wait_until_stationary(port)


def right_click_menu_select(item, entry, port='56799', entry_string=None, entry_action=None):
    move_and_click(item['x'], item['y'], 3, 3, 'right')
    random_sleep(0.4, 0.5)
    q = {
        'getMenuEntries': True
    }
    data = query_game_data(q, port)
    if 'menuEntries' in data:
        curr_pos = pyautogui.position()
        if entry:
            additional_pixels = 20 + (entry - 1) * 15 + 3
            move_and_click(curr_pos[0], curr_pos[1] + additional_pixels, 7, 1)
        elif entry_string and entry_action:
            for i in range(len(data['menuEntries']['items'])):
                if entry_string in data['menuEntries']['items'][i] and entry_action in data['menuEntries']['items'][i]:
                    additional_pixels = (len(data['menuEntries']['items']) - 1 - i) * 15 + 25
                    move_and_click(curr_pos[0], curr_pos[1] + additional_pixels, 7, 1)
                    random_sleep(0.5, 0.6)


def get_player_animation(port='56799'):
    q = {
        'playerAnimation': True
    }
    data = query_game_data(q, port)
    if 'playerAnimation' in data:
        return data['playerAnimation']
    else:
        return -1


def get_full_player_animation(port='56799'):
    q = {
        'playerAnimation': True,
        'poseAnimation': True
    }
    data = query_game_data(q, port)
    if 'playerAnimation' in data and 'primaryPlayerAnimation' in data:
        return {
            'primary': data['playerAnimation'],
            'secondary': data['poseAnimation']
        }
    else:
        return -1


def get_target_obj(port='56799'):
    q = {
        'getTargetObj': True
    }
    data = query_game_data(q, port)
    if 'targetObj' in data:
        return data['targetObj']
    else:
        return -1


def get_target_npc(port='56799'):
    q = {
        'getTargetNPC': True
    }
    data = query_game_data(q, port)
    print(data)
    if 'targetNPC' in data:
        return data['targetNPC']
    else:
        return


def get_npc_by_id(npc_id, port):
    q = {
        'npcsID': [npc_id]
    }
    npcs = query_game_data(q, port)
    if 'npcs' in npcs:
        for npc in npcs['npcs']:
            if str(npc['id']) == npc_id:
                return npc
    return False


def get_npcs_by_id(npc_id, port):
    q = {
        'npcsID': [x.strip() for x in npc_id.split(',')]
    }
    npcs = query_game_data(q, port)
    if 'npcs' in npcs:
        return npcs['npcs']
    return False


def get_chat_options(port):
    q = {
        'chatOptions': True
    }
    chat = query_game_data(q, port)
    if 'chatOptions' in chat:
        return chat['chatOptions']
    return False


def select_chat_option(chat_options, phrase):
    if not chat_options:
        return -1
    for i, option in enumerate(chat_options):
        if phrase in option:
            return i
    return -1


def get_varbit_value(varbit, port):
    q = {
        'varBit': varbit
    }
    vb = query_game_data(q, port)
    if 'varBit' in vb:
        return vb['varBit']
    return False


def have_leveled_up(port='56799'):
    leveled_up_widget = get_widget('233,0', port)
    if leveled_up_widget:
        return True
    return False


def click_banker(port='56799'):
    q = {
        'npcs': ['Banker']
    }
    data = query_game_data(q, port)
    if len(data["npcs"]) != 0:
        closest = find_closest_npc(data['npcs'])
        move_and_click(closest['x'], closest['y'], 5, 6)


def deposit_all_but_x_in_bank(items, port='56799'):
    while True:
        found_additional_items = False
        inv = get_inv(port)
        for item in inv:
            if item['id'] not in items:
                found_additional_items = True
                move_and_click(item['x'], item['y'], 3, 3)
                random_sleep(0.5, 0.6)
                break
        if not found_additional_items:
            break
    random_sleep(0.5, 0.6)


def deposit_all_of_x(items, port='56799'):
    while True:
        found_additional_items = False
        inv = get_inv(port)
        for item in inv:
            if item['id'] in items:
                found_additional_items = True
                move_and_click(item['x'], item['y'], 3, 3)
                random_sleep(0.5, 0.6)
                break
        if not found_additional_items:
            break
    random_sleep(0.5, 0.6)


def get_item_quantity_in_inv(inv, targ):
    quantity = 0
    for item in inv:
        if item['id'] == int(targ):
            quantity += item['quantity']
    return quantity


def run_towards_square(destination, port):
    """

    :param destination: obj {x: 2341, y: 687, z:0}
    :type port: str
    """

    loc = get_world_location(port)
    steps = []
    while loc['x'] != destination['x'] or loc['y'] != destination['y']:
        x_diff = destination['x'] - loc['x']
        x_inc = 0
        if x_diff > 0:
            x_inc = min(5, x_diff)
        else:
            x_inc = max(-5, x_diff)
        y_diff = destination['y'] - loc['y']
        y_inc = 0
        if y_diff > 0:
            y_inc = min(5, y_diff)
        else:
            y_inc = max(-5, y_diff)
        loc['x'] = loc['x'] + x_inc
        loc['y'] = loc['y'] + y_inc
        next_sq = '{},{},{}'.format(loc['x'], loc['y'], loc['z'])
        steps.append(next_sq)
    print(steps)
    run_to_loc(steps)

def run_towards_square_v2(destination, port):
    """

    :param destination: obj {x: 2341, y: 687, z:0}
    :type port: str
    """

    loc = get_world_location(port)
    steps = []
    while loc['x'] != destination['x'] or loc['y'] != destination['y']:
        x_diff = destination['x'] - loc['x']
        x_inc = 0
        if x_diff > 0:
            x_inc = min(5, x_diff)
        else:
            x_inc = max(-5, x_diff)
        y_diff = destination['y'] - loc['y']
        y_inc = 0
        if y_diff > 0:
            y_inc = min(5, y_diff)
        else:
            y_inc = max(-5, y_diff)

        if abs(x_inc) < 5 and abs(y_inc) < 5:
            break
        loc['x'] = loc['x'] + x_inc
        loc['y'] = loc['y'] + y_inc
        next_sq = '{},{},{}'.format(loc['x'], loc['y'], loc['z'])
        steps.append(next_sq)
    print(steps)
    run_to_loc_v2(steps)


def objective_click_handler(fn, exit_condition, max_iter):
    iterations = 0
    while iterations < max_iter:
        fn()
        if exit_condition:
            return True
    return False


def is_mining(port='56799'):
    q = {
        'isMining': True,
    }
    data = query_game_data(q, port)
    if 'isMining' in data:
        return data['isMining']
    return False

def spam_click(tile, seconds, port='56799'):
    start_time = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - start_time).total_seconds() > seconds:
            break
        else:
            while True:
                data = query_game_data({
                    'tiles': [tile]
                }, port)
                formatted_step = tile.replace(',', '')
                if 'tiles' in data and formatted_step in data['tiles'] and \
                        75 < data['tiles'][formatted_step]['y'] < 1040:
                    fast_move_and_click(data['tiles'][formatted_step]['x'], data['tiles'][formatted_step]['y'], 3, 3)
                    break
                random_sleep(0.3, 0.4)


def fast_move_and_click(x, y, w, h, button='left'):
    bezier_movement(x - w, y - h, x + w, y + h)
    pyautogui.click()


def set_yaw(val, port):
    q = {
        'setYaw': str(val)
    }
    query_game_data(q, port)


def get_interacting(port):
    q = {
        'interactingWith': True,
    }
    data = query_game_data(q, port)
    if 'interactingWith' in data:
        return data['interactingWith']
    else:
        return False

def press_key(key):
    if key == 'esc':
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)

def set_timings(timings, current_time):
    config['timings']['script_start'] = current_time
    config['timings']['break_start'] = current_time + datetime.timedelta(
        minutes=random.randint(timings['min_session'], timings['max_session'])
    )
    config['timings']['break_end'] = config['timings']['break_start'] + datetime.timedelta(
        minutes=random.randint(timings['min_rest'], timings['max_rest'])
    )


def break_manager_v2(script_config):
    """
    :param script_config: Object
    {
        'intensity': 'high' | 'low',
        'logout': function(), -- Steps to run before logging out for break
        'login': function(), -- Steps to run after logging back in
    }
    """
    current_time = datetime.datetime.now()
    timings = config['{}_intensity_script'.format(script_config['intensity'])]
    # Initialize timings on script start
    if not config['timings']['script_start']:
        set_timings(timings, current_time)
    # Begin break period
    if current_time > config['timings']['break_start'] and not config['timings']['on_break']:
        if script_config.logout:
            script_config.logout()
        logout()
        config['timings']['on_break'] = True
    elif config['timings']['break_start'] < current_time < config['timings']['break_end'] \
            and config['timings']['on_break']:
        move_and_click(500, 500, 5, 5)
        random_sleep(10, 15)
    elif current_time > config['timings']['break_end'] \
            and config['timings']['on_break']:
        login(get_config(config.password))
        if script_config.login:
            script_config.login()
        set_timings(timings, current_time)