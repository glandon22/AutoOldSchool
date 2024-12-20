import datetime

import pyautogui

import osrs
room = 1


def passed_traps(dest):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if dest['x_min'] <= qh.get_player_world_location('x') <= dest['x_max'] \
        and dest['y_min'] <= qh.get_player_world_location('y') <= dest['y_max']:
        osrs.dev.logger.debug('made it through with following points:')
        print(qh.get_player_world_location())
        print(dest)
        return True


def in_game():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_player_world_location('z') == 0 and qh.get_player_world_location('y') > 4000:
        return True


def completed_first(start_time):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'428,5'})
    qh.query_backend()
    if start_time and (datetime.datetime.now() - start_time).total_seconds() > 5:
        osrs.dev.logger.warning('Timed out trying to escape room 1 through door')
        return True
    elif qh.get_widgets('428,5') and 'Room 2' in qh.get_widgets('428,5')['text']:
        osrs.dev.logger.info('successfully made it through first floor.')
        return True


def completed_third(start_time):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'428,5'})
    qh.query_backend()
    if start_time and (datetime.datetime.now() - start_time).total_seconds() > 5:
        osrs.dev.logger.warning('Timed out trying to escape room 1 through door')
        return True
    elif qh.get_widgets('428,5') and 'Room 3' in qh.get_widgets('428,5')['text']:
        osrs.dev.logger.info('successfully made it through first floor.')
        return True


def first_room():
    for i in range(26618, 26621 + 1):
        start_time = datetime.datetime.now()
        osrs.move.interact_with_object_v3(
            i, custom_exit_function=completed_first, custom_exit_function_arg=start_time, obj_type='wall'
        )
        if completed_first(None):
            return


def completed_second(start_time):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'428,5'})
    qh.query_backend()
    if start_time and (datetime.datetime.now() - start_time).total_seconds() > 5:
        osrs.dev.logger.warning('Timed out trying to escape room 2 through door')
        return True
    elif qh.get_widgets('428,5') and 'Room 3' in qh.get_widgets('428,5')['text']:
        osrs.dev.logger.info('successfully made it through second floor.')
        return True


def second():
    for i in range(26618, 26621 + 1):
        start_time = datetime.datetime.now()
        osrs.move.interact_with_object_v3(
            i, custom_exit_function=completed_second, custom_exit_function_arg=start_time, obj_type='wall'
        )
        if completed_second(None):
            return


def searched_chest(start_time):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'428,5'})
    qh.query_backend()
    if start_time and (datetime.datetime.now() - start_time).total_seconds() > 5:
        osrs.dev.logger.warning('Timed out searching chest')
        return True


def into_next_room(target):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'428,5'})
    qh.set_right_click_menu()
    qh.query_backend()
    if qh.get_widgets('428,5') and f'Room {room}' in qh.get_widgets('428,5')['text']:
        osrs.dev.logger.info('successfully made it through floor %s.', room - 1)
        return True
    if target and qh.get_right_click_menu() and qh.get_right_click_menu()['entries']:
        for option in qh.get_right_click_menu()['entries']:
            if option[0] == 'Enter' and str(option[1]) == str(target):
                pyautogui.click()
                pyautogui.click()
                return True


def completed_room(exit_function):
    for i in range(26618, 26621 + 1):
        print('here342123434')
        osrs.dev.logger.debug('currently looking for door %s in room %s', i, room - 1)
        osrs.move.interact_with_object_v3(
            i, custom_exit_function=exit_function, obj_type='wall', custom_exit_function_arg=i
        )               
        if exit_function(None):
            break
    pots = osrs.combat_utils.PotConfig(antipoision=True, stamina=True).asdict()
    osrs.combat_utils.fast_food_handler(None, 40)
    osrs.combat_utils.pot_handler(None, pots, min_run=40)
    osrs.player.toggle_run('on')


def start():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['1779'])
    for i in range(26622, 26625 + 1):
        osrs.move.interact_with_object_v3(
            i, coord_type='z', coord_value=2, greater_than=True, right_click_option='Search', timeout=7
        )
        start_time = datetime.datetime.now()
        while True:
            qh.query_backend()
            if (datetime.datetime.now() - start_time).total_seconds() > 2:
                break
            elif qh.get_npcs():
                osrs.move.interact_with_npc(
                    '1779', right_click_option='Start-minigame', custom_exit_function=in_game
                )
                return
        osrs.move.interact_with_object_v3(
            20932, obj_type='wall', coord_type='z', coord_value=0, greater_than=False,
            right_click_option='Leave Tomb', timeout=7
        )


while True:
    osrs.game.break_manager_v4({
        'intensity':'high',
        'login': False,
        'logout': False
    })
    start()
    # room 1
    osrs.move.interact_with_object_v3(
        21280, conditional_click='Pass', custom_exit_function=passed_traps, timeout=7,
        custom_exit_function_arg={'x_min': 1927, 'x_max': 1928, 'y_min': 4470, 'y_max': 4471},
        obj_tile={'x': 1926, 'y': 4473, 'z': 0},
        pre_interact=lambda: osrs.move.go_to_loc(1927, 4474, exact_tile=True),
        right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 2
    osrs.move.interact_with_object_v3(
        21280, conditional_click='Pass', custom_exit_function=passed_traps, timeout=7,
        custom_exit_function_arg={'x_min': 1954, 'x_max': 1955, 'y_min': 4471, 'y_max': 4472},
        obj_tile={'x': 1953, 'y': 4474, 'z': 0},
        pre_interact=lambda: osrs.move.go_to_loc(1954, 4475, exact_tile=True),
        right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 3
    osrs.move.interact_with_object_v3(
        21280, conditional_click='Pass', custom_exit_function=passed_traps, timeout=7,
        custom_exit_function_arg={'x_min': 1976, 'x_max': 1977, 'y_min': 4463, 'y_max': 4464},
        obj_tile={'x': 1975, 'y': 4466, 'z': 0},
        pre_interact=lambda: osrs.move.go_to_loc(1976, 4467, exact_tile=True),
        right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 4
    osrs.move.interact_with_object_v3(
        21280, conditional_click='Pass', custom_exit_function=passed_traps, timeout=7,
        obj_tile={'x': 1930, 'y': 4454, 'z': 0},
        custom_exit_function_arg={'x_min': 1932, 'x_max': 1933, 'y_min': 4452, 'y_max': 4453},
        pre_interact=lambda: osrs.move.go_to_loc(1929, 4453, exact_tile=True),
        right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 5
    osrs.move.interact_with_object_v3(
        21280, conditional_click='Pass', custom_exit_function=passed_traps, timeout=7,
        obj_tile={'x': 1962, 'y': 4446, 'z': 0},
        pre_interact=lambda: osrs.move.go_to_loc(1963, 4445, exact_tile=True),
        custom_exit_function_arg={'x_min': 1959, 'x_max': 1960, 'y_min': 4444, 'y_max': 4445},
        right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 6
    osrs.move.interact_with_object_v3(
        21280, conditional_click='Pass', custom_exit_function=passed_traps, timeout=7,
        custom_exit_function_arg={'x_min': 1926, 'x_max': 1927, 'y_min': 4429, 'y_max': 4430},
        obj_tile={'x': 1925, 'y': 4427, 'z': 0},
        pre_interact=lambda: osrs.move.go_to_loc(1926, 4426, exact_tile=True),
        right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 7
    osrs.move.interact_with_object_v3(
        21280, conditional_click='Pass',
        obj_tile={'x': 1943, 'y': 4424, 'z': 0}, custom_exit_function=passed_traps, timeout=7,
        custom_exit_function_arg={'x_min': 1944, 'x_max': 1945, 'y_min': 4426, 'y_max': 4427},
        pre_interact=lambda: osrs.move.go_to_loc(1944, 4423, exact_tile=True),
        right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 8
    osrs.move.interact_with_object_v3(
        21280, conditional_click='Pass',
        obj_tile={'x': 1973, 'y': 4423, 'z': 0}, custom_exit_function=passed_traps, timeout=7,
        custom_exit_function_arg={'x_min': 1974, 'x_max': 1975, 'y_min': 4425, 'y_max': 4426},
        pre_interact=lambda: osrs.move.go_to_loc(1974, 4422, exact_tile=True),
        right_click_option='Pass'
    )
    st = datetime.datetime.now()
    osrs.move.interact_with_object_v3(
        26616, custom_exit_function=searched_chest, custom_exit_function_arg=st
    )
    osrs.move.interact_with_object_v3(
        20931, obj_type='wall', right_click_option='Quick-leave', coord_type='y', coord_value=4000,
        greater_than=False, obj_tile={'x': 1976, 'y': 4435, 'z': 0}
    )
    room = 1

