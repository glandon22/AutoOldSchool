import datetime

from autoscape import general_utils

port = '56799'
course_start = {
    'x': 3222,
    'y': 3413,
    'z': 0
}


def click_allowed(lc, cd, step):
    print('lc', lc)
    # this is not the last clicked step
    if lc['step'] != step:
        return True
    now = datetime.datetime.now()
    if (now - lc['ts']).total_seconds() > cd:
        return True
    else:
        return False


def start_course(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 0 and click_allowed(lc, 3, 1):
        general_utils.run_towards_square(course_start, port)
        q = {
            'decorativeObjects': [{
                'tile': '3221,3414,0',
                'object': '14412'
            }]
        }
        data = general_utils.query_game_data(q)
        if 'decorativeObjects' in data and '14412' in data['decorativeObjects']:
            general_utils.move_and_click(data['decorativeObjects']['14412'][0]['x'],
                                         data['decorativeObjects']['14412'][0]['y'], 2, 2)
            general_utils.sleep_one_tick()
            general_utils.wait_until_stationary(port)
            general_utils.sleep_one_tick()
            return {
                'step': 1,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_1(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and 3214 <= loc['x'] <= 3219 and 3410 <= loc['y'] <= 3419 and click_allowed(lc, 3, 2):
        general_utils.handle_marks(3214, 3219, 3410, 3419, 3, port)
        obstacle = general_utils.get_game_object('3213,3414,3', '14413', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 2,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_2(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and 3201 <= loc['x'] <= 3209 and 3413 <= loc['y'] <= 3419 and click_allowed(lc, 3, 3):
        general_utils.handle_marks(3201, 3209, 3413, 3419, 3, port)
        obstacle = general_utils.get_game_object('3200,3416,3', '14414', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 3,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_3(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 1 and 3193 <= loc['x'] <= 3197 and 3416 <= loc['y'] <= 3416 and click_allowed(lc, 4, 4):
        general_utils.handle_marks(3193, 3197, 3416, 3416, 1, port)
        obstacle = general_utils.get_game_object('3192,3416,1', '14832', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 4,
                'ts': datetime.datetime.now()
            }
    return lc

def platform_4(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and 3182 <= loc['x'] <= 3201 and 3402 <= loc['y'] <= 3406 and click_allowed(lc, 3, 5):
        general_utils.handle_marks(3182, 3201, 3402, 3406, 3, port)
        obstacle = general_utils.get_game_object('3194,3401,3', '14833', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 5,
                'ts': datetime.datetime.now()
            }
    return lc

def platform_5(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and 3182 <= loc['x'] <= 3201 and 3386 <= loc['y'] <= 3398 and click_allowed(lc, 3, 6):
        general_utils.handle_marks(3182, 3201, 3386, 3398, 3, port)
        obstacle = general_utils.get_game_object('3209,3400,3', '14834', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 5,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_6(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and 3218 <= loc['x'] <= 3232 and 3393 <= loc['y'] <= 3402 and click_allowed(lc, 5, 7):
        general_utils.handle_marks(3218, 3232, 3393, 3402, 3, port)
        obstacle = general_utils.get_game_object('3233,3402,3', '14835', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 6,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_7(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and 3236 <= loc['x'] <= 3240 and 3403 <= loc['y'] <= 3408 and click_allowed(lc, 3, 8):
        general_utils.handle_marks(3236, 3240, 3403, 3408, 3, port)
        obstacle = general_utils.get_game_object('3237,3409,3', '14836', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 7,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_8(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and 3236 <= loc['x'] <= 3240 and 3410 <= loc['y'] <= 3415 and click_allowed(lc, 3, 9):
        general_utils.handle_marks(3236, 3240, 3410, 3415, 3, port)
        obstacle = general_utils.get_game_object('3236,3416,3', '14841', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 8,
                'ts': datetime.datetime.now()
            }
    return lc


def drink_stam():
    run_energy = general_utils.get_widget('160,28', port)
    if run_energy and int(run_energy['text']) < 45:
        inv = general_utils.get_inv(port, True)
        stam = general_utils.are_items_in_inventory_v2(inv, [12631, 12629, 12627, 12625])
        if stam:
            general_utils.move_and_click(stam['x'], stam['y'], 3, 3)
            general_utils.random_sleep(1, 1.1)

def main():
    last_click = {
        'step': 0,
        'ts': datetime.datetime.now()
    }
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 43, 48, 423, 551, 'julenth', False)
        general_utils.wait_until_stationary(port)
        drink_stam()
        last_click = start_course(last_click)
        last_click = platform_1(last_click)
        last_click = platform_2(last_click)
        last_click = platform_3(last_click)
        last_click = platform_4(last_click)
        last_click = platform_5(last_click)
        last_click = platform_6(last_click)
        last_click = platform_7(last_click)
        last_click = platform_8(last_click)

main()