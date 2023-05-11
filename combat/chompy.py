# chompy id 1475
# 684 swamp hole id
# toad 1473
# 2875 inflated toad
import datetime

from osrs_utils import general_utils
port = '56799'


def fill_bellows():
    swamp = general_utils.get_multiple_surrounding_game_objects(10, ['684'], port)
    if swamp and '684' in swamp:
        print(swamp['684'])
        closest = general_utils.find_closest_target(swamp['684'])
        print(closest)
        if closest:
            #this spot is unreachable
            if closest['x_coord'] == 2396 and closest['y_coord'] == 3043:
                general_utils.run_towards_square_v2({'x': 2394, 'y': 3050, 'z': 0}, port)
                return
            general_utils.move_and_click(closest['x'], closest['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                curr_inv = general_utils.get_inv()
                if general_utils.is_item_in_inventory_v2(curr_inv, '2872') or \
                        (datetime.datetime.now() - start_time).total_seconds() > 5:
                    break


def inflate_toads():
    toads = general_utils.get_npcs_by_id('1473', port)
    if toads:
        c = general_utils.find_closest_target(toads)
        if c:
            general_utils.fast_move_and_click(c['x'], c['y'], 3, 3)


def main():
    while True:
        inv = general_utils.get_inv()
        empty_bellows = general_utils.is_item_in_inventory_v2(inv, '2871')
        inflated_toad = general_utils.is_item_in_inventory_v2(inv, '2875')
        chompies = general_utils.get_npcs_by_id('1475', port)
        interacting = general_utils.get_interacting(port)
        if interacting:
            continue
        if chompies:
            closest = general_utils.find_closest_target(chompies)
            if closest:
                general_utils.fast_move_and_click(closest['x'], closest['y'], 2, 2)
                general_utils.random_sleep(1, 2)
            continue
        if empty_bellows:
            fill_bellows()
            continue
        if inflated_toad:
            general_utils.move_and_click(inflated_toad['x'], inflated_toad['y'], 3, 3)
            general_utils.random_sleep(1.4, 3)
            continue
        inflate_toads()




main()
#print(general_utils.get_inv())