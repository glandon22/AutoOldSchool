import datetime
import math
import random
import time

import osrs.move
import osrs.server as server
import osrs.clock as clock
import secret_keepr
import osrs.keeb as keeb
import osrs.move as move
import osrs.dev as dev
import osrs.queryHelper as QueryHelper

config = dev.load_yaml()


class ScriptConfiguration(object):
    def __init__(self, intensity, login, logout):
        self.config = {
            'intensity': intensity,
            'login': login,
            'logout': logout
        }
    low = 'low'
    high = 'high'

def login_v2(password, port='56799'):
    keeb.keyboard.press(keeb.Key.enter)
    keeb.keyboard.release(keeb.Key.enter)
    clock.sleep_one_tick()
    p = secret_keepr.get_config(password)
    keeb.keyboard.type(p)
    clock.sleep_one_tick()
    keeb.keyboard.press(keeb.Key.enter)
    keeb.keyboard.release(keeb.Key.enter)
    coords = {
        'x': 0,
        'y': 0
    }

    while True:
        q = {
            'widget': '378,72'
        }
        widget = server.query_game_data(q, port)
        if 'widget' in widget:
            ctp = widget['widget']
            # once the click to play button is loaded, it takes a couple seconds to get accurate coords
            # due to some underlying game mechanics (i guess)
            if ctp['x'] == coords['x'] and ctp['y'] == coords['y']:
                move.move_and_click(ctp['x'], ctp['y'], 15, 15)
                break
            else:
                coords['x'] = ctp['x']
                coords['y'] = ctp['y']
        clock.random_sleep(0.6, 0.7)


def login_v3(ctp=True):
    keeb.keyboard.press(keeb.Key.enter)
    keeb.keyboard.release(keeb.Key.enter)
    print('press first enter')
    clock.sleep_one_tick()
    clock.sleep_one_tick()
    keeb.keyboard.type(config['password'])
    print('type pass')
    clock.sleep_one_tick()
    clock.sleep_one_tick()
    keeb.keyboard.press(keeb.Key.enter)
    keeb.keyboard.release(keeb.Key.enter)
    print('press second enter')
    coords = {
        'x': 0,
        'y': 0
    }
    if ctp:
        while True:
            q = {
                'widget': '378,72'
            }
            widget = server.query_game_data(q, config['port'])
            if 'widget' in widget:
                ctp = widget['widget']
                # once the click to play button is loaded, it takes a couple seconds to get accurate coords
                # due to some underlying game mechanics (i guess)
                if ctp['x'] == coords['x'] and ctp['y'] == coords['y']:
                    move.move_and_click(ctp['x'], ctp['y'], 15, 15)
                    break
                else:
                    coords['x'] = ctp['x']
                    coords['y'] = ctp['y']
            clock.random_sleep(0.6, 0.7)


def login_v4():
    qh = QueryHelper.QueryHelper()
    qh.set_canvas()
    qh.set_game_state()
    while True:
        qh.query_backend()
        canvas = qh.get_canvas()
        x = math.floor((canvas['xMax'] + canvas['xMin']) / 2)
        # Game image is a fixed size, only black space is added horizontally as UI scales
        y = canvas['yMin'] + 251
        # add this click below to clear any unexpected interfaces. i.e. world was full
        osrs.move.click({'x': x, 'y': y + 50})
        osrs.move.click({'x': x, 'y': y})
        osrs.clock.sleep_one_tick()
        qh.query_backend()
        if qh.get_game_state() == 'LOGGING_IN' or qh.get_game_state() == 'LOADING':
            print(f'Log in stats: {qh.get_game_state()}')
            continue
        elif qh.get_game_state() == 'LOGGED_IN':
            keeb.keyboard.press(keeb.Key.esc)
            keeb.keyboard.release(keeb.Key.esc)
            clock.sleep_one_tick()
            return


def logout(port='56799'):
    LOGOUT_ICON = {
        'widget': '161,46'
    }
    LOGOUT_BUTTON = {
        'widget': '182,12'
    }
    WORLD_SWITCHER_LOGOUT = {
        'widget': '69,25'
    }
    icon = server.query_game_data(LOGOUT_ICON, port)
    move.move_and_click(icon['widget']['x'], icon['widget']['y'], 10, 10)
    clock.random_sleep(1, 1.4)
    logout_button = server.query_game_data(LOGOUT_BUTTON, port)
    if 'widget' in logout_button:
        move.move_and_click(logout_button['widget']['x'], logout_button['widget']['y'], 3, 3)
        clock.random_sleep(0.3, 0.4)
    else:
        logout_button = server.query_game_data(WORLD_SWITCHER_LOGOUT, port)
        move.move_and_click(logout_button['widget']['x'], logout_button['widget']['y'], 3, 3)
        clock.random_sleep(0.3, 0.4)
    print('logged out')


def break_manager(start_time, min_session, max_session, min_rest, max_rest, password, post_login_steps=None, port='56799', pre_logout_steps=None):
    take_break = clock.break_every_hour(random.randint(min_session, max_session), start_time)
    if take_break:
        print('Taking extended break, signing off.')
        if pre_logout_steps:
            pre_logout_steps()
        clock.random_sleep(20, 30)
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
            move.click_off_screen(500, 510, 500, 510)
        login_v2(password, port)
        clock.random_sleep(0.4, 0.5)
        if post_login_steps:
            post_login_steps()
        return datetime.datetime.now()
    return start_time


def multi_break_manager(start_time, min_session, max_session, min_rest, max_rest, acc_configs):
    take_break = clock.break_every_hour(random.randint(min_session, max_session), start_time)
    if take_break:
        print('Taking extended break, signing off. Current time: ', datetime.datetime.now())
        clock.random_sleep(20, 30)
        for acc in acc_configs:
            logout(acc['port'])
            clock.random_sleep(3, 3.1)
            if len(acc_configs) > 1:
                with keeb.keyboard.pressed(keeb.Key.alt):
                    keeb.keyboard.press(keeb.Key.tab)
                    keeb.keyboard.release(keeb.Key.tab)
        break_start_time = datetime.datetime.now()
        while (datetime.datetime.now() - break_start_time).total_seconds() < random.randint(min_rest, max_rest):
            print(
                'Break has currently run for: ',
                (datetime.datetime.now() - break_start_time).total_seconds(),
                ' and can run for up to: ',
                max_rest
            )
            time.sleep(30)
            move.click_off_screen(200, 250, 200, 250)
        for acc in acc_configs:
            login_v2(acc['password'], acc['port'])
            if len(acc_configs) > 1:
                with keeb.keyboard.pressed(keeb.Key.alt):
                    keeb.keyboard.press(keeb.Key.tab)
                    keeb.keyboard.release(keeb.Key.tab)
            clock.random_sleep(3, 3.1)
        clock.random_sleep(0.4, 0.5)
        for acc in acc_configs:
            if acc['post_login_steps']:
                acc['post_login_steps']()
                if len(acc_configs) > 1:
                    with keeb.keyboard.pressed(keeb.Key.alt):
                        keeb.keyboard.press(keeb.Key.tab)
                        keeb.keyboard.release(keeb.Key.tab)
                clock.random_sleep(3, 3.1)
        return datetime.datetime.now()
    return start_time


def set_timings(timings, current_time):
    config['timings']['script_start'] = current_time
    config['timings']['break_start'] = current_time + datetime.timedelta(
        seconds=random.randint(timings['min_session'] * 60, timings['max_session'] * 60)
    )
    config['timings']['break_end'] = config['timings']['break_start'] + datetime.timedelta(
        seconds=random.randint(timings['min_rest'] * 60, timings['max_rest'] * 60)
    )


# experimental
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
        print('current config: {}'.format(config))


    # Begin break period
    if current_time > config['timings']['break_start'] and not config['timings']['on_break']:
        # Run pre-logout logic supplied by script
        if script_config['logout']:
            script_config['logout']()
        logout()
        config['timings']['on_break'] = True
    elif config['timings']['break_start'] < current_time < config['timings']['break_end'] \
            and config['timings']['on_break']:
        move.move_and_click(500, 500, 5, 5)
        clock.random_sleep(10, 15)
    elif current_time > config['timings']['break_end'] \
            and config['timings']['on_break']:
        login_v3()
        # Run post-login logic supplied by script
        if script_config['login']:
            script_config['login']()
        set_timings(timings, current_time)
        config['timings']['on_break'] = False


def break_manager_v3(script_config):
    """
    :param script_config: Object
    {
        'intensity': 'high' | 'low',
        'logout': function(), -- Steps to run before logging out for break
        'login': function(), -- Steps to run after logging back in
        'click_to_play': True | False -> Instances like Tithe Farm dont display this button after login
    }
    """
    current_time = datetime.datetime.now()
    timings = config['{}_intensity_script'.format(script_config['intensity'])]
    # Initialize timings on script start
    if not config['timings']['script_start']:
        set_timings(timings, current_time)
        print('current config: {}'.format(config))

    # Begin break period
    if current_time > config['timings']['break_start']:
        # Run pre-logout logic supplied by script
        if script_config['logout']:
            script_config['logout']()
        logout()
        config['timings']['break_end'] = datetime.datetime.now() + datetime.timedelta(
            minutes=random.randint(timings['min_rest'], timings['max_rest'])
        )
        while True:
            if datetime.datetime.now() < config['timings']['break_end']:
                move.move_and_click(500, 750, 5, 5)
                clock.random_sleep(10, 15)
            else:
                break
        if 'click_to_play' in script_config:
            login_v3('click_to_play' in script_config and script_config['click_to_play'])
        else:
            login_v3()
        # Run post-login logic supplied by script
        if script_config['login']:
            script_config['login']()
        set_timings(timings, datetime.datetime.now())
    return config


def break_manager_v4(script_config):
    """
    :param script_config: Object
    {
        'intensity': 'high' | 'low',
        'logout': function(), -- Steps to run before logging out for break
        'login': function(), -- Steps to run after logging back in
        'click_to_play': True | False -> Instances like Tithe Farm dont display this button after login
    }
    """
    current_time = datetime.datetime.now()
    timings = config['{}_intensity_script'.format(script_config['intensity'])]
    # Initialize timings on script start
    if not config['timings']['script_start']:
        set_timings(timings, current_time)
        print('current config: {}'.format(config))

    # Begin break period
    if current_time > config['timings']['break_start']:
        # Run pre-logout logic supplied by script
        if script_config['logout']:
            script_config['logout']()
        logout()
        config['timings']['break_end'] = datetime.datetime.now() + datetime.timedelta(
            minutes=random.randint(timings['min_rest'], timings['max_rest'])
        )
        while True:
            if datetime.datetime.now() < config['timings']['break_end']:
                move.move_and_click(500, 223, 5, 5)
                clock.random_sleep(10, 15)
            else:
                break
        login_v4()
        # Run post-login logic supplied by script
        if script_config['login']:
            script_config['login']()
        set_timings(timings, datetime.datetime.now())
    return config