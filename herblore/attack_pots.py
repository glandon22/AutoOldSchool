
import osrs
import osrs
# guam 91
# newt 221

import datetime

import osrs
import keyboard
# 91 guam unf
# 227 vial water
POT = 99
# newt 221
SECONDARY = 231


def make_pot(port):
    inv = osrs.inv.get_inv(port)
    pot = osrs.inv.is_item_in_inventory_v2(inv, POT)
    osrs.move.move_and_click(pot['x'], pot['y'], 3, 3)
    secondary = osrs.inv.is_item_in_inventory_v2(inv, SECONDARY)
    osrs.move.move_and_click(secondary['x'], secondary['y'], 3, 3)
    osrs.clock.random_sleep(.9, 1.2)
    keyboard.send('space')
    osrs.clock.random_sleep(0.3, 0.4)
    osrs.move.click_off_screen(click=False)


def click_banker(port):
    q = {
        'npcs': ['Banker']
    }
    data = osrs.server.query_game_data(q, port)
    if len(data["npcs"]) != 0:
        closest = osrs.util.find_closest_npc(data['npcs'])
        osrs.move.move_and_click(closest['x'], closest['y'], 5, 6)


def dump_inventory_in_bank(port):
    q = {
        'inv': True
    }
    data = osrs.server.query_game_data(q, port)
    if 'inv' in data and len(data['inv']) > 0:
        print('Dumping inventory.')
        q = {
            'dumpInvButton': True
        }
        while True:
            data = osrs.server.query_game_data(q, port)
            if 'dumpInvButton' in data:
                center = data['dumpInvButton']
                osrs.move.move_and_click(center['x'], center['y'], 10, 10)
                osrs.clock.random_sleep(.5, .6)
                break


def withdraw_materials(port):
    found_pot = False
    found_secondary = False
    while True:
        data = osrs.bank.get_bank_data(port)
        for item in data:
            if item["id"] == POT:
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                found_pot = True
            elif item["id"] == SECONDARY:
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                found_secondary = True
        keyboard.send('esc')
        break
    if not found_secondary or not found_pot:
        print(data)
        exit("no more pots or secondaries")
    osrs.clock.random_sleep(0.9, 1.1)


def make_pots(port):
    while True:
        inv = osrs.inv.get_inv(port)
        leveled_up_widget = osrs.server.get_widget('233,0', port)
        if not osrs.inv.are_items_in_inventory_v2(inv, [POT, SECONDARY]):
            print('Bag completed.')
            print('Clicking on banker.')
            click_banker(port)
            print('Waiting for bank interface to open.')
            osrs.clock.random_sleep(1.1, 1.3)
            dump_inventory_in_bank(port)
            print('Withdrawing potion materials.')
            withdraw_materials(port)
            print('Making pots.')
            make_pot(port)
        elif leveled_up_widget:
            make_pot(port)
        else:
            make_pot('56799')

make_pots('56799')
