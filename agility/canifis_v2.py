import datetime

from autoscape import general_utils

port = '56799'
course_start = {
    'x': 3506,
    'y': 3486,
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
    if 'z' in loc and loc['z'] == 0 and click_allowed(lc, 10, 1):
        q = {
            'tiles': ['3508,3489,0']
        }
        data = general_utils.query_game_data(q)
        if 'tiles' in data and '350834890' in data['tiles']:
            general_utils.move_and_click(data['tiles']['350834890']['x'],
                                         data['tiles']['350834890']['y'], 2, 2)
            general_utils.sleep_one_tick()
            return {
                'step': 1,
                'ts': datetime.datetime.now()
            }
        else:
            general_utils.run_towards_square(course_start, port)
    return lc


def platform_1(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 2 and 3504 <= loc['x'] <= 3511 and 3491 <= loc['y'] <= 3497 and click_allowed(lc, 3, 2):
        general_utils.handle_marks(3504, 3511, 3491, 3497, 2, port)
        obstacle = general_utils.get_game_object('3506,3498,2', '14844', port)
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
    if 'z' in loc and loc['z'] == 2 and 3496 <= loc['x'] <= 3504 and 3503 <= loc['y'] <= 3507 and click_allowed(lc, 3, 3):
        general_utils.handle_marks(3496, 3504, 3503, 3507, 2, port)
        obstacle = general_utils.get_game_object('3496,3504,2', '14845', port)
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
    if 'z' in loc and loc['z'] == 2 and \
            3485 <= loc['x'] <= 3493 and \
            3498 <= loc['y'] <= 3505 and \
            click_allowed(lc, 4, 4):
        general_utils.sleep_one_tick()
        general_utils.handle_marks(3485, 3493, 3498, 3505, 2, port)
        obstacle = general_utils.get_game_object('3485,3499,2', '14848', port)
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
    if 'z' in loc and loc['z'] == 3 and\
            3474 <= loc['x'] <= 3480 and \
            3491 <= loc['y'] <= 3500 and \
            click_allowed(lc, 3, 5):
        general_utils.handle_marks(3474, 3480, 3491, 3500, 3, port)
        obstacle = general_utils.get_game_object('3478,3491,3', '14846', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 5,
                'ts': datetime.datetime.now()
            }
    return lc

# may need a longer timeout here becasue the animation is weird
def platform_5(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 2 and \
            3477 <= loc['x'] <= 3484 and \
            3481 <= loc['y'] <= 3487 and \
            click_allowed(lc, 3, 6):
        general_utils.handle_marks(3477, 3484, 3481, 3487, 2, port)
        obstacle = general_utils.get_game_object('3480,3483,2', '14894', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 6,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_6(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3488 <= loc['x'] <= 3503 and \
            3468 <= loc['y'] <= 3478 and \
            click_allowed(lc, 6, 7):
        general_utils.handle_marks(3488, 3503, 3468, 3478, 3, port)
        obstacle = general_utils.get_game_object('3504,3476,3', '14847', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 7,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_7(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 2 and \
            3508 <= loc['x'] <= 3516 and \
            3474 <= loc['y'] <= 3483 and \
            click_allowed(lc, 3, 8):
        general_utils.handle_marks(3508, 3516, 3474, 3483, 2, port)
        obstacle = general_utils.get_game_object('3510,3483,2', '14897', port)
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
        general_utils.sleep_one_tick()
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

main()