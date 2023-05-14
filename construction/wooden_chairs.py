import datetime

from autoscape import general_utils
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
built_chair = '6752'
chair_slot = '4517'
item_to_make = '1'
plank = '960'
noted_plank = '961'
min_planks = 2
phials = '1614'

def make_chair():
    chair_to_build = general_utils.get_surrounding_game_objects(10, [chair_slot], port)
    general_utils.right_click_menu_select(chair_to_build[chair_slot], None, port, 'Chair space', 'Build')
    while True:
        build_menu = general_utils.get_widget('458,0', port)
        if build_menu:
            keyboard.type(item_to_make)
            general_utils.random_sleep(0.5, 0.6)
            break


def remove_chair():
    while True:
        chair_to_remove = general_utils.get_surrounding_game_objects(10, [built_chair], port)
        if chair_to_remove:
            general_utils.right_click_menu_select(chair_to_remove[built_chair], None, port, 'Chair', 'Remove')
            break
    general_utils.random_sleep(0.2, 0.3)
    while True:
        options = general_utils.get_chat_options(port)
        if options:
            keyboard.type('1')
            break
    general_utils.random_sleep(0.2, 0.3)
    while True:
        chair_to_build = general_utils.get_surrounding_game_objects(10, [chair_slot], port)
        if chair_to_build:
            break
    general_utils.random_sleep(0.2, 0.3)


def build_until_out():
    while True:
        inv = general_utils.get_inv(port)
        plank_count = general_utils.get_item_quantity_in_inv(inv, plank)
        if plank_count >= min_planks:
            make_chair()
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
        planks = general_utils.is_item_in_inventory_v2(inv, noted_plank)
        if not planks:
            exit('no more planks')
        general_utils.move_and_click(planks['x'], planks['y'], 3, 3)
        phials_loc = general_utils.get_npc_by_id(phials, port)
        if phials_loc:
            general_utils.move_and_click(phials_loc['x'], phials_loc['y'], 2, 2)
        general_utils.random_sleep(0.5, 0.6)
        targ = general_utils.get_target_npc(port)
        # misclicked
        if str(targ) != phials:
            general_utils.wait_until_stationary(port)
            continue
        else:
            while True:
                options = general_utils.get_chat_options(port)
                if options:
                    keyboard.type('3')
                    break
            general_utils.random_sleep(0.2, 0.3)
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
    while True:
        start_time = general_utils.break_manager(start_time, 49, 54, 432, 673, 'pass_71', False, port)
        build_until_out()
        general_utils.antiban_rest(45, 100, 300)
        click_phials()
        general_utils.antiban_rest(45, 100, 300)
        enter_home()
        general_utils.antiban_rest(45, 100, 300)

main()