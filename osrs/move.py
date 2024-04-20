import datetime
import math
import platform
import random
import time

import numpy as np
import pyautogui
from scipy import interpolate

import osrs.dev as dev
import osrs.move
import osrs.server as server
import osrs.clock as clock
import osrs.dax as dax
import osrs.util as util
import osrs.queryHelper as queryHelper

inv_widget_id = '161,97'
minimap_widget_id = '161,95'
chat_buttons_widget_id = '162,1'

config = dev.load_yaml()


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
    except ValueError as bez:
        print(f'bezier movement blew up: {bez}')
        pyautogui.moveTo(x2, y2)
        return [x2, y2]
    # Move upto a certain number of points
    u = np.linspace(0, 1, num=2 + int(dev.point_dist(x1, y1, x2, y2) / 50.0))
    points = interpolate.splev(u, tck)

    # Move mouse.
    duration = 0.1
    timeout = duration / len(points[0])
    point_list = zip(*(i.astype(int) for i in points))
    for point in point_list:
        if point[0] > 1920 or point[0] < 0 or point[1] < 20 or point[1] > 1040:
            print('point: {} out of bounds, rejecting movement request.'.format(point))
            return False
        pyautogui.moveTo(*point)
        time.sleep(timeout)
    return [x2, y2]


def wait_until_stationary(port='56799'):
    POSE_ANIMATION = {
        'poseAnimation': True
    }
    while True:
        data = server.query_game_data(POSE_ANIMATION, port)
        # i am not moving
        if 'poseAnimation' in data and (data['poseAnimation'] == 808 or data['poseAnimation'] == 813 or data['poseAnimation'] == 4591):
            break
        else:
            clock.random_sleep(0.1, 0.2)


def am_stationary(port='56799'):
    POSE_ANIMATION = {
        'poseAnimation': True
    }
    data = server.query_game_data(POSE_ANIMATION, port)
    if 'poseAnimation' in data and data['poseAnimation'] == 808:
        return True
    else:
        return False


def move_and_click(x, y, w, h, button='left'):
    movement = bezier_movement(x - w, y - h, x + w, y + h)
    clock.random_sleep(0.15, 0.25)
    curr_pos = pyautogui.position()
    # DO NOT CLICK ON THE TASK BAR
    if not movement:
        print('movement was unsuccessful, target was off screen. Rejecting click.')
        return
    pyautogui.click() if button == 'left' else pyautogui.click(button='right')
    clock.random_sleep(0.15, 0.25)


def click(obj):
    movement = bezier_movement(obj['x'] - 1, obj['y'], obj['x'], obj['y'] + 1)
    clock.random_sleep(0.15, 0.25)
    # DO NOT CLICK ON THE TASK BAR
    if not movement:
        print('movement was unsuccessful, target was off screen. Rejecting click.')
        return
    pyautogui.click()
    clock.random_sleep(0.15, 0.25)


def fast_click(obj):
    movement = bezier_movement(obj['x'] - 3, obj['y'] - 3, obj['x'] + 3, obj['y'] + 3)
    if not movement:
        print('movement was unsuccessful, target was off screen. Rejecting click.')
        return
    pyautogui.click()


def fast_move(obj):
    bezier_movement(obj['x'] - 3, obj['y'] - 3, obj['x'] + 3, obj['y'] + 3)


def jiggle_mouse():
    x1, y1 = pyautogui.position()
    bezier_movement(x1 - 90, y1 - 90, x1 - 50, y1 -30)


def run_to_loc(steps, port='56799'):
    # dont click on squares hidden by my inventory
    q = {
        'widget': '161,95'
    }
    inv = server.query_game_data(q, port)
    inv_container = {
        'x_max': inv['widget']['x'] + 130,
        'x_min': inv['widget']['x'] - 130,
        'y_max': inv['widget']['y'] + 175,
        'y_min': inv['widget']['y'] - 175,
    }
    for step in steps:
        start_time = datetime.datetime.now()
        while True:
            data = server.query_game_data({
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
        clock.random_sleep(1.5, 1.6)
    wait_until_stationary(port)
    clock.random_sleep(0.5, 0.6)


def run_to_loc_v2(steps, port='56799'):
    # dont click on squares hidden by my inventory
    q = {
        'widget': '161,95'
    }
    inv = server.query_game_data(q, port)
    inv_container = {
        'x_max': inv['widget']['x'] + 130,
        'x_min': inv['widget']['x'] - 130,
        'y_max': inv['widget']['y'] + 175,
        'y_min': inv['widget']['y'] - 175,
    }
    for step in steps:
        start_time = datetime.datetime.now()
        while True:
            data = server.query_game_data({
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
        clock.sleep_one_tick()
    wait_until_stationary(port)


def run_towards_square(destination, port):
    """

    :param destination: obj {x: 2341, y: 687, z:0}
    :type port: str
    """

    loc = server.get_world_location(port)
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
    run_to_loc(steps)


def run_towards_square_v2(destination, port='56799'):
    """

    :param destination: obj {x: 2341, y: 687, z:0}
    :type port: str
    """

    loc = server.get_world_location(port)
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
    print('run towards steps', steps)
    # I will never call this function on a destination this far away
    if len(steps) > 100:
        return
    run_to_loc_v2(steps)


def click_off_screen(x1=3000, x2=3100, y1=100, y2=200, click=True):
    bezier_movement(x1, y1, x2, y2)
    clock.random_sleep(0.15, 0.25)
    if click:
        pyautogui.click()
        clock.random_sleep(0.15, 0.25)


def fast_move_and_click(x, y, w, h, button='left'):
    bezier_movement(x - w, y - h, x + w, y + h)
    pyautogui.click()


def instant_click(x, y):
    pyautogui.moveTo(x, y)
    clock.random_sleep(0.1, 0.11)
    pyautogui.click()


def spam_click(tile, seconds, port='56799'):
    start_time = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - start_time).total_seconds() > seconds:
            break
        data = server.query_game_data({
            'tiles': [tile]
        }, port)
        formatted_step = tile.replace(',', '')
        if 'tiles' in data and formatted_step in data['tiles'] and \
                75 < data['tiles'][formatted_step]['y'] < 1040:
            fast_move_and_click(data['tiles'][formatted_step]['x'], data['tiles'][formatted_step]['y'], 3, 3)


def instant_spam_click(tile, seconds, port='56799'):
    start_time = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - start_time).total_seconds() > seconds:
            break
        else:
            while True:
                data = server.query_game_data({
                    'tiles': [tile]
                }, port)
                formatted_step = tile.replace(',', '')
                if 'tiles' in data and formatted_step in data['tiles'] and \
                        75 < data['tiles'][formatted_step]['y'] < 1040:
                    instant_click(data['tiles'][formatted_step]['x'], data['tiles'][formatted_step]['y'])
                    break
                else:
                    break


def spam_on_screen(x, y, seconds):
    start_time = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - start_time).total_seconds() > seconds:
            instant_click(x, y)


# this doesnt work on my mac bc of the different screen resolutions...
def right_click_menu_select(item, entry, port='56799', entry_string=None, entry_action=None):
    if platform.system() == 'Darwin':
        return mac_right_click_menu_select(item, entry_action)
    move_and_click(item['x'], item['y'], 3, 3, 'right')
    clock.random_sleep(0.2, 0.3)
    q = {
        'getMenuEntries': True
    }
    data = server.query_game_data(q, port)
    if 'menuEntries' in data:
        curr_pos = pyautogui.position()
        if entry:
            additional_pixels = 20 + (entry - 1) * 15 + 3
            if platform.system() == 'Darwin':
                additional_pixels = math.floor(additional_pixels / 2)
            move_and_click(curr_pos[0], curr_pos[1] + additional_pixels, 7, 1)
        elif entry_action:
            for i in range(len(data['menuEntries']['items'])):
                if entry_action in data['menuEntries']['items'][i]:
                    additional_pixels = (len(data['menuEntries']['items']) - 1 - i) * 15 + 25
                    if platform.system() == 'Darwin':
                        additional_pixels = 19 + (len(data['menuEntries']['items']) - 1 - i) * 15
                    print(additional_pixels)
                    move_and_click(curr_pos[0], curr_pos[1] + additional_pixels, 7, 1)
                    return True
            return False


def right_click_menu_select_v2(item, entry_action):
    move_and_click(item['x'], item['y'], 3, 3, 'right')
    clock.random_sleep(0.2, 0.3)
    q = {
        'getMenuEntries': True
    }
    data = server.query_game_data(q, config['port'])
    if 'menuEntries' in data:
        curr_pos = pyautogui.position()
        reversed_entries = list(reversed(data['menuEntries']['items']))
        for i, item in enumerate(reversed_entries):
            if entry_action in item:
                additional_pixels = 22 + (len(data['menuEntries']['items']) - 1 - i) * 15
                move_and_click(curr_pos[0], curr_pos[1] + additional_pixels, 0, 0)
                return


def right_click_v3(item, action):
    move_and_click(item['x'], item['y'], 3, 3, 'right')
    curr_pos = pyautogui.position()
    clock.random_sleep(0.2, 0.3)
    q = {
        'rightClick': True
    }
    data = server.query_game_data(q, config['port'])
    if 'rightClickMenu' in data:
        entry_data = data['rightClickMenu']
        choose_option_offset = entry_data['height'] - (len(entry_data['entries']) * 15)
        parsed_entries = reversed(entry_data['entries'])
        for i, entry in enumerate(parsed_entries):
            if action.upper() == entry.upper():
                additional = choose_option_offset + (i * 15)
                move_and_click(
                    curr_pos[0],
                    curr_pos[1] + additional,
                    0,
                    0
                )
                return


def mac_right_click_menu_select(item, entry_action=None):
    move_and_click(item['x'], item['y'], 3, 3, 'right')
    clock.random_sleep(0.2, 0.3)
    q = {
        'getMenuEntries': True
    }
    data = server.query_game_data(q, config['port'])
    if 'menuEntries' in data:
        curr_pos = pyautogui.position()
        print(curr_pos, pyautogui.position())
        reversed_entries = list(reversed(data['menuEntries']['items']))
        for i, item in enumerate(reversed_entries):
            if entry_action in item:
                # Choose Option menu part is 19px, add a few more to get into the option i want
                additional_pixels = 19 + ((i + 1) * 15) - 44
                print('apx', additional_pixels)
                move_and_click(curr_pos[0], curr_pos[1] + additional_pixels, 0, 0)
                print(pyautogui.position())
                # random_sleep(0.5, 0.6)
                return


def move_around_center_screen(x1=800, y1=400, x2=1000, y2=600):
    bezier_movement(x1, y1, x2, y2)
    clock.random_sleep(0.15, 0.25)


def follow_path(start, end):
    path = dax.generate_path(start, end)
    if not path:
        return
    parsed_tiles = util.tile_objects_to_strings(path)
    qh = queryHelper.QueryHelper()
    qh.set_tiles(set(parsed_tiles))
    qh.set_destination_tile()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        dist_to_end = osrs.dev.point_dist(
            qh.get_player_world_location('x'),
            qh.get_player_world_location('y'),
            int(parsed_tiles[-1].split(',')[0]),
            int(parsed_tiles[-1].split(',')[1])
        )
        # sometimes the tile i want to end up on has an object on it so i cant actually stand on it,
        # in that case, i still want to break if i am at the end of the path
        if f"{qh.get_player_world_location('x')},{qh.get_player_world_location('y')},0" == parsed_tiles[-1] or \
                dist_to_end <= 3:
            break
        for tile in reversed(parsed_tiles):
            if is_clickable(qh.get_tiles(tile)):
                osrs.move.fast_click(qh.get_tiles(tile))
                break


def is_clickable(target):
    if not target or 'x' not in target or 'y' not in target:
        return False
    qh = queryHelper.QueryHelper()
    qh.set_canvas()
    qh.set_widgets({minimap_widget_id, inv_widget_id, chat_buttons_widget_id})
    qh.query_backend()
    target_on_canvas = qh.get_canvas()['xMin'] + 10 < target['x'] < qh.get_canvas()['xMax'] - 10 and qh.get_canvas()['yMin'] + 10 < target['y'] < qh.get_canvas()['yMax'] - 10
    target_on_inv = qh.get_widgets(inv_widget_id)['xMin'] - 10 < target['x'] < qh.get_widgets(inv_widget_id)['xMax'] + 10 and \
                    qh.get_widgets(inv_widget_id)['yMin'] - 10 < target['y'] < qh.get_widgets(inv_widget_id)['yMax'] + 10
    target_on_chat_buttons = qh.get_widgets(chat_buttons_widget_id)['xMin'] < target['x'] < qh.get_widgets(chat_buttons_widget_id)['xMax'] and \
                    qh.get_widgets(chat_buttons_widget_id)['yMin'] - 25 < target['y'] < qh.get_widgets(chat_buttons_widget_id)['yMax'] + 25
    target_on_minimap = qh.get_widgets(minimap_widget_id)['xMin'] < target['x'] < qh.get_widgets(minimap_widget_id)['xMax'] and \
                    qh.get_widgets(minimap_widget_id)['yMin'] < target['y'] < qh.get_widgets(minimap_widget_id)['yMax']
    return target_on_canvas and not target_on_inv and not target_on_minimap and not target_on_chat_buttons


