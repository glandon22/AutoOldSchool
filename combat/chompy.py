# chompy id 1475
# 684 swamp hole id
# toad 1473
# 2875 inflated toad
import datetime


import osrs
port = '56799'


def fill_bellows():
    swamp = osrs.server.get_multiple_surrounding_game_objects(10, ['684'], port)
    if swamp and '684' in swamp:
        print(swamp['684'])
        closest = osrs.util.find_closest_target(swamp['684'])
        print(closest)
        if closest:
            #this spot is unreachable
            if closest['x_coord'] == 2396 and closest['y_coord'] == 3043:
                osrs.move.run_towards_square_v2({'x': 2394, 'y': 3050, 'z': 0}, port)
                return
            osrs.move.move_and_click(closest['x'], closest['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                curr_inv = osrs.inv.get_inv()
                if osrs.inv.is_item_in_inventory_v2(curr_inv, '2872') or \
                        (datetime.datetime.now() - start_time).total_seconds() > 5:
                    break


def inflate_toads():
    toads = osrs.server.get_npcs_by_id('1473', port)
    if toads:
        c = osrs.util.find_closest_target(toads)
        if c:
            osrs.move.fast_move_and_click(c['x'], c['y'], 3, 3)


def main():
    while True:
        inv = osrs.inv.get_inv()
        empty_bellows = osrs.inv.is_item_in_inventory_v2(inv, '2871')
        inflated_toad = osrs.inv.is_item_in_inventory_v2(inv, '2875')
        chompies = osrs.server.get_npcs_by_id('1475', port)
        interacting = osrs.server.get_interacting(port)
        if interacting:
            continue
        if chompies:
            closest = osrs.util.find_closest_target(chompies)
            if closest:
                osrs.move.fast_move_and_click(closest['x'], closest['y'], 2, 2)
                osrs.clock.random_sleep(1, 2)
            continue
        if empty_bellows:
            fill_bellows()
            continue
        if inflated_toad:
            osrs.move.move_and_click(inflated_toad['x'], inflated_toad['y'], 3, 3)
            osrs.clock.random_sleep(1.4, 3)
            continue
        inflate_toads()

