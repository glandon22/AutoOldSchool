from osrs_utils import general_utils

# guam 91
# newt 221

import datetime
from osrs_utils import general_utils
import keyboard
# 91 guam unf
# 227 vial water
POT = 91
# newt 221
SECONDARY = 221


def make_pot(port):
    inv = general_utils.get_inv(port)
    pot = general_utils.is_item_in_inventory_v2(inv, POT)
    general_utils.move_and_click(pot['x'], pot['y'], 3, 3)
    secondary = general_utils.is_item_in_inventory_v2(inv, SECONDARY)
    general_utils.move_and_click(secondary['x'], secondary['y'], 3, 3)
    general_utils.random_sleep(.9, 1.2)
    keyboard.send('space')
    general_utils.random_sleep(0.3, 0.4)
    general_utils.click_off_screen(click=False)


def click_banker(port):
    q = {
        'npcs': ['Banker']
    }
    data = general_utils.query_game_data(q, port)
    if len(data["npcs"]) != 0:
        closest = general_utils.find_closest_npc(data['npcs'])
        general_utils.move_and_click(closest['x'], closest['y'], 5, 6)


def dump_inventory_in_bank(port):
    q = {
        'inv': True
    }
    data = general_utils.query_game_data(q, port)
    if 'inv' in data and len(data['inv']) > 0:
        print('Dumping inventory.')
        q = {
            'dumpInvButton': True
        }
        while True:
            data = general_utils.query_game_data(q, port)
            if 'dumpInvButton' in data:
                center = data['dumpInvButton']
                general_utils.move_and_click(center['x'], center['y'], 10, 10)
                general_utils.random_sleep(.5, .6)
                break


def withdraw_materials(port):
    found_pot = False
    found_secondary = False
    while True:
        data = general_utils.get_bank_data(port)
        for item in data:
            if item["id"] == POT:
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
                found_pot = True
            elif item["id"] == SECONDARY:
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
                found_secondary = True
        keyboard.send('esc')
        break
    if not found_secondary or not found_pot:
        print(data)
        exit("no more pots or secondaries")
    general_utils.random_sleep(0.9, 1.1)


def make_pots(port):
    inv = general_utils.get_inv(port)
    leveled_up_widget = general_utils.get_widget('233,0', port)
    if not general_utils.are_items_in_inventory_v2(inv, [POT, SECONDARY]):
        print('Bag completed.')
        print('Clicking on banker.')
        click_banker(port)
        print('Waiting for bank interface to open.')
        general_utils.random_sleep(1.1, 1.3)
        dump_inventory_in_bank(port)
        print('Withdrawing potion materials.')
        withdraw_materials(port)
        print('Making pots.')
        make_pot(port)
    elif leveled_up_widget:
        make_pot(port)

