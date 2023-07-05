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


def get_in_position():
    chair_to_build = osrs.server.get_surrounding_game_objects(10, [larder_slot], port)
    osrs.move.right_click_menu_select(chair_to_build[larder_slot], None, port, 'Larder space', 'Build')
    while True:
        build_menu = osrs.server.get_widget('458,0', port)
        if build_menu:
            osrs.keeb.press_key('esc')
            osrs.clock.random_sleep(0.5, 0.6)
            break


def build():
    while True:
        inv = osrs.inv.get_inv(port)
        plank_count = osrs.inv.get_item_quantity_in_inv(inv, plank)
        if plank_count >= min_planks:
            make_chair()
            remove_chair()
        else:
            # wait for butler to return with more planks
            inv = osrs.inv.get_inv(port)
            plank_count = osrs.inv.get_item_quantity_in_inv(inv, plank)
            if plank_count >= min_planks:
                butler = osrs.server.get_npc_by_id('227')
                if butler and 'dist' in butler:
                    if butler['dist'] <= 1:
                        # butler is still moving so wait a second
                        osrs.clock.random_sleep(1.2, 1.4)
                        butler = osrs.server.get_npc_by_id('227')
                        if butler:
                            osrs.move.move_and_click(butler['x'], butler['y'], 2, 2)
                            chat = osrs.server.get_chat_options()
                            if chat:
                                for i, option in enumerate(chat):
                                    if 'Fetch' in option:
                                        osrs.keeb.keyboard.type(str(i))
                                        break
                    else:
                        call_butler()


def build_v2():
    # 1 = building 2 = waiting
    status = 1
    while True:
        inv = osrs.inv.get_inv(port)
        plank_count = osrs.inv.get_item_quantity_in_inv(inv, plank)
        butler = osrs.server.get_npc_by_id('227')
        if status == 1:
            osrs.game.break_manager_v3(script_config)
            if plank_count >= min_planks:
                make_chair()
                remove_chair()
            else:
                status = 2
        elif status == 2:
            # butler has delivered planks and is waiting for instructions
            if plank_count >= min_planks and butler:
                osrs.clock.random_sleep(1.2, 1.4)
                butler = osrs.server.get_npc_by_id('227')
                osrs.move.move_and_click(butler['x'], butler['y'], 2, 2)
                while True:
                    chat = osrs.server.get_chat_options()
                    if chat:
                        found = False
                        for i, option in enumerate(chat):
                            if 'Fetch' in option:
                                osrs.keeb.keyboard.type(str(i))
                                found = True
                        if found:
                            status = 1
                            break
        elif plank_count < min_planks:
            call_butler()


def call_butler():
    while True:
        wrench = osrs.server.get_widget('161,53', port)
        if wrench:
            osrs.move.move_and_click(wrench['x'], wrench['y'], 3, 3)
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            house_icon = osrs.server.get_widget('116,31', port)
            if house_icon:
                osrs.move.move_and_click(house_icon['x'], house_icon['y'], 3, 3)
                osrs.clock.sleep_one_tick()
                osrs.clock.sleep_one_tick()
                call_servant = osrs.server.get_widget('370,22', port)
                if call_servant:
                    osrs.move.move_and_click(call_servant['x'], call_servant['y'], 3, 3)
                    start_time = datetime.datetime.now()
                    while True:
                        chat = osrs.server.get_chat_options()
                        if chat:
                            for i, option in enumerate(chat):
                                if 'Fetch' in option:
                                    osrs.keeb.keyboard.type(str(i))
                                    return
                        elif (datetime.datetime.now() - start_time).total_seconds() > 10:
                            break


def enter_home():
    outer_portal = osrs.server.get_game_object('2951,3222,0', '15478', port)
    osrs.move.right_click_menu_select(outer_portal, None, port, 'Portal', 'Build mode')
    while True:
        loc = osrs.server.get_world_location(port)
        if loc and 'x' in loc and loc['x'] > 4000:
            break


def login_routine():
    osrs.clock.random_sleep(2, 3)
    enter_home()
    osrs.clock.random_sleep(3, 5)
    get_in_position()


script_config = {
    'intensity': 'high',
    'logout': False,
    'login': login_routine
}


def main():
    while True:
        enter_home()
        osrs.clock.random_sleep(3, 5)
        get_in_position()
        call_butler()
        build_v2()


main()
