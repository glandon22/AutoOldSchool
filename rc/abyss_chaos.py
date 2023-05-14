'''# add 70 to y after click to move over ferox enclave
# # [161, 69] to get the equipment tab

q = {
    'widget': '161,69'
}
'''

# need to bank, find bank 26711 tile '3130,3632,0'
# dump air runes
# check if i need a new ring, if so withdraw and equip
# withdraw ess
# click free for all portal, 26645 on '3128,3626,0'
# wait a half second
# click home tele
# wait a sec
# click esc to get back to my inv
# repeat loop

# home tele 8013
import datetime

import keyboard
import pyautogui

from autoscape import general_utils

global port


def click_home_tab():
    inv = general_utils.get_inv()
    home_tab = general_utils.is_item_in_inventory(inv, 8013)
    general_utils.move_and_click(home_tab[0], home_tab[1], 4, 6)


def run_to_loc(steps):
    for step in steps:
        while True:
            data = general_utils.query_game_data({
                'tiles': [step]
            }, port)
            formatted_step = step.replace(',', '')
            if 'tiles' in data and formatted_step in data['tiles'] and data['tiles'][formatted_step]['y'] > 75:
                general_utils.move_and_click(data['tiles'][formatted_step]['x'], data['tiles'][formatted_step]['y'], 7,
                                             7)
                break
        general_utils.random_sleep(1, 1.1)
    general_utils.wait_until_stationary(port)
    general_utils.random_sleep(0.5, 0.6)


def click_ruins():
    while True:
        ruins = general_utils.get_game_object('3313,3255,0', '34817')
        if not ruins:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(ruins['x'], ruins['y'], 7, 7)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary()
            break


def click_altar():
    while True:
        altar = general_utils.get_game_object('2271,4842,0', '34769')
        if not altar:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(altar['x'], altar['y'], 7, 7)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary(port)
            break


def tele_to_altar():
    while True:
        inv = general_utils.get_inv(port)
        ess = general_utils.is_item_in_inventory(inv, 7936)
        if ess:
            break
    while True:
        equipment_tab = general_utils.get_widget('161,69', port)
        if not equipment_tab:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(equipment_tab['x'], equipment_tab['y'], 7, 7)
            general_utils.random_sleep(0.5, 0.6)
            break
    while True:
        neck_slot = general_utils.get_widget('387,17', port)
        if not neck_slot:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.right_click_menu_select(neck_slot, 2, port)
            keyboard.send('esc')
            general_utils.random_sleep(2, 2.1)
            break


def tele_to_ferox():
    while True:
        inv = general_utils.get_inv()
        ess = general_utils.is_item_in_inventory(inv, 7936)
        if not ess:
            break
    while True:
        equipment_tab = general_utils.get_widget('161,69')
        if not equipment_tab:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(equipment_tab['x'], equipment_tab['y'], 7, 7)
            general_utils.random_sleep(0.5, 0.6)
            break
    while True:
        ring_slot = general_utils.get_widget('387,24')
        if not ring_slot:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(ring_slot['x'], ring_slot['y'], 7, 7, 'right')
            general_utils.random_sleep(0.5, 0.6)
            # right click menus always open in the same place relative to where they are opened from,
            # so to access desired entry i just go down from my current y position
            current_y_mouse_val = pyautogui.position()[1]
            general_utils.move_and_click(ring_slot['x'], current_y_mouse_val + 69, 15, 0)
            keyboard.send('esc')
            general_utils.random_sleep(2, 2.1)
            break


def click_bank():
    while True:
        bank = general_utils.get_game_object('3130,3632,0', '26711', port)
        if not bank:
            general_utils.random_sleep(1, 2)
        else:
            general_utils.move_and_click(bank['x'], bank['y'], 7, 7)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.wait_until_stationary(port)
            break


def handle_banking(ring_charges, neck_charges):
    get_glory = False
    get_dueling = False
    if neck_charges == 0:
        glory = general_utils.find_item_in_bank(1712, port)
        general_utils.right_click_menu_select(glory, 2, port)
        general_utils.random_sleep(0.3, 0.4)
        get_glory = True
    if ring_charges == 0:
        dueling = general_utils.find_item_in_bank(2552, port)
        general_utils.right_click_menu_select(dueling, 2, port)
        general_utils.random_sleep(0.3, 0.4)
        get_dueling = True
    keyboard.send('esc')
    general_utils.random_sleep(0.3, 0.4)
    inv = general_utils.get_inv(port)
    if get_dueling:
        dueling = general_utils.is_item_in_inventory_v2(inv, 2552)
        general_utils.move_and_click(dueling['x'], dueling['y'], 3, 3)
    if get_glory:
        glory = general_utils.is_item_in_inventory_v2(inv, 1712)
        general_utils.move_and_click(glory['x'], glory['y'], 3, 3)
    click_bank()
    general_utils.wait_for_bank_interface(port)
    general_utils.bank_dump_inv(port)
    general_utils.random_sleep(0.3, 0.4)
    pure_ess = general_utils.find_item_in_bank(7936, port)
    general_utils.move_and_click(pure_ess['x'], pure_ess['y'], 3, 3)
    general_utils.random_sleep(0.3, 0.4)
    keyboard.send('esc')
    general_utils.random_sleep(0.3, 0.4)


def enter_ffa_portal():
    while True:
        portal = general_utils.get_game_object('3129,3626,0', '26645')
        if portal:
            general_utils.move_and_click(portal['x'], portal['y'], 3, 3)
            break
    while True:
        player_loc = general_utils.get_world_location()
        if player_loc and player_loc['y'] > 4000:
            general_utils.random_sleep(0.5, 0.6)
            break


def go_to_abyss():
    run_to_loc([
        '3087,3521,0'
    ])
    general_utils.random_sleep(0.6, 0.7)
    enter_wildy = general_utils.get_widget('475,11', port)
    if enter_wildy:
        general_utils.move_and_click(enter_wildy['x'], enter_wildy['y'], 8, 6)
    general_utils.random_sleep(2, 2.1)
    run_to_loc([
        '3089,3537,0',
        '3096,3547,0',
        '3099,3556,0'
    ])
    while True:
        q = {
            'npcsID': ['2581']
        }
        data = general_utils.query_game_data(q, port)
        if 'npcs' in data:
            for npc in data['npcs']:
                if npc['id'] == 2581:
                    general_utils.move_and_click(npc['x'], npc['y'], 2, 2)
                    targ = general_utils.get_target_npc(port)
                    print(targ)
                    if targ == 2581:
                        return
                    general_utils.random_sleep(1, 1.1)

# the right obstacles have dynamic ids, not sure how to get around this one
def find_obstacle():
    last_click = -1
    obstacle_key = -1
    while True:
        # 26251 26187 26188 26189 26208 26190
        obstacle = general_utils.get_surrounding_game_objects(10, [26208, 26250, 26574, 26188, 26192], port)
        found = False
        for key in obstacle.keys():
            general_utils.move_and_click(obstacle[key]['x'], obstacle[key]['y'], 2, 2)
            last_click = datetime.datetime.now()
            general_utils.random_sleep(0.5, 0.6)
            obstacle_key = key
            found = True
            break
        if found:
            break
    general_utils.wait_until_stationary(port)
    world_loc = general_utils.get_world_location(port)
    while True:
        curr = general_utils.get_world_location(port)
        if (last_click - datetime.datetime.now()).total_seconds() > 5:
            obstacle = general_utils.get_surrounding_game_objects(10, [obstacle_key], port)
            general_utils.move_and_click(obstacle[obstacle_key]['x'], obstacle[obstacle_key]['y'], 2, 2)
            last_click = datetime.datetime.now()
        elif curr != world_loc:
            break




def main(config_port):
    global port
    port = config_port

    trips = 0
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 47, 54, 423, 551, 'pass_71', False)
        tele_to_altar()
        general_utils.random_sleep(0.5, 0.6)
        click_ruins()
        click_altar()
        tele_to_ferox()
        trips += 1
        click_bank()
        general_utils.wait_for_bank_interface()
        handle_banking(trips % 8, trips % 4)
        enter_ffa_portal()


port = '56800'
find_obstacle()

