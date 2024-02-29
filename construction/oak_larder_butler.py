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
wrench_widget_id = '161,47'
house_widget_id = '116,31'
call_servant_widget_id = '370,22'
butler_greeting_widget_id = '231,4'
player_chat_widget_id = '217,5'
chat_box_input_widget_id = '162,41'


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


def build_v2(qh):
    # 1 = building 2 = waiting
    status = 2
    while True:
        qh.query_backend()
        inv = qh.get_inventory()
        plank_count = osrs.inv.get_item_quantity_in_inv(inv, plank)
        butler = osrs.server.get_npc_by_id('227')
        if status == 1:
            osrs.game.break_manager_v4(script_config)
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
                    # may need to add timeout and reclick here on butler
                    if chat:
                        found = False
                        for i, option in enumerate(chat):
                            if 'Fetch' in option:
                                osrs.keeb.keyboard.type(str(i))
                                found = True
                        if found:
                            status = 1
                            break
            elif qh.get_widgets(butler_greeting_widget_id):
                osrs.keeb.press_key('space')
            elif qh.get_chat_options():
                for i, option in enumerate(qh.get_chat_options()):
                    if '5,000 coins' in option:
                        osrs.keeb.keyboard.type(str(i))
        elif plank_count < min_planks:
            call_butler_v2(qh)


def build_v3(qh):
    # 1 = building 2 = waiting
    status = 2
    while True:
        qh.query_backend()
        inv = qh.get_inventory()
        plank_count = osrs.inv.get_item_quantity_in_inv(inv, plank)
        butler = osrs.server.get_npc_by_id('227')
        if status == 1:
            osrs.game.break_manager_v4(script_config)
            if plank_count >= min_planks:
                make_chair()
                remove_chair()
            else:
                status = 2
        elif status == 2:
            # butler has delivered planks and is waiting for instructions
            if plank_count >= min_planks and butler:
                call_butler_v2(qh)
                status = 1
            elif qh.get_widgets(butler_greeting_widget_id):
                osrs.keeb.press_key('space')
            elif qh.get_chat_options():
                for i, option in enumerate(qh.get_chat_options()):
                    if '5,000 coins' in option:
                        osrs.keeb.keyboard.type(str(i))


def call_butler_v2(qh: osrs.queryHelper.QueryHelper):
    # summon butler
    last_butler_click = datetime.datetime.now() - datetime.timedelta(hours=777)
    # send him for planks
    requested_planks = False
    while True:
        qh.query_backend()
        # wrench is always present, so check for that last
        if qh.get_npcs() \
                and len(qh.get_npcs()) > 0 \
                and 'dist' in qh.get_npcs()[0] \
                and qh.get_npcs()[0]['dist'] == 1 and (datetime.datetime.now() - last_butler_click).total_seconds() > 7:
            osrs.move.click(qh.get_npcs()[0])
            last_butler_click = datetime.datetime.now()
        elif qh.get_chat_options():
            for i, option in enumerate(qh.get_chat_options()):
                if 'Fetch from bank' in option:
                    return osrs.keeb.keyboard.type(str(i))
        elif qh.get_widgets(butler_greeting_widget_id):
            break
        elif qh.get_widgets(house_widget_id) and \
                qh.get_widgets(wrench_widget_id) and \
                'spriteID' in qh.get_widgets(wrench_widget_id) and \
                qh.get_widgets(wrench_widget_id)['spriteID'] == 1030:
            print(qh.get_widgets(wrench_widget_id))
            osrs.move.click(qh.get_widgets(house_widget_id))
            osrs.clock.sleep_one_tick()
        elif qh.get_widgets(call_servant_widget_id) and \
                qh.get_widgets(wrench_widget_id) and \
                'spriteID' in qh.get_widgets(wrench_widget_id) and \
                qh.get_widgets(wrench_widget_id)['spriteID'] == 1030:
            osrs.move.click(qh.get_widgets(call_servant_widget_id))
            osrs.clock.sleep_one_tick()
        elif qh.get_widgets(wrench_widget_id):
            osrs.move.click(qh.get_widgets(wrench_widget_id))
            osrs.clock.sleep_one_tick()
    while True:
        qh.query_backend()
        if qh.get_widgets(butler_greeting_widget_id) or qh.get_widgets(player_chat_widget_id):
            osrs.keeb.press_key('space')
        elif qh.get_chat_options():
            for i, option in enumerate(qh.get_chat_options()):
                if 'Go to the bank' in option or 'Bring something from the bank' in option or 'Oak planks' in option or '5,000 coins' in option:
                    osrs.keeb.keyboard.type(str(i))
                    if 'Oak planks' in option:
                        requested_planks = True
                # this dialogue appears after paying the servant 5k
                elif 'Go to the bank' in option:
                    return osrs.keeb.keyboard.type(str(i))
                elif 'Fetch from bank' in option:
                    return osrs.keeb.keyboard.type(str(i))
        elif qh.get_widgets(chat_box_input_widget_id) and requested_planks:
            print('found', qh.get_widgets(chat_box_input_widget_id))
            osrs.keeb.keyboard.type('16')
            return osrs.keeb.press_key('enter')


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
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        wrench_widget_id, house_widget_id, call_servant_widget_id, butler_greeting_widget_id, player_chat_widget_id,
        chat_box_input_widget_id
    })
    qh.set_chat_options()
    qh.set_inventory()
    qh.set_npcs(['227'])
    build_v3(qh)



main()
