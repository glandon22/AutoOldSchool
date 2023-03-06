# 9003 temp catch
# 9004 catch
# 9341 tree to set trap
# 9343 set trap w nothing in it
# 9005 9158 temp states before net is broken then net and rope fall to ground
# ghasts hit me so may need to bring food


# start script by setting correct amonut of traps, currently two
# begin looping to check for catch or borken trap
# when discovred, loot it and reset it

import datetime

from osrs_utils import general_utils
port = '56799'


def place_trap():
    tree = general_utils.get_surrounding_game_objects(5, ['9341'])
    if tree and '9341' in tree:
        general_utils.move_and_click(tree['9341']['x'], tree['9341']['y'], 2, 2)
    while True:
        objs = general_utils.get_surrounding_game_objects(3, ['9343'])
        if '9343' in objs:
            general_utils.random_sleep(1.5, 1.6)
            break
    inv = general_utils.get_inv(port, True)
    liz = general_utils.is_item_in_inventory_v2(inv, 10149)
    if liz:
        general_utils.move_and_click(liz['x'], liz['y'], 3, 3)

def wait_for_catch():
    while True:
        objs = general_utils.get_surrounding_game_objects(8, ['9003', '9004', '9343', '9005', '9158'])
        if '9004' in objs:
            general_utils.move_and_click(objs['9004']['x'], objs['9004']['y'], 2, 2)
            general_utils.random_sleep(2, 2.3)
            break
        ground_items = general_utils.get_surrounding_ground_items(8, ['303', '954'], port)
        if ground_items and '954' in ground_items and '303' in ground_items:
            # need to wait in between, once i move i need to recall ground items to find hte new coords of net
            general_utils.right_click_menu_select(ground_items['954'][0], None, port, 'Rope', 'Take')
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary(port)
            general_utils.random_sleep(0.5, 0.6)
            ground_items = general_utils.get_surrounding_ground_items(2, ['303'], port)
            general_utils.right_click_menu_select(ground_items['303'][0], None, port, 'Small fishing net', 'Take')
            break

def main():
    start_time = datetime.datetime.now()
    general_utils.random_sleep(0.3, 0.4)
    place_trap()
    while True:
        start_time = general_utils.break_manager(start_time, 53, 58, 423, 551, 'julenth', False)
        general_utils.random_sleep(0.6, 0.7)
        place_trap()
        general_utils.random_sleep(0.6, 0.7)
        wait_for_catch()

general_utils.random_sleep(1, 1.5)
main()