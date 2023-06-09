import datetime


import osrs
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
built_larder = '13566'
larder_slot = '15403'
item_to_make = '2'
plank = '8778'
noted_plank = '8779'
min_planks = 8
phials = '1614'

def make_chair():
    chair_to_build = osrs.server.get_surrounding_game_objects(10, [larder_slot], port)
    osrs.move.right_click_menu_select(chair_to_build[larder_slot], None, port, 'Larder space', 'Build')
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
            osrs.move.right_click_menu_select(chair_to_remove[built_larder], None, port, 'Larder', 'Remove')
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
        plank_count = osrs.inv.get_item_quantity_in_inv(inv, plank)
        if plank_count >= min_planks:
            make_chair()
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
        planks = osrs.inv.is_item_in_inventory_v2(inv, noted_plank)
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


def enter_home():
    outer_portal = osrs.server.get_game_object('2951,3222,0', '15478', port)
    osrs.move.right_click_menu_select(outer_portal, None, port, 'Portal', 'Build mode')
    while True:
        loc = osrs.server.get_world_location(port)
        if loc and 'x' in loc and loc['x'] > 4000:
            break

def main():
    start_time = datetime.datetime.now()
    osrs.clock.random_sleep(3, 3.1)
    while True:
        start_time = osrs.game.break_manager(start_time, 49, 54, 432, 673, 'pass_70', False, port)
        osrs.clock.antiban_rest(45, 100, 300)
        build_until_out()
        osrs.clock.antiban_rest(45, 100, 300)
        leave_house()
        osrs.clock.antiban_rest(45, 100, 300)
        click_phials()
        osrs.clock.antiban_rest(45, 100, 300)
        enter_home()
        osrs.clock.random_sleep(3, 5)

osrs.clock.random_sleep(2, 3)
main()