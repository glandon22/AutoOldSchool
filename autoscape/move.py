import datetime
import platform
import random
import time

import numpy as np
import pyautogui
from scipy import interpolate

import general_utils


def bezier_movement(x_min, y_min, x_max, y_max):
    y_max = y_max + 42 if platform.system() == 'Darwin' else y_max
    y_min = y_min + 42 if platform.system() == 'Darwin' else y_min
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
    u = np.linspace(0, 1, num=2 + int(general_utils.point_dist(x1, y1, x2, y2) / 50.0))
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


def click_off_screen(x1=3000, x2=3100, y1=100, y2=200, click=True):
    bezier_movement(x1, y1, x2, y2)
    general_utils.random_sleep(0.15, 0.25)
    if click:
        pyautogui.click()
        general_utils.random_sleep(0.15, 0.25)


def move_and_click(x, y, w, h, button='left'):
    movement = bezier_movement(x - w, y - h, x + w, y + h)
    general_utils.random_sleep(0.15, 0.25)
    curr_pos = pyautogui.position()
    print('pos', curr_pos, curr_pos[1])
    # DO NOT CLICK ON THE TASK BAR
    if not movement:
        print('movement was unsuccessful, target was off screen. Rejecting click.')
        return
    pyautogui.click() if button == 'left' else pyautogui.click(button='right')
    general_utils.random_sleep(0.15, 0.25)


def move_around_center_screen(x1=800, y1=400, x2=1000, y2=600):
    bezier_movement(x1, y1, x2, y2)
    general_utils.random_sleep(0.15, 0.25)


def fast_move_and_click(x, y, w, h, button='left'):
    bezier_movement(x - w, y - h, x + w, y + h)
    pyautogui.click()


def spam_click(tile, seconds, port='56799'):
    start_time = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - start_time).total_seconds() > seconds:
            break
        else:
            while True:
                data = general_utils.query_game_data({
                    'tiles': [tile]
                }, port)
                formatted_step = tile.replace(',', '')
                if 'tiles' in data and formatted_step in data['tiles'] and \
                        75 < data['tiles'][formatted_step]['y'] < 1040:
                    fast_move_and_click(data['tiles'][formatted_step]['x'], data['tiles'][formatted_step]['y'], 3, 3)
                    break
                general_utils.random_sleep(0.3, 0.4)


def run_towards_square_v2(destination, port):
    """

    :param destination: obj {x: 2341, y: 687, z:0}
    :type port: str
    """

    loc = general_utils.get_world_location(port)
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


def run_towards_square(destination, port):
    """

    :param destination: obj {x: 2341, y: 687, z:0}
    :type port: str
    """

    loc = general_utils.get_world_location(port)
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


def run_to_loc(steps, port='56799'):
    # dont click on squares hidden by my inventory
    q = {
        'widget': '161,95'
    }
    inv = general_utils.query_game_data(q, port)
    inv_container = {
        'x_max': inv['widget']['x'] + 130,
        'x_min': inv['widget']['x'] - 130,
        'y_max': inv['widget']['y'] + 175,
        'y_min': inv['widget']['y'] - 175,
    }
    for step in steps:
        start_time = datetime.datetime.now()
        while True:
            data = general_utils.query_game_data({
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
        general_utils.random_sleep(1.5, 1.6)
    general_utils.wait_until_stationary(port)
    general_utils.random_sleep(0.5, 0.6)


def run_to_loc_v2(steps, port='56799'):
    # dont click on squares hidden by my inventory
    q = {
        'widget': '161,95'
    }
    inv = general_utils.query_game_data(q, port)
    inv_container = {
        'x_max': inv['widget']['x'] + 130,
        'x_min': inv['widget']['x'] - 130,
        'y_max': inv['widget']['y'] + 175,
        'y_min': inv['widget']['y'] - 175,
    }
    for step in steps:
        start_time = datetime.datetime.now()
        while True:
            data = general_utils.query_game_data({
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
        general_utils.sleep_one_tick()
    general_utils.wait_until_stationary(port)


def right_click_menu_select(item, entry, port='56799', entry_string=None, entry_action=None):
    move_and_click(item['x'], item['y'], 3, 3, 'right')
    general_utils.random_sleep(0.4, 0.5)
    q = {
        'getMenuEntries': True
    }
    data = general_utils.query_game_data(q, port)
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
                    general_utils.random_sleep(0.5, 0.6)