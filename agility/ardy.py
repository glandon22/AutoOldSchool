import datetime

from autoscape import general_utils

port = '56799'
course_start = {
    'x': 2673,
    'y': 3298,
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
        general_utils.sleep_one_tick()
        q = {
            'decorativeObjects': [{
                'tile': '2673,3298,0',
                'object': '15608'
            }]
        }
        data = general_utils.query_game_data(q)
        if 'decorativeObjects' in data and '15608' in data['decorativeObjects']:
            general_utils.move_and_click(data['decorativeObjects']['15608'][0]['x'],
                                         data['decorativeObjects']['15608'][0]['y'], 2, 2)
            general_utils.sleep_one_tick()
            general_utils.wait_until_stationary(port)
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
    if 'z' in loc and loc['z'] == 3 and \
            2671 <= loc['x'] <= 2672 and \
            3299 <= loc['y'] <= 3309 and \
            click_allowed(lc, 5, 2):
        obstacle = general_utils.get_game_object('2671,3310,3', '15609', port)
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
    if 'z' in loc and loc['z'] == 3 and \
            2661 <= loc['x'] <= 2665 and \
            3318 <= loc['y'] <= 3319 and \
            click_allowed(lc, 4, 3):
        # Additional animation delay
        general_utils.random_sleep(0.6, 0.7)
        obstacle = general_utils.get_ground_object('2661,3318,3', '26635', port)
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
    if 'z' in loc and loc['z'] == 3 and \
            2653 <= loc['x'] <= 2657 and \
            3318 <= loc['y'] <= 3319 and \
            click_allowed(lc, 4, 4):
        general_utils.handle_marks(2653, 2657, 3318, 3319, 3, port)
        obstacle = general_utils.get_game_object('2653,3318,3', '15610', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(0.6, 0.7)
            return {
                'step': 4,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_4(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            2653 <= loc['x'] <= 2654 and \
            3310 <= loc['y'] <= 3314 and \
            click_allowed(lc, 4, 5):
        obstacle = general_utils.get_game_object('2653,3309,3', '15611', port)
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
    if 'z' in loc and loc['z'] == 3 and \
            2651 <= loc['x'] <= 2653 and \
            3300 <= loc['y'] <= 3309 and \
            click_allowed(lc, 3, 6):
        # animatino delay
        general_utils.sleep_one_tick()
        obstacle = general_utils.get_game_object('2654,3300,3', '28912', port)
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
            2655 <= loc['x'] <= 2666 and \
            3297 <= loc['y'] <= 3297 and \
            click_allowed(lc, 5, 7):
        obstacle = general_utils.get_game_object('2656,3296,3', '15612', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 7,
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


def drink_wine():
    hp = general_utils.get_skill_data('hitpoints', port)
    if 'boostedLevel' in hp and hp['boostedLevel'] < 15:
        inv = general_utils.get_inv(port)
        wine = general_utils.is_item_in_inventory_v2(inv, '1993')
        if not wine:
            exit('out of wine')
        general_utils.move_and_click(wine['x'], wine['y'], 3, 3)


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
        drink_wine()
        last_click = start_course(last_click)
        last_click = platform_1(last_click)
        last_click = platform_2(last_click)
        last_click = platform_3(last_click)
        last_click = platform_4(last_click)
        last_click = platform_5(last_click)
        last_click = platform_6(last_click)

print(general_utils.break_manager_v2({'intensity': 'high'}))