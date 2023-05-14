import datetime

from autoscape import general_utils

port = '56799'
course_start = {
    'x': 2729,
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
    if 'z' in loc and loc['z'] == 0 and click_allowed(lc, 3, 1):
        general_utils.sleep_one_tick()
        q = {
            'decorativeObjects': [{
                'tile': '2729,3489,0',
                'object': '14927'
            }]
        }
        data = general_utils.query_game_data(q)
        if 'decorativeObjects' in data and '14927' in data['decorativeObjects']:
            general_utils.move_and_click(data['decorativeObjects']['14927'][0]['x'],
                                         data['decorativeObjects']['14927'][0]['y'], 2, 2)
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
            2721 <= loc['x'] <= 2730 and \
            3490 <= loc['y'] <= 3497 and \
            click_allowed(lc, 4, 2):
        general_utils.handle_marks(2721, 2730, 3490, 3497, 3, port)
        obstacle = general_utils.get_game_object('2720,3494,3', '14928', port)
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
    if 'z' in loc and loc['z'] == 2 and \
            2704 <= loc['x'] <= 2714 and \
            3487 <= loc['y'] <= 3498 and \
            click_allowed(lc, 3, 3):
        general_utils.handle_marks(2704, 2714, 3487, 3498, 2, port)
        obstacle = general_utils.get_ground_object('2710,3489,2', '14932', port)
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
            2709 <= loc['x'] <= 2716 and \
            3476 <= loc['y'] <= 3482 and \
            click_allowed(lc, 4, 4):
        general_utils.handle_marks(2709, 2716, 3476, 3482, 2, port)
        obstacle = general_utils.get_game_object('2711,3476,2', '14929', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 4,
                'ts': datetime.datetime.now()
            }
    return lc

# animation causes an additional delay on this step
def platform_4(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            2699 <= loc['x'] <= 2716 and \
            3469 <= loc['y'] <= 3476 and \
            click_allowed(lc, 4, 5):
        general_utils.sleep_one_tick()
        general_utils.sleep_one_tick()
        general_utils.handle_marks(2699, 2716, 3469, 3476, 3, port)
        obstacle = general_utils.get_game_object('2701,3469,3', '14930', port)
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
    if 'z' in loc and loc['z'] == 2 and \
            2691 <= loc['x'] <= 2703 and \
            3459 <= loc['y'] <= 3466 and \
            click_allowed(lc, 3, 6):
        general_utils.handle_marks(2691, 2703, 3459, 3466, 2, port)
        obstacle = general_utils.get_game_object('2703,3463,2', '14931', port)
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
            3026 <= loc['x'] <= 3029 and \
            3352 <= loc['y'] <= 3355 and \
            click_allowed(lc, 5, 7):
        general_utils.handle_marks(3026, 3029, 3352, 3355, 3, port)
        obstacle = general_utils.get_ground_object('3026,3353,3', '14911', port)
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
    if 'z' in loc and loc['z'] == 3 and \
            3009 <= loc['x'] <= 3021 and \
            3353 <= loc['y'] <= 3358 and \
            click_allowed(lc, 3, 8):
        general_utils.handle_marks(3009, 3021, 3353, 3358, 3, port)
        obstacle = general_utils.get_game_object('3018,3352,3', '14919', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 8,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_8(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3016 <= loc['x'] <= 3022 and \
            3343 <= loc['y'] <= 3349 and \
            click_allowed(lc, 3, 9):
        general_utils.handle_marks(3016, 3022, 3343, 3349, 3, port)
        obstacle = general_utils.get_game_object('3015,3345,3', '14920', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 9,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_9(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3011 <= loc['x'] <= 3014 and \
            3344 <= loc['y'] <= 3346 and \
            click_allowed(lc, 3, 10):
        general_utils.handle_marks(3011, 3014, 3344, 3346, 3, port)
        obstacle = general_utils.get_game_object('3012,3343,3', '14921', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 10,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_10(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3009 <= loc['x'] <= 3013 and \
            3335 <= loc['y'] <= 3342 and \
            click_allowed(lc, 3, 11):
        general_utils.handle_marks(3009, 3013, 3335, 3342, 3, port)
        obstacle = general_utils.get_game_object('3014,3335,3', '14923', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 11,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_11(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3012 <= loc['x'] <= 3018 and \
            3331 <= loc['y'] <= 3334 and \
            click_allowed(lc, 3, 12):
        general_utils.handle_marks(3012, 3018, 3331, 3334, 3, port)
        obstacle = general_utils.get_game_object('3018,3333,3', '14924', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 12,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_12(lc):
    loc = general_utils.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3019 <= loc['x'] <= 3024 and \
            3332 <= loc['y'] <= 3335 and \
            click_allowed(lc, 3, 13):
        general_utils.handle_marks(3019, 3024, 3332, 3335, 3, port)
        obstacle = general_utils.get_game_object('3024,3333,3', '47195', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 13,
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
        last_click = platform_7(last_click)
        last_click = platform_8(last_click)
        last_click = platform_9(last_click)
        last_click = platform_10(last_click)
        last_click = platform_11(last_click)
        last_click = platform_12(last_click)

main()