'''
notes

entrance 26624 -> wall 20932

26622
26623
26625

mummy 1779 right click Start-minigame
rm1
21280 Pass -> spear trap succes when y<= 4471
search 26616
wall 26620 Pick-lock then Enter
wall 26621 Pick-lock then Enter
wall 26618 Pick-lock then Enter
wall 26618 Pick-lock then Enter
26619
'''
import datetime


import osrs
# use this to track which room i am in
room = 1


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


def into_next_room(start_time):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'428,5'})
    qh.query_backend()
    if start_time and (datetime.datetime.now() - start_time).total_seconds() > 5:
        osrs.dev.logger.warning('Timed out trying to escape room 1 through door')
        return True
    elif qh.get_widgets('428,5') and f'Room {room}' in qh.get_widgets('428,5')['text']:
        osrs.dev.logger.info('successfully made it through floor %s.', room - 1)
        return True


def completed_room(exit_function):
    for i in range(26618, 26621 + 1):
        start_time = datetime.datetime.now()
        osrs.move.interact_with_object_v3(
            i, custom_exit_function=exit_function, custom_exit_function_arg=start_time, obj_type='wall'
        )
        if exit_function(None):
            return


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
        21280, coord_type='y', coord_value=4471, greater_than=False, timeout=7, right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 2
    osrs.clock.sleep_one_tick()
    osrs.move.interact_with_object_v3(
        21280, coord_type='y', coord_value=4472, greater_than=False, timeout=7, right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 3
    osrs.clock.sleep_one_tick()
    osrs.move.interact_with_object_v3(
        21280, coord_type='y', coord_value=4464, greater_than=False, timeout=7, right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    osrs.clock.random_sleep(3, 3.1)
    # room 4
    osrs.move.interact_with_object_v3(
        21280, coord_type='x', coord_value=1932, greater_than=True, timeout=7, right_click_option='Pass',
        obj_tile={'x': 1930, 'y': 4454, 'z': 0}
    )
    room += 1
    completed_room(into_next_room)
    # room 5
    osrs.clock.sleep_one_tick()
    osrs.move.interact_with_object_v3(
        21280, coord_type='x', coord_value=1960, greater_than=False, timeout=7, right_click_option='Pass',
        obj_tile={'x': 1962, 'y': 4446, 'z': 0}
    )
    room += 1
    completed_room(into_next_room)
    # room 6
    osrs.clock.sleep_one_tick()
    osrs.move.interact_with_object_v3(
        21280, coord_type='y', coord_value=4429, greater_than=True, timeout=7, right_click_option='Pass'
    )
    room += 1
    completed_room(into_next_room)
    # room 7
    osrs.clock.sleep_one_tick()
    osrs.move.interact_with_object_v3(
        21280, coord_type='y', coord_value=4426, greater_than=True, timeout=7, right_click_option='Pass',
        obj_tile={'x': 1946, 'y': 4424, 'z': 0}
    )
    room += 1
    completed_room(into_next_room)
    # room 8
    osrs.clock.sleep_one_tick()
    osrs.move.interact_with_object_v3(
        21280, coord_type='y', coord_value=4425, greater_than=True, timeout=7, right_click_option='Pass',
        obj_tile={'x': 1976, 'y': 4423, 'z': 0}
    )
    st = datetime.datetime.now()
    osrs.move.interact_with_object_v3(
        26616, custom_exit_function=searched_chest, custom_exit_function_arg=st
    )
    osrs.move.interact_with_object_v3(
        20931, obj_type='wall', right_click_option='Quick-leave', coord_type='y', coord_value=4000,
        greater_than=False, obj_tile={'x': 1976, 'y': 4435, 'z': 0}
    )


# 26616 search
