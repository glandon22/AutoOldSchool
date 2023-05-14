import datetime

from autoscape import general_utils

port = '56799'
course_start = {
    'x': 3103,
    'y': 3276,
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
                'tile': '3103,3279,0',
                'object': '11404'
            }]
        }
        data = general_utils.query_game_data(q)
        if 'decorativeObjects' in data and '11404' in data['decorativeObjects']:
            general_utils.move_and_click(data['decorativeObjects']['11404'][0]['x'],
                                         data['decorativeObjects']['11404'][0]['y'], 2, 2)
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
    if 'z' in loc and loc['z'] == 3 and 3097 <= loc['x'] <= 3102 and 3277 <= loc['y'] <= 3281 and click_allowed(lc, 3, 2):
        general_utils.handle_marks(3097, 3102, 3277, 3281, 3, port)
        obstacle = general_utils.get_ground_object('3098,3277,3', '11405', port)
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
    if 'z' in loc and loc['z'] == 3 and 3087 <= loc['x'] <= 3093 and 3272 <= loc['y'] <= 3278 and click_allowed(lc, 3, 3):
        general_utils.handle_marks(3087, 3093, 3272, 3278, 3, port)
        obstacle = general_utils.get_ground_object('3092,3276,3', '11406', port)
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
    if 'z' in loc and loc['z'] == 3 and 3089 <= loc['x'] <= 3094 and 3265 <= loc['y'] <= 3268 and click_allowed(lc, 3, 4):
        general_utils.handle_marks(3089, 3094, 3265, 3268, 3, port)
        obstacle = general_utils.get_game_object('3089,3264,3', '11430', port)
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
    if 'z' in loc and loc['z'] == 3 and 3083 <= loc['x'] <= 3088 and 3256 <= loc['y'] <= 3261 and click_allowed(lc, 3, 5):
        general_utils.handle_marks(3083, 3088, 3256, 3261, 3, port)
        obstacle = general_utils.get_game_object('3088,3256,3', '11630', port)
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
    if 'z' in loc and loc['z'] == 3 and 3087 <= loc['x'] <= 3094 and 3252 <= loc['y'] <= 3255 and click_allowed(lc, 3, 6):
        general_utils.handle_marks(3087, 3094, 3252, 3255, 3, port)
        obstacle = general_utils.get_game_object('3095,3255,3', '11631', port)
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
    if 'z' in loc and loc['z'] == 3 and 3096 <= loc['x'] <= 3101 and 3256 <= loc['y'] <= 3261 and click_allowed(lc, 3, 7):
        general_utils.handle_marks(3096, 3101, 3256, 3261, 3, port)
        obstacle = general_utils.get_game_object('3102,3261,3', '11632', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.random_sleep(1, 1.2)
            return {
                'step': 7,
                'ts': datetime.datetime.now()
            }
    return lc


def main():
    last_click = {
        'step': 0,
        'ts': datetime.datetime.now()
    }
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 43, 48, 423, 551, 'julenth', False)
        general_utils.wait_until_stationary(port)
        last_click = start_course(last_click)
        last_click = platform_1(last_click)
        last_click = platform_2(last_click)
        last_click = platform_3(last_click)
        last_click = platform_4(last_click)
        last_click = platform_5(last_click)
        last_click = platform_6(last_click)

main()