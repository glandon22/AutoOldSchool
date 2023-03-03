import datetime

from osrs_utils import general_utils
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
built_larder = '5134'
larder_slot = '15366'
item_to_make = '1'
plant = '8431'
noted_plant = '8432'
phials = '1614'
empty_can = '5331'

def make_chair():
    chair_to_build = general_utils.get_surrounding_game_objects(10, [larder_slot], port)
    general_utils.right_click_menu_select(chair_to_build[larder_slot], None, port, 'Small Plant space 1', 'Build')
    while True:
        build_menu = general_utils.get_widget('458,0', port)
        if build_menu:
            keyboard.type(item_to_make)
            general_utils.random_sleep(0.5, 0.6)
            break


def remove_chair():
    while True:
        chair_to_remove = general_utils.get_surrounding_game_objects(10, [built_larder], port)
        if chair_to_remove:
            general_utils.right_click_menu_select(chair_to_remove[built_larder], None, port, 'Plant', 'Remove')
            break
    general_utils.random_sleep(0.2, 0.3)
    while True:
        options = general_utils.get_chat_options(port)
        if options:
            keyboard.type('1')
            break
    general_utils.random_sleep(0.2, 0.3)
    while True:
        chair_to_build = general_utils.get_surrounding_game_objects(10, [larder_slot], port)
        if chair_to_build:
            break
    general_utils.random_sleep(0.2, 0.3)


def build_until_out():
    while True:
        inv = general_utils.get_inv(port)
        plant_count = general_utils.get_item_quantity_in_inv(inv, plant)
        empty_can_exists = general_utils.is_item_in_inventory_v2(inv, empty_can)
        if plant_count > 0 and not empty_can_exists:
            make_chair()
            general_utils.random_sleep(0.6,0.7)
            remove_chair()
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
        planks = general_utils.is_item_in_inventory_v2(inv, noted_plant)
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
    inv = general_utils.get_inv(port, True)
    empty_can_exists = general_utils.is_item_in_inventory_v2(inv, empty_can)
    if empty_can_exists:
        general_utils.random_sleep(1, 1.1)
        general_utils.move_and_click(empty_can_exists['x'], empty_can_exists['y'], 3, 3)
        well = general_utils.get_game_object('2966,3209,0', '9684', port)
        general_utils.move_and_click(well['x'], well['y'], 3, 3)
    while True:
        inv = general_utils.get_inv(port, True)
        empty_can_exists = general_utils.is_item_in_inventory_v2(inv, empty_can)
        if not empty_can_exists:
            general_utils.random_sleep(0.6, 0.67)
            break


def enter_home():
    outer_portal = general_utils.get_game_object('2951,3222,0', '15478', port)
    general_utils.right_click_menu_select(outer_portal, None, port, 'Portal', 'Build mode')
    while True:
        loc = general_utils.get_world_location(port)
        if loc and 'x' in loc and loc['x'] > 4000:
            break

def main():
    start_time = datetime.datetime.now()
    general_utils.random_sleep(3, 3.1)
    while True:
        general_utils.antiban_rest(45, 100, 300)
        build_until_out()
        general_utils.antiban_rest(45, 100, 300)
        leave_house()
        general_utils.antiban_rest(45, 100, 300)
        click_phials()
        general_utils.antiban_rest(45, 100, 300)
        start_time = general_utils.break_manager(start_time, 49, 54, 432, 673, 'julenth', False, port)
        enter_home()
        general_utils.random_sleep(3, 5)

general_utils.random_sleep(2, 3)
main()
