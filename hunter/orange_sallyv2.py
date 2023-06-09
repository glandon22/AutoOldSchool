import datetime

import pyautogui


import osrs

SOUTH_TREE = '3407,3088,0'
SOUTH_BROKEN_TRAP = '3408,3088,0'

WEST_TREE = '3404,3092,0'
WEST_BROKEN_TRAP = '3403,3092,0'

NORTH_TREE = '3407,3093,0'
NORTH_BROKEN_TRAP = '3407,3094,0'

ROPE = 954
SMALL_NET = 303

CAUGHT_SALLY = '8734'
YOUNG_TREE = '8732'
port = '56799'

locs = [
    {
        'tree': NORTH_TREE,
        'trap': NORTH_BROKEN_TRAP
    },
    {
        'tree': WEST_TREE,
        'trap': WEST_BROKEN_TRAP
    },
    {
        'tree': SOUTH_TREE,
        'trap': SOUTH_BROKEN_TRAP
    },
]


def retrieve_rope_and_net(pair):
    while True:
        broken_rope = osrs.server.get_ground_items(pair['trap'], ROPE)
        broken_net = osrs.server.get_ground_items(pair['trap'], SMALL_NET)
        if (broken_rope and str(ROPE) in broken_rope) or (broken_net and str(SMALL_NET) in broken_net):
            osrs.move.spam_click(pair['trap'], 0.25)
        else:
            return


def retrieve_catch(catch, pair):
    osrs.move.move_and_click(catch['x'], catch['y'], 2, 2)
    start_time = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - start_time).total_seconds() > 10:
            print('Exceeded 10 second wait time when trying to retrieve catch on {} tree'.format(pair['tree']))
            break
        full_trap = osrs.server.get_game_object(pair['tree'], CAUGHT_SALLY, port)
        if not full_trap:
            # Need to sleep for a moment to let that trap be cleared and animation complete.
            osrs.clock.random_sleep(1, 1.1)
            print('Catch has been retrieved on tree {}.'.format(pair['tree']))
            break
        else:
            osrs.clock.sleep_one_tick()


def set_trap(unset_tree, pair):
    '''
    osrs.move.fast_move_and_click(unset_tree['x'], unset_tree['y'], 2, 2)
    start_time = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - start_time).total_seconds() > 10:
            print('Exceeded 5 second wait time when trying to set trap on {} tree'.format(pair['tree']))
            break
        trap_to_set = osrs.server.get_game_object(pair['tree'], YOUNG_TREE, port)
        if not trap_to_set:
            # Need to sleep for a moment to let that trap set and animation complete.
            osrs.clock.random_sleep(2.7, 2.8)
            print('New trap has been set on tree {}.'.format(pair['tree']))
            break
        else:
            osrs.clock.sleep_one_tick()'''

    while True:
        trap_to_set = osrs.server.get_game_object(pair['tree'], YOUNG_TREE, port)
        inv = osrs.inv.get_inv()
        have_rope = osrs.inv.is_item_in_inventory_v2(inv, ROPE)
        have_net = osrs.inv.is_item_in_inventory_v2(inv, SMALL_NET)
        if not trap_to_set or not have_net or not have_rope:
            return
        else:
            osrs.move.spam_click(pair['tree'], 0.25)
            osrs.clock.sleep_one_tick()


def collect_traps_to_logout():
    while True:
        count = 0
        for pair in locs:
            catch = osrs.server.get_game_object(pair['tree'], CAUGHT_SALLY, port)
            if catch:
                retrieve_catch(catch, pair)
            retrieve_rope_and_net(pair)
            unset_tree = osrs.server.get_game_object(pair['tree'], YOUNG_TREE)
            if unset_tree:
                count += 1
            inv = osrs.inv.get_inv()
            osrs.inv.power_drop(inv, [], [10146])
        if count == 3:
            verify = 0
            for pair in locs:
                unset_tree = osrs.server.get_game_object(pair['tree'], YOUNG_TREE)
                if unset_tree:
                    verify += 1
            if verify == 3:
                return


def main():
    start_time = datetime.datetime.now()
    while True:
        # need to create function to allow log out
        start_time = osrs.game.break_manager(start_time, 51, 56, 423, 551, 'julenth', False, port, collect_traps_to_logout)
        for pair in locs:
            catch = osrs.server.get_game_object(pair['tree'], CAUGHT_SALLY, port)
            if catch:
                retrieve_catch(catch, pair)
            retrieve_rope_and_net(pair)
            unset_tree = osrs.server.get_game_object(pair['tree'], YOUNG_TREE)
            if unset_tree:
                set_trap(unset_tree, pair)
            inv = osrs.inv.get_inv()
            osrs.inv.power_drop(inv, [], [10146])


main()
