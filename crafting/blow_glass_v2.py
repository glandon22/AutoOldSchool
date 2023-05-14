from autoscape import general_utils
import keyboard
import math
import datetime
import random
import time


def craft():
    data = general_utils.get_skill_data('crafting')
    crafting_level = data['level']
    item_to_make = determine_item_to_make(crafting_level)
    inv = general_utils.get_inv()
    for item in inv:
        if item["id"] == 1785:
            general_utils.move_and_click(item["x"], item["y"], 8, 8)
            break
    for item in inv:
        if item["id"] == 1775:
            general_utils.move_and_click(item["x"], item["y"], 8, 8)
            break
    general_utils.random_sleep(.9, 1.2)
    keyboard.send(item_to_make)
    general_utils.click_off_screen(300, 1000, 400, 700, False)
    return crafting_level


def determine_item_to_make(lvl):
    if lvl < 4:
        return '1'
    elif lvl < 12:
        return '2'
    elif lvl < 33:
        return '3'
    elif lvl < 42:
        return '4'
    elif lvl < 46:
        return '5'
    elif lvl < 100:
        return '6'


def click_banker():
    q = {
        'npcs': ['Banker']
    }
    data = general_utils.query_game_data(q)
    if len(data["npcs"]) != 0:
        closest = general_utils.find_closest_npc(data['npcs'])
        general_utils.move_and_click(closest['x'], closest['y'], 5, 6)


def main():
    start_time = datetime.datetime.now()
    while True:
        data = general_utils.get_skill_data('crafting')
        crafting_level = data['level']
        click_banker()
        general_utils.wait_for_bank_interface()
        # dump everything other than my pipe
        inv = general_utils.get_inv()
        for item in inv:
            if item['id'] != 1785:
                general_utils.move_and_click(item['x'], item['y'], 5, 5)
                break
        bank = general_utils.get_bank_data()
        found = False
        for item in bank:
            if item["id"] == 1775:
                found = True
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
        keyboard.send('esc')
        if not found:
            general_utils.logout()
            print('out of glass')
            return

        general_utils.random_sleep(0.9, 1.1)
        craft()
        general_utils.click_off_screen()
        while True:
            data = general_utils.get_player_info(8814)
            found = False
            for item in data["inv"]:
                if item["id"] == 1775:
                    found = True
                    break
            if not found:
                break
            elif data['craftingLevel'] != crafting_level:
                craft()
                crafting_level = data['craftingLevel']
                general_utils.click_off_screen()


def complete_inv_on_login(port):
    inv = general_utils.get_inv(port)
    glass = general_utils.is_item_in_inventory_v2(inv, 1775)
    if glass:
        craft()


def blow_glass(crafting_lvl):
    inv = general_utils.get_inv()
    have_molten_glass = general_utils.is_item_in_inventory_v2(inv, 1775)
    if not have_molten_glass:
        click_banker()
        general_utils.wait_for_bank_interface()
        found = True
        while found:
            found = False
            inv = general_utils.get_inv()
            for item in inv:
                if item['id'] != 1785:
                    general_utils.move_and_click(item['x'], item['y'], 5, 5)
                    general_utils.random_sleep(0.6, 0.7)
                    found = True
                    break
        bank = general_utils.get_bank_data()
        found = False
        for item in bank:
            if item["id"] == 1775:
                found = True
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
        keyboard.send('esc')
        if not found:
            return print('out of glass')
        general_utils.random_sleep(0.8, 0.9)
        return craft()
    # handle leveling
    elif crafting_lvl != general_utils.get_skill_data('crafting'):
        return craft()

