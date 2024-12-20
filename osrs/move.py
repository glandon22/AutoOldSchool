import datetime
import math
import platform
import random
import time

import numpy as np
import pyautogui
from Xlib.Xcursorfont import target
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
        if 'poseAnimation' in data and (
                data['poseAnimation'] == 808 or data['poseAnimation'] == 813 or data['poseAnimation'] == 4591):
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
    movement = bezier_movement(obj['x'], obj['y'], obj['x'], obj['y'])
    if not movement:
        print('movement was unsuccessful, target was off screen. Rejecting click.')
        return
    osrs.clock.random_sleep(0.01, 0.02)
    pyautogui.click()


def fast_click_v2(obj, button='PRIMARY'):
    pyautogui.moveTo(obj['x'], obj['y'])
    if button == 'PRIMARY':
        osrs.clock.random_sleep(0.11, 0.12)
    pyautogui.click(button=button)


def fast_right_click(obj):
    movement = bezier_movement(obj['x'] - 3, obj['y'] - 3, obj['x'] + 3, obj['y'] + 3)
    if not movement:
        print('movement was unsuccessful, target was off screen. Rejecting click.')
        return
    pyautogui.click(button='RIGHT')


def fast_move(obj):
    bezier_movement(obj['x'] - 3, obj['y'] - 3, obj['x'] + 3, obj['y'] + 3)


def jiggle_mouse():
    x1, y1 = pyautogui.position()
    bezier_movement(x1 - 90, y1 - 90, x1 - 50, y1 - 30)


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


def run_towards_square(destination, port=56799, steps_only=False):
    """

    :param steps_only: true || False
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
    if steps_only:
        return steps
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


def run_towards_square_v3(destination, steps_only=False, loc=None):
    """

    :param steps_only: true || False
    :param destination: obj {x: 2341, y: 687, z:0}
    :type port: str
    """
    if not loc:
        loc = server.get_world_location()
    steps = []
    while loc['x'] != destination['x'] or loc['y'] != destination['y']:
        x_diff = destination['x'] - loc['x']
        x_inc = 0
        if x_diff > 0:
            x_inc = min(2, x_diff)
        else:
            x_inc = max(-2, x_diff)
        y_diff = destination['y'] - loc['y']
        y_inc = 0
        if y_diff > 0:
            y_inc = min(2, y_diff)
        else:
            y_inc = max(-2, y_diff)
        loc['x'] = loc['x'] + x_inc
        loc['y'] = loc['y'] + y_inc
        next_sq = '{},{},{}'.format(loc['x'], loc['y'], loc['z'])
        steps.append(next_sq)
    if steps_only:
        return steps
    run_to_loc(steps)


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


def instant_move(obj):
    pyautogui.moveTo(obj['x'], obj['y'])


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
                return True


# when you right click something in your inventory,
# the game returns the action ie Drop and some random number
# but when you click an item on the ground it gives you the
# item id
def right_click_v4(item, action, in_inv=False):
    move_and_click(item['x'], item['y'], 3, 3, 'right')
    curr_pos = pyautogui.position()
    qh = queryHelper.QueryHelper()
    qh.set_right_click_menu()
    wait_start = datetime.datetime.now()
    while True:
        qh.query_backend()
        if (datetime.datetime.now() - wait_start).total_seconds() > 1:
            pyautogui.click()
            return False
        if qh.get_right_click_menu():
            entry_data = qh.get_right_click_menu()
            choose_option_offset = entry_data['height'] - (len(entry_data['entries']) * 15)
            parsed_entries = reversed(entry_data['entries'])
            for i, entry in enumerate(parsed_entries):
                if action.upper() == entry[0].upper() and (in_inv or item['id'] == int(entry[1])):
                    additional = choose_option_offset + (i * 15)
                    move_and_click(
                        curr_pos[0],
                        curr_pos[1] + additional,
                        0,
                        0
                    )
                    return True


def right_click_v5(item, action, in_inv=False):
    move_and_click(item['x'], item['y'], 3, 3, 'right')
    curr_pos = pyautogui.position()
    qh = queryHelper.QueryHelper()
    qh.set_right_click_menu()
    while True:
        qh.query_backend()
        if qh.get_right_click_menu():
            entry_data = qh.get_right_click_menu()
            choose_option_offset = entry_data['height'] - (len(entry_data['entries']) * 15)
            parsed_entries = reversed(entry_data['entries'])
            for i, entry in enumerate(parsed_entries):
                if action.upper() == entry[0].upper() and (in_inv or item['id'] == int(entry[1])):
                    additional = choose_option_offset + (i * 15)
                    move_and_click(
                        curr_pos[0],
                        curr_pos[1] + additional,
                        0,
                        0
                    )
                    return True
            pyautogui.click()
            return False


def check_right_click_options(item, action, canvas, in_inv=False):
    osrs.move.move_and_click(item['x'], item['y'], 3, 3, 'right')
    curr_pos = pyautogui.position()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_right_click_menu()
    max_canvas_y = canvas['yMax'] - canvas['yMin']
    # if i right click something that is low on the screen, the menu would open off the screen so the game pushes it up
    additional_offset = 0
    while True:
        qh.query_backend()
        if qh.get_right_click_menu():
            if curr_pos[1] + qh.get_right_click_menu()['height'] > max_canvas_y:
                print('too big')
                # the extra "- 15" is because this doesnt account for the menu header, which is 15px on a 1080p screen
                additional_offset = qh.get_right_click_menu()['y'] + 40 - curr_pos[1] - 15
            entry_data = qh.get_right_click_menu()
            choose_option_offset = entry_data['height'] - (len(entry_data['entries']) * 15)
            parsed_entries = reversed(entry_data['entries'])
            for i, entry in enumerate(parsed_entries):
                if action.upper() == entry[0].upper() and (in_inv or item['id'] == int(entry[1])):
                    pyautogui.click()
                    return True
            pyautogui.click()
            return False


def right_click_v6(item, action, canvas, in_inv=False):
    osrs.move.fast_click_v2(item, 'RIGHT')
    osrs.clock.random_sleep(0.05, 0.051)
    curr_pos = pyautogui.position()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_right_click_menu()
    max_canvas_y = canvas['yMax']
    while True:
        qh.query_backend()
        rcm = qh.get_right_click_menu()
        if rcm:
            # this is the y coord of the very top of the menu
            menu_top = rcm['y'] + canvas['yOffset']
            if curr_pos[1] + rcm['height'] > max_canvas_y:
                # the extra "- 15" is because this doesnt account for the menu header, which is 15px on a 1080p screen
                additional_offset = rcm['y'] + 40 - curr_pos[1] - 15
            entry_data = rcm
            choose_option_offset = entry_data['height'] - (len(entry_data['entries']) * 15)
            parsed_entries = reversed(entry_data['entries'])
            for i, entry in enumerate(parsed_entries):
                if action.upper() == entry[0].upper() and (in_inv or item['id'] == int(entry[1])):
                    osrs.move.fast_click_v2({'x': curr_pos[0], 'y': menu_top + choose_option_offset + (i * 15)})
                    return True
            pyautogui.click()
            return False


def right_click_v7(item, action, canvas, target=None):
    osrs.move.fast_click_v2(item, 'RIGHT')
    osrs.clock.random_sleep(0.05, 0.051)
    curr_pos = pyautogui.position()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_right_click_menu()
    max_canvas_y = canvas['yMax']
    while True:
        qh.query_backend()
        rcm = qh.get_right_click_menu()
        if rcm:
            # this is the y coord of the very top of the menu
            menu_top = rcm['y'] + canvas['yOffset']
            if curr_pos[1] + rcm['height'] > max_canvas_y:
                # the extra "- 15" is because this doesnt account for the menu header, which is 15px on a 1080p screen
                additional_offset = rcm['y'] + 40 - curr_pos[1] - 15
            entry_data = rcm
            choose_option_offset = entry_data['height'] - (len(entry_data['entries']) * 15)
            parsed_entries = reversed(entry_data['entries'])
            for i, entry in enumerate(parsed_entries):
                if action.upper() == entry[0].upper() and (not target or target.lower() in entry[2].lower()):
                    osrs.move.fast_click_v2({'x': curr_pos[0], 'y': menu_top + choose_option_offset + (i * 15)})
                    return True
            pyautogui.click()
            return False


def right_click_v8(item, action, qh: osrs.queryHelper.QueryHelper, tg=None):
    canvas = qh.get_canvas()
    rcm = qh.get_right_click_menu()
    if rcm:
        curr_pos = pyautogui.position()
        max_canvas_y = canvas['yMax']
        # this is the y coord of the very top of the menu
        menu_top = rcm['server_y'] + canvas['yOffset']
        entry_data = rcm
        choose_option_offset = 21
        parsed_entries = reversed(entry_data['entries'])
        for i, entry in enumerate(parsed_entries):
            if action.upper() == entry[0].upper() and (not tg or tg.lower() in entry[2].lower()):
                pyautogui.click(button='RIGHT')
                osrs.clock.random_sleep(0.1, 0.11)
                pyautogui.click(curr_pos[0], menu_top + choose_option_offset + (i * 15))
                return True
        osrs.move.fast_move(item)
    else:
        osrs.move.fast_move(item)
    return False



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


def follow_path(
        start, end, right_click=False, exact_tile=False, skip_dax=False,
        player_loc=None
):
    # selected = 3053
    all_chat_widget = '162,5'
    game_chat_widget = '162,8'
    pub_chat_widget = '162,12'
    priv_chat_widget = '162,16'
    chan_chat_widget = '162,20'
    clan_chat_widget = '162,24'
    trade_chat_widget = '162,28'
    report_player_widget = '875,22'
    path = None
    if not skip_dax:
        path = dax.generate_path(start, end)
    parsed_tiles = []
    if not path:
        # if dax failed fall back to my budget patching homebrewed deal
        parsed_tiles = run_towards_square_v3(
            {'x': end['x'], 'y': end['y'], 'z': 0}, steps_only=True, loc=player_loc
        )
    else:
        parsed_tiles = util.tile_objects_to_strings(path)
    qh = queryHelper.QueryHelper()
    qh.set_tiles(set(parsed_tiles))
    qh.set_destination_tile()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_widgets({game_chat_widget, all_chat_widget, pub_chat_widget, priv_chat_widget, chan_chat_widget, clan_chat_widget, trade_chat_widget, report_player_widget})
    prev_loc = None
    time_on_same_tile = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - time_on_same_tile).total_seconds() > 2.5:
            osrs.dev.logger.warning('2.5 seconds on same tile, ending')
            return

        if qh.get_player_world_location() != prev_loc:
            prev_loc = qh.get_player_world_location()
            time_on_same_tile = datetime.datetime.now()

        qh.query_backend()

        if qh.get_destination_tile() == end:
            last_tile = None
            time_on_tile = datetime.datetime.now()
            while True:
                qh.query_backend()
                if qh.get_player_world_location('x') == end['x'] and qh.get_player_world_location('y') == end['y']:
                    osrs.dev.logger.info("Arrived at destination.")
                    return
                elif qh.get_player_world_location() != last_tile:
                    last_tile = qh.get_player_world_location()
                    time_on_tile = datetime.datetime.now()
                elif (datetime.datetime.now() - time_on_tile).total_seconds() > 1:
                    osrs.dev.logger.info("Timed out trying to go to loc")
                    break
            continue
        # ensure that the chat box isnt open bc it blocks my clicks
        if qh.get_widgets(report_player_widget):
            osrs.keeb.press_key('esc')
        for key in qh.get_widgets():
            if qh.get_widgets(key)['spriteID'] == 3053:
                osrs.move.fast_click(qh.get_widgets(key))
                break
        dist_to_end = osrs.dev.point_dist(
            qh.get_player_world_location('x'),
            qh.get_player_world_location('y'),
            int(parsed_tiles[-1].split(',')[0]),
            int(parsed_tiles[-1].split(',')[1])
        )
        # sometimes the tile i want to end up on has an object on it so i cant actually stand on it,
        # in that case, i still want to break if i am at the end of the path
        if dist_to_end <= 3 and not exact_tile:
            break
        elif exact_tile and dist_to_end == 0:
            osrs.dev.logger.info("On desired tile - exiting")
        for tile in reversed(parsed_tiles):
            if qh.get_tiles(tile) and qh.get_tiles(tile)['dist'] <= 10:
                if right_click:
                    osrs.move.right_click_v6(qh.get_tiles(tile), 'Walk here', qh.get_canvas(), in_inv=True)
                else:
                    osrs.move.fast_click(qh.get_tiles(tile))
                break


def fixed_follow_path(path, right_click=False, exact_tile=False):
    # selected = 3053
    all_chat_widget = '162,5'
    game_chat_widget = '162,8'
    pub_chat_widget = '162,12'
    priv_chat_widget = '162,16'
    chan_chat_widget = '162,20'
    clan_chat_widget = '162,24'
    trade_chat_widget = '162,28'
    report_player_widget = '875,22'

    parsed_tiles = path
    qh = queryHelper.QueryHelper()
    qh.set_tiles(set(parsed_tiles))
    qh.set_destination_tile()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_widgets({game_chat_widget, all_chat_widget, pub_chat_widget, priv_chat_widget, chan_chat_widget, clan_chat_widget, trade_chat_widget, report_player_widget})
    prev_loc = None
    time_on_same_tile = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - time_on_same_tile).total_seconds() > 2.5:
            print('2.5 seconds on same tile, ending - fixed')
            return
        if qh.get_player_world_location() != prev_loc:
            prev_loc = qh.get_player_world_location()
            time_on_same_tile = datetime.datetime.now()
        qh.query_backend()
        # ensure that the chat box isnt open bc it blocks my clicks
        if qh.get_widgets(report_player_widget):
            osrs.keeb.press_key('esc')
        for key in qh.get_widgets():
            if qh.get_widgets(key)['spriteID'] == 3053:
                osrs.move.fast_click(qh.get_widgets(key))
                break
        dist_to_end = osrs.dev.point_dist(
            qh.get_player_world_location('x'),
            qh.get_player_world_location('y'),
            int(parsed_tiles[-1].split(',')[0]),
            int(parsed_tiles[-1].split(',')[1])
        )
        # sometimes the tile i want to end up on has an object on it so i cant actually stand on it,
        # in that case, i still want to break if i am at the end of the path
        if dist_to_end <= 3 and not exact_tile:
            break
        for tile in reversed(parsed_tiles):
            if is_clickable(qh.get_tiles(tile)):
                if right_click:
                    osrs.move.right_click_v6(qh.get_tiles(tile), 'Walk here', qh.get_canvas(), in_inv=True)
                else:
                    osrs.move.fast_click(qh.get_tiles(tile))
                break


def is_clickable(target):
    if not target or 'x' not in target or 'y' not in target:
        return False
    qh = queryHelper.QueryHelper()
    qh.set_canvas()
    qh.set_widgets({minimap_widget_id, inv_widget_id, chat_buttons_widget_id})
    qh.query_backend()
    target_on_canvas = qh.get_canvas()['xMin'] + 10 < target['x'] < qh.get_canvas()['xMax'] - 10 and qh.get_canvas()[
        'yMin'] + 10 < target['y'] < qh.get_canvas()['yMax'] - 10
    target_on_inv = qh.get_widgets(inv_widget_id)['xMin'] - 10 < target['x'] < qh.get_widgets(inv_widget_id)[
        'xMax'] + 10 and \
                    qh.get_widgets(inv_widget_id)['yMin'] - 10 < target['y'] < qh.get_widgets(inv_widget_id)[
                        'yMax'] + 10
    target_on_chat_buttons = qh.get_widgets(chat_buttons_widget_id)['xMin'] < target['x'] < \
                             qh.get_widgets(chat_buttons_widget_id)['xMax'] and \
                             qh.get_widgets(chat_buttons_widget_id)['yMin'] - 25 < target['y'] < \
                             qh.get_widgets(chat_buttons_widget_id)['yMax'] + 25
    target_on_minimap = qh.get_widgets(minimap_widget_id)['xMin'] < target['x'] < qh.get_widgets(minimap_widget_id)[
        'xMax'] and \
                        qh.get_widgets(minimap_widget_id)['yMin'] < target['y'] < qh.get_widgets(minimap_widget_id)[
                            'yMax']
    return target_on_canvas and not target_on_inv and not target_on_minimap and not target_on_chat_buttons


def interact_with_object(
        door_id, coord_type, coord_value, greater_than, obj_dist=15,
        intermediate_tile=None, obj_type='game', timeout=0.1, custom_exit_function=None, custom_exit_function_arg=None,
        pre_interact=None, obj_tile=None, right_click_option=None
):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_objects_v2(obj_type, {door_id})
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    if intermediate_tile:
        qh.set_tiles({intermediate_tile})
    while True:
        qh.query_backend()
        target_obj = qh.get_objects_v2(obj_type, door_id, obj_dist)
        if target_obj and obj_tile:
            target_obj = list(
                filter(lambda obj: obj['x_coord'] == obj_tile['x'] and obj['y_coord'] == obj_tile['y'], target_obj)
            )
        if not custom_exit_function:
            if greater_than and qh.get_player_world_location(coord_type) >= coord_value:
                return
            elif not greater_than and qh.get_player_world_location(coord_type) <= coord_value:
                return
        else:
            if custom_exit_function_arg is not None and custom_exit_function(custom_exit_function_arg):
                return True
            elif custom_exit_function_arg is None and custom_exit_function():
                return True

        if target_obj and (datetime.datetime.now() - last_click).total_seconds() > timeout:
            if pre_interact:
                pre_interact()
            if right_click_option is None:
                osrs.move.fast_click_v2(target_obj[0])
                last_click = datetime.datetime.now()
            else:
                success = osrs.move.right_click_v6(target_obj[0], right_click_option, qh.get_canvas())
                if success:
                    last_click = datetime.datetime.now()
        elif intermediate_tile and qh.get_tiles(intermediate_tile) and not target_obj:
            osrs.move.fast_click_v2(qh.get_tiles(intermediate_tile))


def interact_with_multiple_objects(
        obj_ids, coord_type, coord_value, greater_than,
        intermediate_tile=None, obj_type='game', timeout=0.1, custom_exit_function=None, custom_exit_function_arg=None,
        pre_interact=None, obj_tile=None, right_click_option=None
):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_objects_v2(obj_type, obj_ids)
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    if intermediate_tile:
        qh.set_tiles({intermediate_tile})
    while True:
        qh.query_backend()
        target_obj = qh.get_objects_v2(obj_type)
        closest = False
        if target_obj and obj_tile:
            target_obj = list(
                filter(lambda obj: obj['x_coord'] == obj_tile['x'] and obj['y_coord'] == obj_tile['y'], target_obj)
            )
        if target_obj:
            closest = osrs.util.find_closest_target(target_obj)
        if not custom_exit_function:
            if greater_than and qh.get_player_world_location(coord_type) >= coord_value:
                return
            elif not greater_than and qh.get_player_world_location(coord_type) <= coord_value:
                return
        else:
            if custom_exit_function_arg is not None and custom_exit_function(custom_exit_function_arg):
                return True
            elif custom_exit_function_arg is None and custom_exit_function():
                return True

        if closest and (datetime.datetime.now() - last_click).total_seconds() > timeout:
            if pre_interact:
                pre_interact()
            if right_click_option is None:
                osrs.move.fast_click_v2(closest)
                last_click = datetime.datetime.now()
            else:
                success = osrs.move.right_click_v6(closest, right_click_option, qh.get_canvas())
                if success:
                    last_click = datetime.datetime.now()
        elif intermediate_tile and qh.get_tiles(intermediate_tile) and not target_obj:
            osrs.move.fast_click_v2(qh.get_tiles(intermediate_tile))


def go_to_loc(
        dest_x, dest_y, dest_z=0, right_click=False, exact_tile=False,
        skip_dax=False, exit_on_dest=False, player_loc=None
):
    x_min = dest_x - 3
    y_min = dest_y - 3
    x_max = dest_x + 3
    y_max = dest_y + 3
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_destination_tile()
    qh.set_tiles({f'{dest_x},{dest_y},{dest_z}'})
    while True:
        qh.query_backend()
        if (x_min <= qh.get_player_world_location('x') <= x_max
                and y_min <= qh.get_player_world_location('y') <= y_max
                and not exact_tile):
            break
        elif exact_tile and qh.get_player_world_location('x') == dest_x and qh.get_player_world_location('y') == dest_y:
            break
        elif qh.get_destination_tile() \
                and qh.get_destination_tile()['x'] == dest_x \
                and qh.get_destination_tile()['y'] == dest_y:
            if exit_on_dest:
                last_tile = None
                time_on_tile = datetime.datetime.now()
                while True:
                    qh.query_backend()
                    if qh.get_player_world_location('x') == dest_x and qh.get_player_world_location('y') == dest_y:
                        osrs.dev.logger.info("Arrived at destination.")
                        return
                    elif qh.get_player_world_location() != last_tile:
                        last_tile = qh.get_player_world_location()
                        time_on_tile = datetime.datetime.now()
                    elif (datetime.datetime.now() - time_on_tile).total_seconds() > 1:
                        osrs.dev.logger.info("Timed out trying to go to loc")
                        break
            continue
        elif qh.get_tiles(f'{dest_x},{dest_y},{dest_z}') and is_clickable(qh.get_tiles(f'{dest_x},{dest_y},{dest_z}')):
            if right_click:
                osrs.move.right_click_v6(
                    qh.get_tiles(f'{dest_x},{dest_y},{dest_z}'),
                    'Walk here',
                    qh.get_canvas(),
                    in_inv=True
                )
            else:
                osrs.move.fast_click(qh.get_tiles(f'{dest_x},{dest_y},{dest_z}'))
        else:
            osrs.move.follow_path(
                qh.get_player_world_location(), {'x': dest_x, 'y': dest_y, 'z': dest_z},
                right_click=right_click, exact_tile=exact_tile, skip_dax=skip_dax, player_loc=player_loc
            )


def tab_to_varrock():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    last_tab = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        # in varrock center
        if 3195 <= qh.get_player_world_location('x') <= 3226 and 3419 <= qh.get_player_world_location(
                'y') <= 3438:
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            return
        elif qh.get_inventory(osrs.item_ids.VARROCK_TELEPORT) and (datetime.datetime.now() - last_tab).total_seconds() > 10:
            osrs.move.click(qh.get_inventory(osrs.item_ids.VARROCK_TELEPORT))
            last_tab = datetime.datetime.now()


def initialize_query_helper(obj_id, obj_type, intermediate_tile):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_right_click_menu()
    qh.set_objects_v2(obj_type, {obj_id} if isinstance(obj_id, int) else set(obj_id))
    if intermediate_tile:
        qh.set_tiles({intermediate_tile})
    return qh


def should_exit(qh, coord_type, coord_value, greater_than, custom_exit_function, custom_exit_function_arg):
    if coord_type is not None and coord_value is not None:
        player_location = qh.get_player_world_location(coord_type)
        if (greater_than and player_location >= coord_value) or (
                not greater_than and player_location <= coord_value):
            return True
    if custom_exit_function:
        return custom_exit_function(
            custom_exit_function_arg
        ) if custom_exit_function_arg is not None else custom_exit_function()
    return False


def handle_interaction(
        qh, target_obj, last_click, pre_interact,
        pre_interact_arg, timeout, right_click_option, in_inv=False, conditional_click=None
):
    current_time = datetime.datetime.now()
    if (current_time - last_click).total_seconds() > timeout:
        if pre_interact:
            pre_interact(pre_interact_arg) if pre_interact_arg else pre_interact()

        if right_click_option:
            success = osrs.move.right_click_v6(target_obj[0], right_click_option, qh.get_canvas(), in_inv=in_inv)
            if success:
                last_click = current_time
        elif conditional_click is not None:
            osrs.move.instant_move(target_obj)
            if qh.get_right_click_menu() and qh.get_right_click_menu()['entries']:
                for option in qh.get_right_click_menu()['entries']:
                    if option[0] == conditional_click and str(option[1]) == str(target_obj['id']):
                        pyautogui.click()
                        return True
        else:
            osrs.move.fast_click_v2(target_obj[0])
            last_click = current_time
    return last_click


def interact_with_object_v3(
        obj_id, coord_type=None, coord_value=None, greater_than=True, obj_dist=15,
        intermediate_tile=None, obj_type='game', timeout=0.1,
        custom_exit_function=None, custom_exit_function_arg=None,
        pre_interact=None, obj_tile=None, right_click_option=None,
        pre_interact_arg=None,
        conditional_click=None
):
    """
    Interacts with objects in the game world based on given parameters.

    :param conditional_click: the desired left click option if necessary
    :param obj_id: int or set :: 12345 || {1234, 687}
    :param coord_type: char :: 'x' || 'y' || 'z'
    :param coord_value: int :: 1234
    :param greater_than: bool :: True || False
    :param obj_dist: int :: 10
    :param intermediate_tile: tile string :: '3456,3453,3'
    :param obj_type: 'wall' || 'game' || 'ground' || 'decorative' || 'ground_items'
    :param timeout: int (seconds) :: 3
    :param custom_exit_function: function()
    :param custom_exit_function_arg: single arg or list of args
    :param pre_interact: function()
    :param obj_tile: tile object :: {'x': 1234, 'y': 3456, 'z': 0}
    :param right_click_option: string :: 'Take'
    :param pre_interact_arg: any :: arguments to pass to the pre interact function
    :return: None
    """

    # Main function logic
    qh = initialize_query_helper(obj_id, obj_type, intermediate_tile)
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)

    while True:
        qh.query_backend()
        target_obj = qh.get_objects_v2(obj_type, dist=obj_dist)

        if target_obj:
            target_obj = sorted(target_obj, key=lambda obj: obj['dist'])
            if obj_tile:
                target_obj = [obj for obj in target_obj if
                              obj['x_coord'] == obj_tile['x'] and obj['y_coord'] == obj_tile['y']]

        if should_exit(qh, coord_type, coord_value, greater_than, custom_exit_function, custom_exit_function_arg):
            return True

        if target_obj:
            last_click = handle_interaction(
                qh, target_obj, last_click, pre_interact, pre_interact_arg, timeout, right_click_option, conditional_click
            )
        elif intermediate_tile and qh.get_tiles(intermediate_tile):
            osrs.move.fast_click_v2(qh.get_tiles(intermediate_tile))


def interact_with_widget_v3(
        widget_id, timeout=3,
        custom_exit_function=None, custom_exit_function_arg=None,
        pre_interact=None, right_click_option=None,
        pre_interact_arg=None
):
    """
    Interacts with objects in the game world based on given parameters.

    :param widget_id: int or set :: 12345 || {1234, 687}
    :param coord_type: char :: 'x' || 'y' || 'z'
    :param timeout: int (seconds) :: 3
    :param custom_exit_function: function()
    :param custom_exit_function_arg: single arg or list of args
    :param pre_interact: function()
    :param right_click_option: string :: 'Take'
    :param pre_interact_arg: any :: arguments to pass to the pre interact function
    :return: None
    """

    qh = osrs.queryHelper.QueryHelper()
    qh.set_canvas()
    qh.set_widgets({widget_id} if isinstance(widget_id, str) else set(widget_id))
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)

    while True:
        if pre_interact is not None:
            pre_interact()
        qh.query_backend()
        target_widget = qh.get_widgets()

        if target_widget:
            target_widget = osrs.util.combine_objects(target_widget)

        if custom_exit_function_arg is not None and custom_exit_function(custom_exit_function_arg):
            return True
        elif custom_exit_function_arg is None and custom_exit_function():
            return True

        if target_widget:
            last_click = handle_interaction(
                qh, target_widget, last_click, None, None,
                timeout, right_click_option, in_inv=True
            )


def handle_npc_interaction(
        qh, target_obj, last_click, timeout, right_click_option, in_inv=False
):
    current_time = datetime.datetime.now()
    if (current_time - last_click).total_seconds() > timeout:
        if right_click_option:
            success = osrs.move.right_click_v6(target_obj, right_click_option, qh.get_canvas(), in_inv=in_inv)
            if success:
                last_click = current_time
        else:
            osrs.move.fast_click_v2(target_obj)
            last_click = current_time
    return last_click


def interact_with_npc(
        npc_id, timeout=3,
        custom_exit_function=None, custom_exit_function_arg=None,
        pre_interact=None, right_click_option=None, additional_filter=None, exit_on_interact=False, exit_on_dialogue=False
):

    qh = osrs.queryHelper.QueryHelper()
    qh.set_canvas()
    qh.set_npcs(npc_id if type(npc_id) is list else [npc_id])
    qh.set_player_world_location()
    qh.set_interating_with()
    qh.set_widgets({osrs.widget_ids.main_chat_widget})
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)

    while True:
        if pre_interact is not None:
            pre_interact()
        qh.query_backend()
        target_npcs = qh.get_npcs()

        if target_npcs:
            target_npcs = osrs.util.find_closest_target_in_game(
                target_npcs,
                qh.get_player_world_location(),
                additional_filter=additional_filter if additional_filter is not None else None
            )

        if custom_exit_function_arg is not None and custom_exit_function(custom_exit_function_arg):
            osrs.dev.logger.info('NPC handler configured to exit with custom func and arg and succeeded.')
            return True
        elif custom_exit_function_arg is None and custom_exit_function and custom_exit_function():
            osrs.dev.logger.info('NPC handler configured to exit with custom func (no arg) and succeeded.')
            return True
        elif exit_on_interact and qh.get_interating_with():
            osrs.dev.logger.info('NPC handler configured to exit on interact, have interaction. Exiting.')
            return True
        elif exit_on_dialogue \
                and qh.get_widgets(osrs.widget_ids.main_chat_widget) \
                and not qh.get_widgets(osrs.widget_ids.main_chat_widget)['isHidden']:
            osrs.dev.logger.info('NPC handler configured to exit on dialogue, found dialogue. Exiting.')
            return True

        if target_npcs:
            last_click = handle_npc_interaction(
                qh, target_npcs, last_click,
                timeout, right_click_option, in_inv=True
            )


def conditional_click(qh: osrs.queryHelper.QueryHelper, obj, action, target_field='name'):
    if not obj or not action or not qh:
        return

    action_found = (qh.get_right_click_menu()
                    and qh.get_right_click_menu()['entries']
                    and action in qh.get_right_click_menu()['entries'][-1][0])
    target_found = False
    for item in qh.get_right_click_menu()['entries'][-1]:
        if str(obj[target_field]) in item:
            target_found = True
            break
    if action_found and target_found:
        pyautogui.click()
    elif obj:
        osrs.move.instant_move(obj)
        qh.query_backend()
        action_found = (qh.get_right_click_menu()
                        and qh.get_right_click_menu()['entries']
                        and action in qh.get_right_click_menu()['entries'][-1][0])
        target_found = False
        for item in qh.get_right_click_menu()['entries'][-1]:
            if str(obj[target_field]) in item:
                target_found = True
                break
        if action_found and target_found:
            pyautogui.click()