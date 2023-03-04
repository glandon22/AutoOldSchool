import datetime

from osrs_utils import general_utils
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
altar = '13197'
item_to_make = '2'
bones = '536'
noted_bones = '537'
min_planks = 8
phials = '1614'
player_house = 'xgrace'


def offer():
    inv = general_utils.get_inv(port)
    bone_inv = general_utils.is_item_in_inventory_v2(inv, bones)
    general_utils.move_and_click(bone_inv['x'], bone_inv['y'], 3, 3)
    altar_obj = general_utils.get_surrounding_game_objects(15, [altar], port)
    if altar in altar_obj:
        general_utils.move_and_click(altar_obj[altar]['x'], altar_obj[altar]['y'], 4, 4)
        general_utils.random_sleep(3, 4)
    while True:
        inv = general_utils.get_inv(port)
        bone_inv = general_utils.is_item_in_inventory_v2(inv, bones)
        if not bone_inv:
            break
        leveled = general_utils.have_leveled_up(port)
        if leveled:
            break


def build_until_out():
    while True:
        inv = general_utils.get_inv(port)
        bone_count = general_utils.get_item_quantity_in_inv(inv, bones)
        if bone_count > 0:
            offer()
        else:
            break


def leave_house():
    portal = general_utils.get_surrounding_game_objects(15, ['4525'], port)
    general_utils.move_and_click(portal['4525']['x'], portal['4525']['y'], 1, 5)
    while True:
        loc = general_utils.get_world_location(port)
        if loc and 'x' in loc and loc['x'] < 4000:
            break


def click_phials():
    while True:
        inv = general_utils.get_inv(port, True)
        planks = general_utils.is_item_in_inventory_v2(inv, noted_bones)
        if not planks:
            exit('no more planks')
        general_utils.move_and_click(planks['x'], planks['y'], 3, 3)
        phials_loc = general_utils.get_npc_by_id(phials, port)
        if phials_loc:
            general_utils.move_and_click(phials_loc['x'], phials_loc['y'], 2, 2)
            general_utils.random_sleep(0.2, 0.3)
        targ = general_utils.get_target_npc(port)
        # misclicked
        if str(targ) != phials:
            general_utils.wait_until_stationary(port)
            continue
        else:
            while True:
                options = general_utils.get_chat_options(port)
                if options:
                    option_to_select = general_utils.select_chat_option(options, 'Exchange All')
                    keyboard.type(str(option_to_select))
                    break
            general_utils.random_sleep(0.2, 0.3)
            break


def enter_home():
    outer_portal = general_utils.get_game_object('2951,3222,0', '15478', port)
    general_utils.right_click_menu_select(outer_portal, None, port, 'Portal', 'Friend\'s house')
    general_utils.random_sleep(1, 1.1)
    general_utils.wait_until_stationary(port)
    general_utils.random_sleep(0.6, 0.7)
    keyboard.type(player_house)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    while True:
        loc = general_utils.get_world_location(port)
        if loc and 'x' in loc and loc['x'] > 4000:
            break

def main():
    start_time = datetime.datetime.now()
    general_utils.random_sleep(3, 3.1)
    while True:
        start_time = general_utils.break_manager(start_time, 49, 54, 432, 673, 'julenth', False, port)
        general_utils.antiban_rest(45, 100, 300)
        build_until_out()
        general_utils.antiban_rest(45, 100, 300)
        leave_house()
        general_utils.antiban_rest(45, 100, 300)
        click_phials()
        general_utils.antiban_rest(45, 100, 300)
        enter_home()
        general_utils.random_sleep(3, 5)

general_utils.random_sleep(2, 3)
main()