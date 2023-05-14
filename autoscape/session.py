import datetime

import general_utils


def break_every_hour(max_run, start_time=-1):
    if start_time == -1:
        start_time = datetime.datetime.now()
    general_utils.random_sleep(0.5, 0.9)
    run_time = (datetime.datetime.now() - start_time).total_seconds()
    print('Current Script Runtime: ', run_time, '. Maximum Script Runtime: ', max_run * 60)
    if run_time > max_run * 60:
        return True
    else:
        return False


def logout(port='56799'):
    LOGOUT_ICON = {
        'widget': '161,52'
    }
    LOGOUT_BUTTON = {
        'widget': '182,12'
    }
    WORLD_SWITCHER_LOGOUT = {
        'widget': '69,23'
    }
    icon = general_utils.query_game_data(LOGOUT_ICON, port)
    move_and_click(icon['widget']['x'], icon['widget']['y'], 10, 10)
    general_utils.random_sleep(1, 1.4)
    logout_button = general_utils.query_game_data(LOGOUT_BUTTON, port)
    if 'widget' in logout_button:
        move_and_click(logout_button['widget']['x'], logout_button['widget']['y'], 10, 10)
        general_utils.random_sleep(0.3, 0.4)
    else:
        logout_button = general_utils.query_game_data(WORLD_SWITCHER_LOGOUT, port)
        move_and_click(logout_button['widget']['x'], logout_button['widget']['y'], 10, 10)
        general_utils.random_sleep(0.3, 0.4)


def mac_login(pw, port):
    move_and_click(805, 315, 1, 1)
    general_utils.random_sleep(1, 2)
    general_utils.type_something(get_config(pw))
    move_and_click(635, 345, 1, 1)
    general_utils.random_sleep(1, 2)
    coords = {
        'x': 0,
        'y': 0
    }

    while True:
        q = {
            'widget': '378,72'
        }
        widget = query_game_data(q, port)
        if 'widget' in widget:
            ctp = widget['widget']
            # once the click to play button is loaded, it takes a couple seconds to get accurate coords
            # due to some underlying game mechanics (i guess)
            if ctp['x'] == coords['x'] and ctp['y'] == coords['y']:
                move_and_click(ctp['x'], ctp['y'], 15, 15)
                break
            else:
                coords['x'] = ctp['x']
                coords['y'] = ctp['y']
        random_sleep(0.6, 0.7)


def login(password, port='56799'):
    if platform.system() == 'Darwin': return mac_login(password, port)
    existing_user_paths = {
        'Linux': '../screens/existing_user.png',
        'Windows': 'C:\\Users\\gland\\osrs_yolov3\\screens\\existing_user.png'
    }
    login_paths = {
        'Linux': '../screens/login.png',
        'Windows': 'C:\\Users\\gland\\osrs_yolov3\\screens\\login_button.png'
    }
    existing_user = rough_img_compare(existing_user_paths[platform.system()], 0.8,
                                      (0, 0, 1920, 1080))
    while True:
        existing_user = rough_img_compare(existing_user_paths[platform.system()], 0.8,
                                          (0, 0, 1920, 1080))
        if existing_user:
            break
        time.sleep(1)
    move_and_click(
        existing_user[0] + math.floor(existing_user[2] / 4),
        existing_user[1] + math.floor(existing_user[3] / 4),
        math.floor(existing_user[2] / 4),
        math.floor(existing_user[3] / 4)
    )
    random_sleep(1, 2)
    type_something(get_config(password))
    random_sleep(0.2, 0.4)
    login_button = rough_img_compare(login_paths[platform.system()], 0.8,
                                     (0, 0, 1920, 1080))
    while True:
        login_button = rough_img_compare(login_paths[platform.system()], 0.8,
                                         (0, 0, 1920, 1080))
        if login_button:
            break
        time.sleep(1)
    move_and_click(
        login_button[0] + math.floor(login_button[2] / 4),
        login_button[1] + math.floor(login_button[3] / 4),
        math.floor(login_button[2] / 4),
        math.floor(login_button[3] / 4)
    )

    coords = {
        'x': 0,
        'y': 0
    }

    while True:
        q = {
            'widget': '378,72'
        }
        widget = query_game_data(q, port)
        if 'widget' in widget:
            ctp = widget['widget']
            # once the click to play button is loaded, it takes a couple seconds to get accurate coords
            # due to some underlying game mechanics (i guess)
            if ctp['x'] == coords['x'] and ctp['y'] == coords['y']:
                move_and_click(ctp['x'], ctp['y'], 15, 15)
                break
            else:
                coords['x'] = ctp['x']
                coords['y'] = ctp['y']
        random_sleep(0.6, 0.7)


def set_timings(timings, current_time):
    config['timings']['script_start'] = current_time
    config['timings']['break_start'] = current_time + datetime.timedelta(
        minutes=random.randint(timings['min_session'], timings['max_session'])
    )
    config['timings']['break_end'] = config['timings']['break_start'] + datetime.timedelta(
        minutes=random.randint(timings['min_rest'], timings['max_rest'])
    )


def break_manager_v2(script_config):
    """
    :param script_config: Object
    {
        'intensity': 'high' | 'low',
        'logout': function(), -- Steps to run before logging out for break
        'login': function(), -- Steps to run after logging back in
    }
    """
    current_time = datetime.datetime.now()
    timings = config['{}_intensity_script'.format(script_config['intensity'])]
    # Initialize timings on script start
    if not config['timings']['script_start']:
        set_timings(timings, current_time)
    # Begin break period
    if current_time > config['timings']['break_start'] and not config['timings']['on_break']:
        if script_config.logout:
            script_config.logout()
        logout()
        config['timings']['on_break'] = True
    elif config['timings']['break_start'] < current_time < config['timings']['break_end'] \
            and config['timings']['on_break']:
        move_and_click(500, 500, 5, 5)
        random_sleep(10, 15)
    elif current_time > config['timings']['break_end'] \
            and config['timings']['on_break']:
        login(get_config(config.password))
        if script_config.login:
            script_config.login()
        set_timings(timings, current_time)

    # if curr time is greater than break_time, begin break -- need to differentiate between these two states, probably should have an
    # on_break boolean
    # if curr time is between break start and break end, continue break
    # if curr time is greater than break end, refresh script_start, break_start, and break_end, then run any login and post login steps
def break_manager(start_time, min_session, max_session, min_rest, max_rest, password, post_login_steps=None, port='56799', pre_logout_steps=None):
    take_break = break_every_hour(random.randint(min_session, max_session), start_time)
    if take_break:
        print('Taking extended break, signing off.')
        if pre_logout_steps:
            pre_logout_steps()
        random_sleep(20, 30)
        logout(port)
        break_start_time = datetime.datetime.now()
        while (datetime.datetime.now() - break_start_time).total_seconds() < random.randint(min_rest, max_rest):
            print(
                'Break has currently run for: ',
                (datetime.datetime.now() - break_start_time).total_seconds(),
                ' and can run for up to: ',
                max_rest
            )
            time.sleep(30)
            click_off_screen()
        login(password, port)
        random_sleep(0.4, 0.5)
        if post_login_steps:
            post_login_steps()
        return datetime.datetime.now()
    return start_time


def multi_break_manager(start_time, min_session, max_session, min_rest, max_rest, acc_configs):
    take_break = break_every_hour(random.randint(min_session, max_session), start_time)
    if take_break:
        print('Taking extended break, signing off. Current time: ', datetime.datetime.now())
        random_sleep(20, 30)
        for acc in acc_configs:
            print(acc)
            logout(acc['port'])
            random_sleep(3, 3.1)
            if len(acc_configs) > 1:
                with keyboard.pressed(Key.alt):
                    keyboard.press(Key.tab)
                    keyboard.release(Key.tab)
        break_start_time = datetime.datetime.now()
        while (datetime.datetime.now() - break_start_time).total_seconds() < random.randint(min_rest, max_rest):
            print(
                'Break has currently run for: ',
                (datetime.datetime.now() - break_start_time).total_seconds(),
                ' and can run for up to: ',
                max_rest
            )
            time.sleep(30)
            click_off_screen(200, 250, 200, 250)
        for acc in acc_configs:
            login(acc['password'], acc['port'])
            if len(acc_configs) > 1:
                with keyboard.pressed(Key.alt):
                    keyboard.press(Key.tab)
                    keyboard.release(Key.tab)
            random_sleep(3, 3.1)
        random_sleep(0.4, 0.5)
        for acc in acc_configs:
            if acc['post_login_steps']:
                acc['post_login_steps']()
                if len(acc_configs) > 1:
                    with keyboard.pressed(Key.alt):
                        keyboard.press(Key.tab)
                        keyboard.release(Key.tab)
                random_sleep(3, 3.1)
        return datetime.datetime.now()
    return start_time
