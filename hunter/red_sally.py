import datetime

import osrs

NORTH_TREE = '2449,3228,0'
NORTH_BROKEN_TRAP = '2449,3227,0'

WEST_TREE = '2447,3225,0'
WEST_BROKEN_TRAP = '2447,3226,0'

EAST_TREE = '2451,3225,0'
EAST_BROKEN_TRAP = '2450,3225,0'

SOUTH_TREE = '2453,3219,0'
SOUTH_BROKEN_TRAP = '2453,3220,0'

ROPE = 954
SMALL_NET = 303

TRAP_COUNT = 4
SALAMANDER = 10147
CAUGHT_SALLY = '8986'
YOUNG_TREE = '8990'
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
        'tree': EAST_TREE,
        'trap': EAST_BROKEN_TRAP
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
    while True:
        full_trap = osrs.server.get_game_object(pair['tree'], CAUGHT_SALLY, port)
        if not full_trap:
            return
        else:
            osrs.move.spam_click(pair['tree'], 0.25)
            osrs.clock.sleep_one_tick()


def set_trap(unset_tree, pair):
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
        if count == TRAP_COUNT:
            verify = 0
            for pair in locs:
                retrieve_rope_and_net(pair)
                unset_tree = osrs.server.get_game_object(pair['tree'], YOUNG_TREE)
                if unset_tree:
                    verify += 1
            if verify == TRAP_COUNT:
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
            osrs.inv.power_drop(inv, [], [SALAMANDER])


main()
# i accidentally trapped a ninja imp over my trap which blocked action...