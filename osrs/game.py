import datetime
import math
import random
import time
import re

import osrs.move
import osrs.server as server
import osrs.clock as clock
import osrs.keeb as keeb
import osrs.move as move
import osrs.dev as dev
import osrs.queryHelper as QueryHelper

config = dev.load_yaml()

main_chat_widget = '162,34'
quest_complete_widget = '153,4'


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
    p = config['password']
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
        print(f'Log in status: {qh.get_game_state()}')
        if qh.get_game_state() == 'LOGGING_IN' or qh.get_game_state() == 'LOADING':
            continue
        elif qh.get_game_state() == 'LOGGED_IN':
            clock.sleep_one_tick()
            keeb.keyboard.press(keeb.Key.esc)
            keeb.keyboard.release(keeb.Key.esc)
            clock.sleep_one_tick()
            return
        canvas = qh.get_canvas()
        x = math.floor((canvas['xMax'] + canvas['xMin']) / 2)
        # Game image is a fixed size, only black space is added horizontally as UI scales
        y = math.floor((canvas['yMin'] + 500) / 2)
        # add this click below to clear any unexpected interfaces. i.e. world was full
        osrs.move.click({'x': x, 'y': y + 50})
        osrs.move.click({'x': x, 'y': y})
        osrs.clock.sleep_one_tick()
        qh.query_backend()


def logout():
    logout_icon_widget_id = '161,46'
    logout_button_widget_id = '182,12'
    world_switcher_logout_widget_id = '69,25'

    qh = QueryHelper.QueryHelper()
    qh.set_widgets({logout_icon_widget_id, logout_button_widget_id, world_switcher_logout_widget_id})
    qh.set_game_state()
    clicked_first_button = False
    while True:
        qh.query_backend()
        if qh.get_game_state() == 'LOGIN_SCREEN':
            return
        if clicked_first_button:
            if qh.get_widgets(logout_button_widget_id):
                osrs.move.click(qh.get_widgets(logout_button_widget_id))
                osrs.clock.random_sleep(8, 8.1)
            if qh.get_widgets(world_switcher_logout_widget_id):
                osrs.move.click(qh.get_widgets(world_switcher_logout_widget_id))
                osrs.clock.random_sleep(8, 8.1)
        if qh.get_widgets(logout_icon_widget_id) and not clicked_first_button:
            osrs.move.click(qh.get_widgets(logout_icon_widget_id))
            clicked_first_button = True


def break_manager(start_time, min_session, max_session, min_rest, max_rest, password, post_login_steps=None,
                  port='56799', pre_logout_steps=None):
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
    # dont run the script over night
    if config['timings']['break_start'].hour >= 21:
        config['timings']['break_end'] = config['timings']['break_start'] + datetime.timedelta(
            seconds=random.randint(timings['min_rest'] * 60, timings['max_rest'] * 60)
        ) + datetime.timedelta(hours=8)
    else:
        config['timings']['break_end'] = config['timings']['break_start'] + datetime.timedelta(
            seconds=random.randint(timings['min_rest'] * 60, timings['max_rest'] * 60)
        )
    print(config['timings']['break_end'])


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
    took_break = False
    current_time = datetime.datetime.now()
    timings = config['{}_intensity_script'.format(script_config['intensity'])]
    # Initialize timings on script start
    if not config['timings']['script_start']:
        set_timings(timings, current_time)
        print('current config: {}'.format(config))

    # Begin break period
    if current_time > config['timings']['break_start']:
        took_break = True
        # Run pre-logout logic supplied by script
        if script_config['logout']:
            script_config['logout']()
        logout()
        config['timings']['break_end'] += datetime.timedelta(
            seconds=(current_time - config['timings']['break_start']).total_seconds())
        print(f"logging back in at: {config['timings']['break_end']}")
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
    return {**config, 'took_break': took_break}


# this simulates the login logout functionality for rapid testing
def break_manager_debugging(script_config):
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
        set_timings(timings, current_time - datetime.timedelta(hours=777))
        print('current config: {}'.format(config))

    # Begin break period
    if current_time > config['timings']['break_start']:
        # Run pre-logout logic supplied by script
        if script_config['logout']:
            script_config['logout']()
        logout()
        # log right back in
        config['timings']['break_end'] = datetime.datetime.now()
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


def tele_home():
    while True:
        osrs.keeb.press_key('f6')
        osrs.clock.random_sleep(0.2, 0.3)
        home_tele_button = osrs.server.get_widget('218,31')
        if home_tele_button:
            osrs.move.move_and_click(home_tele_button['x'], home_tele_button['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = osrs.server.get_world_location()
                if loc and loc['x'] > 4000:
                    osrs.clock.random_sleep(2, 2.3)
                    osrs.keeb.press_key('esc')
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 15:
                    break


def tele_home_v2():
    def pre():
        osrs.keeb.press_key('f6')

    def in_house():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_objects_v2('game', {4525})
        qh.query_backend()
        # ensure i am in house and see portal, otherwise i cant tele out of an instance bc my x value is already large
        if qh.get_player_world_location('x') > 3967 and qh.get_objects_v2('game', 4525):
            osrs.keeb.press_key('esc')
            return True

    osrs.move.interact_with_widget_v3(
        osrs.widget_ids.house_poh_tele_widget_id,
        custom_exit_function=in_house,
        pre_interact=pre
    )


def cast_spell(widget):
    while True:
        osrs.keeb.press_key('f6')
        osrs.clock.random_sleep(0.2, 0.3)
        home_tele_button = osrs.server.get_widget(widget)
        if home_tele_button:
            osrs.move.move_and_click(home_tele_button['x'], home_tele_button['y'], 3, 3)
            osrs.keeb.press_key('esc')
            break
    osrs.keeb.press_key('esc')


def tele_home_fairy_ring(code):
    def widget_up():
        qh1 = osrs.queryHelper.QueryHelper()
        qh1.set_widgets_v2({osrs.widget_ids.FAIRY_RING_TELEPORT_BUTTON})
        qh1.query_backend()
        if qh1.get_widgets_v2(osrs.widget_ids.FAIRY_RING_TELEPORT_BUTTON):
            return True

    instructions = [
        [],
        [],
        []
    ]
    if code[0] == 'b':
        instructions[0] += [-5]
    elif code[0] == 'c':
        instructions[0] += [5]
        instructions[0] += [5]
    elif code[0] == 'd':
        instructions[0] += [5]

    if code[1] == 'j':
        instructions[1] += [-5]
    elif code[1] == 'k':
        instructions[1] += [5]
        instructions[1] += [5]
    elif code[1] == 'l':
        instructions[1] += [5]

    if code[2] == 'q':
        instructions[2] += [-5]
    elif code[2] == 'r':
        instructions[2] += [5]
        instructions[2] += [5]
    elif code[2] == 's':
        instructions[2] += [5]

    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_widgets_v2({
        osrs.widget_ids.FAIRY_RING_TELEPORT_BUTTON,
        osrs.widget_ids.FAIRY_RING_LEFT_WHEEL_CENTER,
        osrs.widget_ids.FAIRY_RING_MIDDLE_WHEEL_CENTER,
        osrs.widget_ids.FAIRY_RING_RIGHT_WHEEL_CENTER,
    })
    osrs.move.interact_with_object_v3(
        29228, right_click_option='Configure', timeout=7, custom_exit_function=widget_up
    )
    while True:
        qh.query_backend()
        if qh.get_widgets_v2(osrs.widget_ids.FAIRY_RING_TELEPORT_BUTTON):
            # Each instruction set is for a wheel of the fairy ring interface. it always opens with A I P selected.
            # I add 50px to the y value to move from the center of the wheel widget to the letter where i click to turn
            for op in instructions[0]:
                osrs.move.click({
                    'x': qh.get_widgets_v2(osrs.widget_ids.FAIRY_RING_LEFT_WHEEL_CENTER)['x'] + op,
                    'y': qh.get_widgets_v2(osrs.widget_ids.FAIRY_RING_LEFT_WHEEL_CENTER)['y'] + 50
                })
            for op in instructions[1]:
                osrs.move.click({
                    'x': qh.get_widgets_v2(osrs.widget_ids.FAIRY_RING_MIDDLE_WHEEL_CENTER)['x'] + op,
                    'y': qh.get_widgets_v2(osrs.widget_ids.FAIRY_RING_MIDDLE_WHEEL_CENTER)['y'] + 50
                })
            for op in instructions[2]:
                osrs.move.click({
                    'x': qh.get_widgets_v2(osrs.widget_ids.FAIRY_RING_RIGHT_WHEEL_CENTER)['x'] + op,
                    'y': qh.get_widgets_v2(osrs.widget_ids.FAIRY_RING_RIGHT_WHEEL_CENTER)['y'] + 50
                })
            osrs.move.click(qh.get_widgets_v2(osrs.widget_ids.FAIRY_RING_TELEPORT_BUTTON))
            return


def player_healed():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({osrs.widget_ids.run_energy_widget_id})
    qh.set_skills({'hitpoints', 'prayer', 'attack', 'strength', 'defence'})
    qh.query_backend()
    if int(qh.get_widgets(osrs.widget_ids.run_energy_widget_id)['text']) > 95 and \
            qh.get_skills('hitpoints')['level'] <= qh.get_skills('hitpoints')['boostedLevel'] and \
            qh.get_skills('attack')['level'] <= qh.get_skills('attack')['boostedLevel'] and \
            qh.get_skills('strength')['level'] <= qh.get_skills('strength')['boostedLevel'] and \
            qh.get_skills('prayer')['level'] <= qh.get_skills('prayer')['boostedLevel'] and \
            qh.get_skills('defence')['level'] <= qh.get_skills('defence')['boostedLevel']:
        return True


def click_restore_pool():
    osrs.move.interact_with_object_v3(
        29241,
        custom_exit_function=player_healed
    )


def hop_worlds(pre_hop=False, total_level_worlds=True):
    world_list = [
        421,
        422,
        485,
        486,
        487,
        488,
        489,
        490,
    ]

    if total_level_worlds:
        world_list += [
            420,
            467,
            349,
            361,
            396,
            428,
            527,
        ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_state()
    qh.set_world()
    qh.query_backend()
    index = qh.get_world() in world_list and world_list.index(qh.get_world())
    print('i', index)
    if index is False or index == len(world_list) - 1:
        index = -1
    print('ii', index, world_list[index + 1])
    osrs.keeb.press_key('enter')
    if pre_hop:
        pre_hop()
    command = f'::hop {world_list[index + 1]}'
    print('entering command: ', command)
    osrs.keeb.write(command)
    osrs.keeb.press_key('enter')
    osrs.clock.random_sleep(2, 2.1)
    while True:
        qh.query_backend()
        if qh.get_game_state() == 'LOGGED_IN':
            clock.sleep_one_tick()
            keeb.press_key('esc')
            return


def talk_to_npc(name, right_click=False, right_click_option='Talk-to', custom_exit=None):
    qh = osrs.queryHelper.QueryHelper()
    if type(name) is str:
        qh.set_npcs_by_name([name])
    elif type(name) is int:
        qh.set_npcs([str(name)])
    qh.set_chat_options()
    qh.set_widgets({main_chat_widget})
    qh.set_canvas()
    while True:
        qh.query_backend()
        if qh.get_chat_options() or qh.get_widgets(main_chat_widget) or (custom_exit is not None and custom_exit()):
            return
        elif qh.get_npcs_by_name():
            if right_click:
                osrs.move.right_click_v6(qh.get_npcs_by_name()[0], right_click_option, qh.get_canvas(), in_inv=True)
            else:
                osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif qh.get_npcs():
            if right_click:
                osrs.move.right_click_v6(qh.get_npcs()[0], right_click_option, qh.get_canvas(), in_inv=True)
            else:
                osrs.move.fast_click(qh.get_npcs_by_name()[0])


def dialogue_handler(desired_replies=None, timeout=3):
    npc_chat_head_widget = '231,4'
    player_chat_widget = '217,6'
    chat_holder_widget = '231,0'
    chat_holder2_widget = '217,1'
    click_to_continue_widget = '229,2'
    click_to_continue_level_widget = '233,2'
    click_to_continue_other_widget = '193,0,2'
    #
    # quest_complete_widget = '153,4'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_widgets({
        npc_chat_head_widget, player_chat_widget,
        chat_holder_widget, chat_holder2_widget,
        click_to_continue_widget, main_chat_widget, click_to_continue_level_widget,
        click_to_continue_other_widget
    })
    had_dialogue = False
    dialogue_last_seen = datetime.datetime.now()
    while True:
        qh.query_backend()
        if (
                not qh.get_widgets(main_chat_widget)
                or (qh.get_widgets(main_chat_widget) and qh.get_widgets(main_chat_widget)['isHidden'])
        ):
            if (datetime.datetime.now() - dialogue_last_seen).total_seconds() > timeout:
                return had_dialogue
        else:
            print('here')
            dialogue_last_seen = datetime.datetime.now()

        if desired_replies:
            for reply in desired_replies:
                if qh.get_chat_options(reply):
                    osrs.keeb.write(str(qh.get_chat_options(reply)))
                    had_dialogue = True
        if (qh.get_widgets(player_chat_widget)
                or qh.get_widgets(npc_chat_head_widget)
                or qh.get_widgets(click_to_continue_level_widget)
                or qh.get_widgets(click_to_continue_other_widget)
                or qh.get_widgets(click_to_continue_widget)):
            osrs.keeb.press_key('space')
            had_dialogue = True


def use_portal_nexus(destination):
    # get the character to press to tele to dest
    pattern = '(?<=\>)(.*?)(?=\<)'
    nexus_id = 33354
    dest_list_widget = '17,12'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {nexus_id})
    qh.set_widgets({dest_list_widget})
    qh.set_player_world_location()
    qh.set_canvas()
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') < 4000:
            return
        elif qh.get_widgets(dest_list_widget):
            for i in range(31):
                widget = f"17,12,{i}"
                qh1 = osrs.queryHelper.QueryHelper()
                qh1.set_widgets({widget})
                qh1.query_backend()
                if qh1.get_widgets(widget) and destination.lower() in qh1.get_widgets(widget)['text'].lower():
                    char = re.search(pattern, qh1.get_widgets(widget)['text'].lower())
                    if char and char.group(0):
                        osrs.keeb.write(str(char.group(0)))
        elif qh.get_objects_v2('game', nexus_id) and (datetime.datetime.now() - last_click).total_seconds() > 7:
            osrs.move.right_click_v6(
                qh.get_objects_v2('game', nexus_id)[0],
                'Teleport menu',
                qh.get_canvas()
            )
            last_click = datetime.datetime.now()


def slow_lumb_tele():
    def pre():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_widgets({'161,65'})
        qh.query_backend()
        if qh.get_widgets('161,65') and qh.get_widgets('161,65')['spriteID'] != 1027:
            osrs.keeb.press_key('f6')
            osrs.clock.random_sleep(0.2, 0.3)

    def in_house():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_objects_v2('game', {4525})
        qh.query_backend()
        # ensure i am in house and see portal, otherwise i cant tele out of an instance bc my x value is already large
        if 3197 <= qh.get_player_world_location('x') <= 3236 and 3204 <= qh.get_player_world_location('y') <= 3234:
            osrs.keeb.press_key('esc')
            return True

    osrs.move.interact_with_widget_v3(
        osrs.widget_ids.home_tele_slow_widget_id,
        custom_exit_function=in_house,
        pre_interact=pre,
        right_click_option='Cast',
        timeout=30
    )


def skills_tele(dest):
    '''

    :param dest: Fishing || Mining || Crafting || Cooking || Woodcutting || Farming
    :return:
    '''

    locs = {
        'Fishing': [2601, 2625, 3381, 3408],
        'Mining': [3044, 3060, 9753, 9771],
        'Crafting': [2924, 2947, 2934, 3304],
        'Cooking': [3134, 3157, 3434, 3466],
        'Woodcutting': [1655, 31669, 3496, 3519],
        'Farming': [1243, 1255, 3715, 3739],
    }
    def pre():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_widgets({'161,63'})
        qh.query_backend()
        if qh.get_widgets('161,63') or qh.get_widgets('161,63')['spriteID'] != 1030:
            osrs.keeb.press_key('f4')

    def in_dest():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_objects_v2('game', {4525})
        qh.set_widgets({'387,17,1'})
        qh.query_backend()
        if locs[dest][0] <= qh.get_player_world_location('x') <= locs[dest][1] \
                and locs[dest][2] <= qh.get_player_world_location('y') <= locs[dest][3]:
            osrs.keeb.press_key('esc')
            osrs.dev.logger.info(f'Successfully teled on skills necklace to {dest} Guild.')
            return True
        elif qh.get_widgets('387,17,1') and qh.get_widgets('387,17,1')['itemID'] not in [
            osrs.item_ids.SKILLS_NECKLACE1,
            osrs.item_ids.SKILLS_NECKLACE2,
            osrs.item_ids.SKILLS_NECKLACE3,
            osrs.item_ids.SKILLS_NECKLACE4,
            osrs.item_ids.SKILLS_NECKLACE5,
            osrs.item_ids.SKILLS_NECKLACE6,
        ]:
            osrs.dev.logger.warning('Tried to use skills necklace to tele without having one equipped')
            return True


    osrs.move.interact_with_widget_v3(
        '387,17,1',
        custom_exit_function=in_dest,
        pre_interact=pre,
        right_click_option=f"{dest} Guild",
        timeout=15
    )


def dueling_tele(dest):
    '''

    :param dest: Arena || Castle || Ferox || Fortis
    :return:
    '''

    locs = {
        "Emir's Arena": [3310, 3329, 3224, 32407],
        'Castle Wars': [2434, 2446, 3081, 3099],
        'Ferox Enclave': [3117, 3160, 3615, 3648],
        #'Fortis': [3134, 3157, 3434, 3466]
    }
    def pre():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_widgets({'161,63'})
        qh.query_backend()
        if qh.get_widgets('161,63') or qh.get_widgets('161,63')['spriteID'] != 1030:
            osrs.keeb.press_key('f4')

    def in_dest():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_objects_v2('game', {4525})
        qh.set_widgets({'387,24,1'})
        qh.query_backend()
        if locs[dest][0] <= qh.get_player_world_location('x') <= locs[dest][1] \
                and locs[dest][2] <= qh.get_player_world_location('y') <= locs[dest][3]:
            osrs.keeb.press_key('esc')
            osrs.dev.logger.info(f'Successfully teled on ring of dueling to {dest}.')
            return True
        elif qh.get_widgets('387,24,1') and qh.get_widgets('387,24,1')['itemID'] not in [
            osrs.item_ids.RING_OF_DUELING1,
            osrs.item_ids.RING_OF_DUELING2,
            osrs.item_ids.RING_OF_DUELING3,
            osrs.item_ids.RING_OF_DUELING4,
            osrs.item_ids.RING_OF_DUELING5,
            osrs.item_ids.RING_OF_DUELING6,
            osrs.item_ids.RING_OF_DUELING7,
            osrs.item_ids.RING_OF_DUELING8,

        ]:
            osrs.dev.logger.warning('Tried to use ring of dueling to tele without having one equipped')
            return True


    osrs.move.interact_with_widget_v3(
        '387,24,1',
        custom_exit_function=in_dest,
        pre_interact=pre,
        right_click_option=dest,
        timeout=15
    )


def standard_spells_tele(dest):
    '''

    :param dest: Varrock || Ardougne || Camelot || Falador
    :return:
    '''

    locs = {
        'Varrock': [3201, 3227, 3418, 3438],
        'Ardougne': [2650, 2672, 3292, 3319],
        'Camelot': [2743, 2772, 3467, 3487],
        'Falador': [2956, 2972, 3371, 3394]
    }
    widget_map = {
        'Varrock': osrs.widget_ids.varrock_tele_widget_id,
        'Ardougne': osrs.widget_ids.ardy_tele_spell_widget_id,
        'Camelot': osrs.widget_ids.camelot_tele_spell_widget_id,
        'Falador': osrs.widget_ids.fally_tele_widget_id
    }
    def pre():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_widgets({osrs.widget_ids.home_tele_slow_widget_id})
        qh.query_backend()
        if not qh.get_widgets(osrs.widget_ids.home_tele_slow_widget_id):
            osrs.keeb.press_key('f6')

    def in_dest():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_objects_v2('game', {4525})
        qh.set_widgets({widget_map[dest]})
        qh.query_backend()
        if locs[dest][0] <= qh.get_player_world_location('x') <= locs[dest][1] \
                and locs[dest][2] <= qh.get_player_world_location('y') <= locs[dest][3]:
            osrs.keeb.press_key('esc')
            osrs.dev.logger.info(f'Successfully teled on standard spell book to {dest}.')
            return True

    osrs.move.interact_with_widget_v3(
        widget_map[dest],
        custom_exit_function=in_dest,
        pre_interact=pre,
        right_click_option='Cast',
        timeout=32
    )