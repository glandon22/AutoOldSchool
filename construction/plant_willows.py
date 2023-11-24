import datetime


import osrs
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
built_larder = '4534'
larder_slot = '15362'
item_to_make = '4'
plant = '8423'
noted_plant = '8424'
phials = '1614'
empty_can = '5331'
cans_with_water = [5333, 5334, 5335, 5336, 5337, 5338, 5339, 5340]

def make_chair():
    chair_to_build = osrs.server.get_surrounding_game_objects(10, [larder_slot], port)
    osrs.move.right_click_menu_select(chair_to_build[larder_slot], None, port, 'Small Plant space 1', 'Build')
    while True:
        build_menu = osrs.server.get_widget('458,0', port)
        if build_menu:
            keyboard.type(item_to_make)
            osrs.clock.random_sleep(0.5, 0.6)
            break


def remove_chair():
    while True:
        chair_to_remove = osrs.server.get_surrounding_game_objects(10, [built_larder], port)
        if chair_to_remove:
            osrs.move.right_click_menu_select(chair_to_remove[built_larder], None, port, 'Plant', 'Remove')
            break
    osrs.clock.random_sleep(0.2, 0.3)
    while True:
        options = osrs.server.get_chat_options(port)
        if options:
            keyboard.type('1')
            break
    osrs.clock.random_sleep(0.2, 0.3)
    while True:
        chair_to_build = osrs.server.get_surrounding_game_objects(10, [larder_slot], port)
        if chair_to_build:
            break
    osrs.clock.random_sleep(0.2, 0.3)


def build_until_out():
    while True:
        inv = osrs.inv.get_inv(port)
        plant_count = osrs.inv.get_item_quantity_in_inv(inv, plant)
        filled_can_exists = osrs.inv.are_items_in_inventory_v2(inv, cans_with_water)
        if plant_count > 0 and filled_can_exists:
            make_chair()
            osrs.clock.random_sleep(0.6,0.7)
            remove_chair()
        else:
            break


def leave_house():
    portal = osrs.server.get_surrounding_game_objects(15, ['4525'], port)
    osrs.move.move_and_click(portal['4525']['x'], portal['4525']['y'], 1, 5)
    while True:
        loc = osrs.server.get_world_location(port)
        if loc and 'x' in loc and loc['x'] < 4000:
            break


def click_phials():
    while True:
        inv = osrs.inv.get_inv(port, True)
        planks = osrs.inv.is_item_in_inventory_v2(inv, noted_plant)
        if not planks:
            exit('no more planks')
        osrs.move.move_and_click(planks['x'], planks['y'], 3, 3)
        phials_loc = osrs.server.get_npc_by_id(phials, port)
        if phials_loc:
            osrs.move.move_and_click(phials_loc['x'], phials_loc['y'], 2, 2)
            osrs.clock.random_sleep(0.2, 0.3)
        targ = osrs.server.get_target_npc(port)
        # misclicked
        if str(targ) != phials:
            osrs.move.wait_until_stationary(port)
            continue
        else:
            while True:
                options = osrs.server.get_chat_options(port)
                if options:
                    option_to_select = osrs.util.select_chat_option(options, 'Exchange All')
                    keyboard.type(str(option_to_select))
                    break
            osrs.clock.random_sleep(0.2, 0.3)
            break
    inv = osrs.inv.get_inv(port, True)
    empty_can_exists = osrs.inv.is_item_in_inventory_v2(inv, empty_can)
    if empty_can_exists:
        osrs.clock.random_sleep(1, 1.1)
        osrs.move.move_and_click(empty_can_exists['x'], empty_can_exists['y'], 3, 3)
        well = osrs.server.get_game_object('2966,3209,0', '9684', port)
        osrs.move.move_and_click(well['x'], well['y'], 3, 3)
    while True:
        inv = osrs.inv.get_inv(port, True)
        empty_can_exists = osrs.inv.is_item_in_inventory_v2(inv, empty_can)
        if not empty_can_exists:
            osrs.clock.random_sleep(0.6, 0.67)
            break


def enter_home():
    outer_portal = osrs.server.get_game_object('2951,3222,0', '15478', port)
    osrs.move.right_click_menu_select(outer_portal, None, port, 'Portal', 'Build mode')
    while True:
        loc = osrs.server.get_world_location(port)
        if loc and 'x' in loc and loc['x'] > 4000:
            break

def main():
    start_time = datetime.datetime.now()
    while True:
        build_until_out()
        leave_house()
        click_phials()
        start_time = osrs.game.break_manager(start_time, 49, 54, 432, 673, 'julenth', False, port)
        enter_home()
        osrs.clock.random_sleep(3, 5)

osrs.clock.random_sleep(2, 3)
main()
