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
player_house = 'z e g g'


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


def offer_until_out():
    while True:
        inv = osrs.inv.get_inv(port)
        bone_count = osrs.inv.get_item_quantity_in_inv(inv, bones)
        if bone_count > 0:
            offer()
        else:
            break


def offer_until_out_v2():
    while True:
        inv = osrs.inv.get_inv(port)
        bone_count = osrs.inv.get_item_quantity_in_inv(inv, bones)
        if bone_count > 0:
            altar_obj = osrs.server.get_surrounding_game_objects(15, [altar], port)
            if altar in altar_obj and 'dist' in altar_obj[altar]:
                if altar_obj[altar]['dist'] > 1:
                    osrs.move.move_and_click(altar_obj[altar]['x'], altar_obj[altar]['y'], 4, 4)
                    osrs.clock.random_sleep(1, 2)
                else:
                    for item in inv:
                        if item['id'] == int(bones):
                            altar_obj = osrs.server.get_surrounding_game_objects(15, [altar], port)
                            osrs.move.move_and_click(item['x'], item['y'], 2, 3)
                            osrs.move.move_and_click(altar_obj[altar]['x'], altar_obj[altar]['y'], 3, 3)
                    osrs.clock.random_sleep(1, 2)
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


script_config = {
    'intensity': 'low',
    'logout': False,
    'login': False
}


def main():
    while True:
        offer_until_out_v2()
        leave_house()
        osrs.game.break_manager_v4(script_config)
        click_phials()
        osrs.clock.sleep_one_tick()
        enter_home()

main()