import datetime


import osrs

port = '56799'
course_start = {
    'x': 3351,
    'y': 2960,
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
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 0 and click_allowed(lc, 3, 1):
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()
        obstacle = osrs.server.get_game_object('3351,2962,0', '14935', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.sleep_one_tick()
            osrs.move.wait_until_stationary(port)
            osrs.clock.sleep_one_tick()
            return {
                'step': 1,
                'ts': datetime.datetime.now()
            }
        else:
            osrs.move.run_towards_square_v2(course_start, port)
    return lc


def platform_1(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 1 and \
            3346 <= loc['x'] <= 3351 and \
            2963 <= loc['y'] <= 2968 and \
            click_allowed(lc, 4, 2):
        osrs.agil.handle_marks(3346, 3351, 2963, 2968, 1, port)
        obstacle = osrs.server.get_game_object('3350,2971,1', '14936', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 2,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_2(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 1 and \
            3352 <= loc['x'] <= 3355 and \
            2973 <= loc['y'] <= 2976 and \
            click_allowed(lc, 3, 3):
        osrs.agil.handle_marks(3352, 3355, 2973, 2976, 1, port)
        obstacle = osrs.server.get_game_object('3357,2978,1', '14937', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 3,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_3(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 1 and \
            3360 <= loc['x'] <= 3362 and \
            2977 <= loc['y'] <= 2979 and \
            click_allowed(lc, 4, 4):
        osrs.agil.handle_marks(3360, 3362, 2977, 2979, 1, port)
        obstacle = osrs.server.get_game_object('3364,2977,1', '14938', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(0.6, 0.7)
            return {
                'step': 4,
                'ts': datetime.datetime.now()
            }
    return lc

# animation causes an additional delay on this step
def platform_4(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 1 and \
            3366 <= loc['x'] <= 3370 and \
            2974 <= loc['y'] <= 2976 and \
            click_allowed(lc, 4, 4):
        osrs.agil.handle_marks(3366, 3370, 2974, 2976, 1, port)
        obstacle = osrs.server.get_game_object('3368,2977,1', '14939', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 5,
                'ts': datetime.datetime.now()
            }
    return lc

def platform_5(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 1 and \
            3365 <= loc['x'] <= 3369 and \
            2982 <= loc['y'] <= 2986 and \
            click_allowed(lc, 3, 6):
        osrs.agil.handle_marks(3365, 3369, 2982, 2986, 1, port)
        q = {
            'decorativeObjects': [{
                'tile': '3365,2982,1',
                'object': '14940'
            }]
        }
        data = osrs.server.query_game_data(q)
        if 'decorativeObjects' in data and '14940' in data['decorativeObjects']:
            osrs.move.move_and_click(data['decorativeObjects']['14940'][0]['x'],
                                         data['decorativeObjects']['14940'][0]['y'], 2, 2)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 6,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_6(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 2 and \
            3355 <= loc['x'] <= 3365 and \
            2980 <= loc['y'] <= 2985 and \
            click_allowed(lc, 5, 7):
        osrs.agil.handle_marks(3355, 3365, 2980, 2985, 2, port)
        obstacle = osrs.server.get_game_object('3358,2985,2', '14941', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 7,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_7(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 2 and \
            3357 <= loc['x'] <= 3370 and \
            2990 <= loc['y'] <= 2995 and \
            click_allowed(lc, 3, 8):
        osrs.agil.handle_marks(3357, 3370, 2990, 2995, 2, port)
        obstacle = osrs.server.get_game_object('3360,2997,2', '14944', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 8,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_8(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 2 and \
            3356 <= loc['x'] <= 3362 and \
            3000 <= loc['y'] <= 3004 and \
            click_allowed(lc, 3, 9):
        osrs.agil.handle_marks(3356, 3362, 3000, 3004, 2, port)
        obstacle = osrs.server.get_game_object('3364,3000,2', '14945', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 9,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_9(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3011 <= loc['x'] <= 3014 and \
            3344 <= loc['y'] <= 3346 and \
            click_allowed(lc, 3, 10):
        osrs.agil.handle_marks(3011, 3014, 3344, 3346, 3, port)
        obstacle = osrs.server.get_game_object('3012,3343,3', '14921', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 10,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_10(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3009 <= loc['x'] <= 3013 and \
            3335 <= loc['y'] <= 3342 and \
            click_allowed(lc, 3, 11):
        osrs.agil.handle_marks(3009, 3013, 3335, 3342, 3, port)
        obstacle = osrs.server.get_game_object('3014,3335,3', '14923', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 11,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_11(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3012 <= loc['x'] <= 3018 and \
            3331 <= loc['y'] <= 3334 and \
            click_allowed(lc, 3, 12):
        osrs.agil.handle_marks(3012, 3018, 3331, 3334, 3, port)
        obstacle = osrs.server.get_game_object('3018,3333,3', '14924', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 12,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_12(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3019 <= loc['x'] <= 3024 and \
            3332 <= loc['y'] <= 3335 and \
            click_allowed(lc, 3, 13):
        osrs.agil.handle_marks(3019, 3024, 3332, 3335, 3, port)
        obstacle = osrs.server.get_game_object('3024,3333,3', '47195', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 13,
                'ts': datetime.datetime.now()
            }
    return lc


def drink_stam():
    run_energy = osrs.server.get_widget('160,28', port)
    if run_energy and int(run_energy['text']) < 45:
        inv = osrs.inv.get_inv(port, True)
        stam = osrs.inv.are_items_in_inventory_v2(inv, [12631, 12629, 12627, 12625])
        if stam:
            osrs.move.move_and_click(stam['x'], stam['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.1)


def drink_wine():
    hp = osrs.server.get_skill_data('hitpoints', port)
    if 'boostedLevel' in hp and hp['boostedLevel'] < 2:
        inv = osrs.inv.get_inv(port)
        wine = osrs.inv.is_item_in_inventory_v2(inv, '26149')
        if not wine:
            exit('out of wine')
        osrs.move.move_and_click(wine['x'], wine['y'], 3, 3)


def main():
    last_click = {
        'step': 0,
        'ts': datetime.datetime.now()
    }
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 43, 48, 423, 551, 'julenth', False)
        osrs.move.wait_until_stationary(port)
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