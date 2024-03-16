import datetime


import osrs
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
built_oak_door = '13345'
larder_slot = '15403'
dungeon_entrance_id = '4529'
item_to_make = '1'
plank = '8778'
noted_plank = '8779'
min_planks = 10
phials = '1614'
wrench_widget_id = '161,47'
house_widget_id = '116,31'
call_servant_widget_id = '370,22'
butler_greeting_widget_id = '231,4'
player_chat_widget_id = '217,5'
chat_box_input_widget_id = '162,41'
oak_door_id = '15327'


def make_door():
    while True:
        oak_wall = osrs.server.get_surrounding_wall_objects(8, [oak_door_id])
        if oak_door_id in oak_wall:
            osrs.move.right_click_menu_select(oak_wall[oak_door_id][0], None, port, 'Door space', 'Build')
        start_time = datetime.datetime.now()
        while True:
            build_menu = osrs.server.get_widget('458,0', port)
            if build_menu:
                keyboard.type(item_to_make)
                osrs.clock.random_sleep(0.5, 0.6)
                return
            elif (datetime.datetime.now() - start_time).total_seconds() > 4:
                break


def remove_door():
    while True:
        oak_wall = osrs.server.get_surrounding_wall_objects(8, [built_oak_door])
        if built_oak_door in oak_wall:
            osrs.move.right_click_menu_select(oak_wall[built_oak_door][0], None, port, 'Door', 'Remove')
            break
    osrs.clock.random_sleep(0.2, 0.3)
    while True:
        options = osrs.server.get_chat_options(port)
        if options:
            keyboard.type('1')
            break
    osrs.clock.random_sleep(0.2, 0.3)
    while True:
        oak_wall = osrs.server.get_surrounding_wall_objects(8, [oak_door_id])
        if oak_door_id in oak_wall:
            break
    osrs.clock.random_sleep(0.2, 0.3)


def go_to_dungeon():
    while True:
        dungeon_entrance = osrs.server.get_surrounding_game_objects(12, [dungeon_entrance_id], port)
        if dungeon_entrance:
            osrs.move.click(dungeon_entrance[dungeon_entrance_id])
            break
    while True:
        oak_wall = osrs.server.get_surrounding_wall_objects(8, [oak_door_id])
        if oak_door_id in oak_wall:
            osrs.move.right_click_menu_select(oak_wall[oak_door_id][0], None, port, 'Door space', 'Build')
            break
    while True:
        build_menu = osrs.server.get_widget('458,0', port)
        if build_menu:
            osrs.keeb.press_key('esc')
            osrs.clock.random_sleep(0.5, 0.6)
            break


def get_in_position():
    chair_to_build = osrs.server.get_surrounding_game_objects(10, [larder_slot], port)
    osrs.move.right_click_menu_select(chair_to_build[larder_slot], None, port, 'Larder space', 'Build')
    while True:
        build_menu = osrs.server.get_widget('458,0', port)
        if build_menu:
            osrs.keeb.press_key('esc')
            osrs.clock.random_sleep(0.5, 0.6)
            break


def build_v3(qh):
    # 1 = building 2 = waiting
    status = 2
    last_butler_call = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        inv = qh.get_inventory()
        plank_count = osrs.inv.get_item_quantity_in_inv(inv, plank)
        butler = osrs.server.get_npc_by_id('227')
        if status == 1:
            if plank_count >= min_planks:
                make_door()
                remove_door()
            else:
                status = 2
        elif status == 2 and (datetime.datetime.now() - last_butler_call).total_seconds() > 14:
            osrs.game.break_manager_v4(script_config)
            call_butler_v2(qh)
            last_butler_call = datetime.datetime.now()
            status = 1



def call_butler_v2(qh: osrs.queryHelper.QueryHelper):
    # summon butler
    last_butler_click = datetime.datetime.now() - datetime.timedelta(hours=777)
    # send him for planks
    requested_planks = False
    called_butler = False
    while True:
        qh.query_backend()
        if qh.get_chat_options():
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
        elif qh.get_widgets(butler_greeting_widget_id) or qh.get_widgets(player_chat_widget_id):
            osrs.keeb.press_key('space')
        elif qh.get_widgets(house_widget_id) and \
                qh.get_widgets(wrench_widget_id) and \
                'spriteID' in qh.get_widgets(wrench_widget_id) and \
                qh.get_widgets(wrench_widget_id)['spriteID'] == 1030 and not called_butler:
            osrs.move.click(qh.get_widgets(house_widget_id))
            osrs.clock.sleep_one_tick()
        elif qh.get_widgets(call_servant_widget_id) and \
                qh.get_widgets(wrench_widget_id) and \
                'spriteID' in qh.get_widgets(wrench_widget_id) and \
                qh.get_widgets(wrench_widget_id)['spriteID'] == 1030 and not called_butler:
            osrs.move.click(qh.get_widgets(call_servant_widget_id))
            osrs.clock.sleep_one_tick()
            called_butler = True
        elif qh.get_widgets(wrench_widget_id) and not called_butler:
            osrs.move.click(qh.get_widgets(wrench_widget_id))
            osrs.clock.sleep_one_tick()
        elif qh.get_widgets(chat_box_input_widget_id) and requested_planks:
            osrs.keeb.keyboard.type('20')
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
    go_to_dungeon()


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
