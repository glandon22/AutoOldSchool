import datetime


import osrs
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
altar = '13197'
item_to_make = '2'
bones = '536'
noted_bones = '537'
min_planks = 8
phials = '1614'
player_house = 'im really hi'


def offer():
    inv = osrs.inv.get_inv(port)
    bone_inv = osrs.inv.is_item_in_inventory_v2(inv, bones)
    osrs.move.move_and_click(bone_inv['x'], bone_inv['y'], 3, 3)
    altar_obj = osrs.server.get_surrounding_game_objects(15, [altar], port)
    if altar in altar_obj:
        osrs.move.move_and_click(altar_obj[altar]['x'], altar_obj[altar]['y'], 4, 4)
        osrs.clock.random_sleep(3, 4)
    while True:
        inv = osrs.inv.get_inv(port)
        bone_inv = osrs.inv.is_item_in_inventory_v2(inv, bones)
        if not bone_inv:
            break
        leveled = osrs.server.have_leveled_up(port)
        if leveled:
            break


def build_until_out():
    while True:
        inv = osrs.inv.get_inv(port)
        bone_count = osrs.inv.get_item_quantity_in_inv(inv, bones)
        if bone_count > 0:
            offer()
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
        planks = osrs.inv.is_item_in_inventory_v2(inv, noted_bones)
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
    osrs.move.right_click_menu_select(outer_portal, None, port, 'Portal', 'Friend\'s house')
    osrs.clock.random_sleep(1, 1.1)
    osrs.move.wait_until_stationary(port)
    osrs.clock.random_sleep(0.6, 0.7)
    keyboard.type(player_house)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    while True:
        loc = osrs.server.get_world_location(port)
        if loc and 'x' in loc and loc['x'] > 4000:
            break

def main():
    start_time = datetime.datetime.now()
    osrs.clock.random_sleep(3, 3.1)
    while True:
        start_time = osrs.game.break_manager(start_time, 49, 54, 432, 673, 'julenth', False, port)
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