import datetime

from osrs_utils import general_utils
# anchor
# 2660,2608,0
# ladder 2666,2585,0
#+ 6, -23
port = '56799'
npcs_to_attack = '1693, 1736, 1707, 1692, 1721, 1702, 1691, 1732, 1730, 1708, 1720, 1731, 1722, 1706, 1713, 1737, 1701'


def enter_boat():
    plank = general_utils.get_game_object('2637,2653,0', '25632', port)
    if plank:
        general_utils.move_and_click(plank['x'], plank['y'], 3, 3)


def calc_anchor_point():
    boat_side = general_utils.get_surrounding_wall_objects(15, ['14254'], port)
    if boat_side and '14254' in boat_side:
        print('lll', boat_side)
        return {'x': boat_side['14254'][0]['x_coord'], 'y': boat_side['14254'][0]['y_coord'], 'z': 0}
    return None


def climb_ladder(ap):
    general_utils.run_towards_square_v2({'x': anchor_point['x'] + 6, 'y': anchor_point['y'] - 20, 'z': 0}, port)
    ladder = general_utils.get_game_object('{},{},0'.format(ap['x'] + 6, ap['y'] - 22), '14296', port)
    general_utils.random_sleep(0.6, 0.7)
    print('999', ladder)
    if ladder:
        general_utils.move_and_click(ladder['x'], ladder['y'], 3, 3)
        general_utils.random_sleep(2, 3)


def main():
    global anchor_point
    # Use this value to store what instanced tile I start the game on
    anchor_point = None
    start_time = datetime.datetime.now()
    while True:
        curr_loc = general_utils.get_world_location(port)
        interacting = general_utils.get_interacting(port)
        # I am standing on dock
        if curr_loc and 'x' in curr_loc and 3000 > curr_loc['x'] >= 2638:
            anchor_point = None
            general_utils.sleep_one_tick()
            start_time = general_utils.break_manager(start_time, 53, 59, 423, 551, 'pass_70', False)
            enter_boat()
            general_utils.random_sleep(2,3)
            continue
        # In boat waiting for game to begin
        if curr_loc and 'x' in curr_loc and curr_loc['x'] < 2636:
            print('Waiting for the game to start, I am in the boat.')
            continue
        # Game has started, I am still in the boat
        if curr_loc and 'x' in curr_loc and 50000 > curr_loc['x'] > 3000 and not anchor_point:
            general_utils.random_sleep(0.6, 0.7)
            anchor_point = calc_anchor_point()
            print('Game has begun')
            climb_ladder(anchor_point)
            continue
        if not interacting:
            npcs = general_utils.get_npcs_by_id(npcs_to_attack, port)
            if npcs:
                closest = general_utils.find_closest_npc(npcs)
                if closest and closest['x'] < 1915 and closest['y'] < 1040:
                    general_utils.move_and_click(closest['x'], closest['y'], 2, 2)
                    general_utils.random_sleep(1.5, 1.7)


main()