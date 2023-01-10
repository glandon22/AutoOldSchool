import datetime
from osrs_utils import general_utils
import keyboard

BOWSTRING = 1777
# 66 yew long
# 70 mage long
# 62 maple long
UNSTRUNG_BOW = 70


def string():
    q = {
        'inv': True
    }
    data = general_utils.query_game_data(q)
    for item in data["inv"]:
        if item["id"] == 1777:
            general_utils.move_and_click(item["x"], item["y"], 8, 8)
            break
    for item in data["inv"]:
        if item["id"] == UNSTRUNG_BOW:
            general_utils.move_and_click(item["x"], item["y"], 8, 8)
            break
    general_utils.random_sleep(.9, 1.2)
    keyboard.send('space')
    general_utils.random_sleep(0.3, 0.4)
    general_utils.click_off_screen()


def click_banker():
    q = {
        'npcs': ['Banker']
    }
    data = general_utils.query_game_data(q)
    if len(data["npcs"]) != 0:
        closest = general_utils.find_closest_npc(data['npcs'])
        general_utils.move_and_click(closest['x'], closest['y'], 5, 6)


def dump_inventory_in_bank():
    q = {
        'inv': True
    }
    data = general_utils.query_game_data(q)
    if 'inv' in data and len(data['inv']) > 0:
        print('Dumping inventory.')
        q = {
            'dumpInvButton': True
        }
        while True:
            data = general_utils.query_game_data(q)
            if 'dumpInvButton' in data:
                center = data['dumpInvButton']
                general_utils.move_and_click(center['x'], center['y'], 10, 10)
                general_utils.random_sleep(.5, .6)
                break


def withdraw_materials():
    q = {
        'bank': True
    }
    found_unstrung = False
    found_bowstring = False
    while True:
        data = general_utils.query_game_data(q)
        if 'bankItems' in data and len(data['bankItems']) > 0:
            for item in data["bankItems"]:
                if item["id"] == UNSTRUNG_BOW:
                    general_utils.move_and_click(item["x"], item["y"], 8, 8)
                    found_unstrung = True
                elif item["id"] == BOWSTRING:
                    general_utils.move_and_click(item["x"], item["y"], 8, 8)
                    found_bowstring = True
            keyboard.send('esc')
            break
    if not found_bowstring or not found_unstrung:
        exit("no more unstrung bows or bowstrings")
    general_utils.random_sleep(0.9, 1.1)


def get_fletching_level():
    q = {
        'skills': ['fletching']
    }
    data = general_utils.query_game_data(q)
    return data['skills']['fletching']['level']


def main():
    fletching_level = get_fletching_level()
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 53, 69, 587, 874, 'pass_70')
        print('Clicking on banker.')
        click_banker()
        print('Waiting for bank interface to open.')
        general_utils.random_sleep(1.1, 1.3)
        dump_inventory_in_bank()
        print('Withdrawing fletching materials.')
        withdraw_materials()
        print('Stringing bows.')
        string()
        while True:
            # Throttle calls to the backend slightly
            general_utils.random_sleep(0.025, 0.026)
            q = {
                'skills': ['fletching'],
                'inv': True
            }
            data = general_utils.query_game_data(q)
            if 'inv' in data and not general_utils.are_items_in_inventory(data['inv'], [BOWSTRING, UNSTRUNG_BOW]):
                print('Bag completed stringing.')
                general_utils.antiban_rest(40, 100, 150)
                break
            elif data['skills']['fletching']['level'] != fletching_level:
                print('Leveled fletching. Stringing again.')
                fletching_level = data['skills']['fletching']['level']
                string()


main()

