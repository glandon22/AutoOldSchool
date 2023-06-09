import datetime


import osrs

port = '56799'
course_start = {
    'x': 3035,
    'y': 3340,
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
        q = {
            'decorativeObjects': [{
                'tile': '3036,3341,0',
                'object': '14898'
            }]
        }
        data = osrs.server.query_game_data(q)
        if 'decorativeObjects' in data and '14898' in data['decorativeObjects']:
            osrs.move.move_and_click(data['decorativeObjects']['14898'][0]['x'],
                                         data['decorativeObjects']['14898'][0]['y'], 2, 2)
            osrs.clock.sleep_one_tick()
            osrs.move.wait_until_stationary(port)
            osrs.clock.sleep_one_tick()
            return {
                'step': 1,
                'ts': datetime.datetime.now()
            }
        else:
            osrs.move.run_towards_square(course_start, port)
    return lc


def platform_1(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3035 <= loc['x'] <= 3040 and \
            3342 <= loc['y'] <= 3347 and \
            click_allowed(lc, 3, 2):
        osrs.agil.handle_marks(3035, 3040, 3342, 3347, 3, port)
        obstacle = osrs.server.get_game_object('3040,3343,3', '47195', port)
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
    if 'z' in loc and loc['z'] == 3 and \
            3044 <= loc['x'] <= 3051 and \
            3341 <= loc['y'] <= 3349 and \
            click_allowed(lc, 3, 3):
        osrs.agil.handle_marks(3044, 3051, 3341, 3349, 3, port)
        obstacle = osrs.server.get_game_object('3050,3350,3', '14901', port)
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
    if 'z' in loc and loc['z'] == 3 and \
            3048 <= loc['x'] <= 3051 and \
            3356 <= loc['y'] <= 3358 and \
            click_allowed(lc, 4, 4):
        osrs.agil.handle_marks(3048, 3051, 3356, 3358, 3, port)
        obstacle = osrs.server.get_game_object('3048,3359,3', '14903', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 4,
                'ts': datetime.datetime.now()
            }
    return lc

def platform_4(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3045 <= loc['x'] <= 3048 and \
            3361 <= loc['y'] <= 3367 and \
            click_allowed(lc, 3, 5):
        osrs.agil.handle_marks(3045, 3048, 3361, 3367, 3, port)
        obstacle = osrs.server.get_game_object('3044,3362,3', '14904', port)
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
    if 'z' in loc and loc['z'] == 3 and \
            3034 <= loc['x'] <= 3041 and \
            3361 <= loc['y'] <= 3364 and \
            click_allowed(lc, 3, 6):
        osrs.agil.handle_marks(3034, 3041, 3361, 3364, 3, port)
        obstacle = osrs.server.get_game_object('3034,3361,3', '14905', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 6,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_6(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            3026 <= loc['x'] <= 3029 and \
            3352 <= loc['y'] <= 3355 and \
            click_allowed(lc, 5, 7):
        osrs.agil.handle_marks(3026, 3029, 3352, 3355, 3, port)
        obstacle = osrs.server.get_ground_object('3026,3353,3', '14911', port)
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
    if 'z' in loc and loc['z'] == 3 and \
            3009 <= loc['x'] <= 3021 and \
            3353 <= loc['y'] <= 3358 and \
            click_allowed(lc, 3, 8):
        osrs.agil.handle_marks(3009, 3021, 3353, 3358, 3, port)
        obstacle = osrs.server.get_game_object('3018,3352,3', '14919', port)
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
    if 'z' in loc and loc['z'] == 3 and \
            3016 <= loc['x'] <= 3022 and \
            3343 <= loc['y'] <= 3349 and \
            click_allowed(lc, 3, 9):
        osrs.agil.handle_marks(3016, 3022, 3343, 3349, 3, port)
        obstacle = osrs.server.get_game_object('3015,3345,3', '14920', port)
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