# varrok tele 8007
# reg log 1511
# right tile to be in is 3212, 3429, 0
import random

import pyautogui

from osrs_utils import general_utils
import keyboard
import math
#bank
#get logs
# decide which spot to go to
# go to spot
# burn logs
# return to bank
def select_log(lvl):
    if lvl < 15:
        return 1511
    elif lvl < 30:
        return 1521
    elif lvl < 45:
        return 1519
    else:
        return 1517

def main():
    items_to_keep = [
        8007,  # varr tab
        590,  # tinderbox
    ]
    while True:
        general_utils.antiban_rest()
        data = general_utils.get_player_info(6890)
        fm_level = data['fmLevel']
        log = select_log(fm_level)
        if log not in items_to_keep:
            items_to_keep = [8007, 590, log]
        if len(data["npcs"]) != 0:
            closest_npc = {
                "dist": 999,
                "x": None,
                "y": None
            }
            for npc in data["npcs"]:
                if npc["dist"] < closest_npc["dist"]:
                    closest_npc = {
                        "dist": npc["dist"],
                        "x": npc["x"],
                        "y": npc["y"]
                    }
            general_utils.move_and_click(closest_npc["x"], closest_npc["y"], 5, 6)

        while True:
            loc = general_utils.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
            if loc:
                break
        # dump everything other than my tinderbox and varr teles
        if len(data['inv']) != 2:
            for item in data['inv']:
                if item['id'] not in items_to_keep:
                    general_utils.move_and_click(item['x'], item['y'], 5, 5)
                    break
        data = general_utils.get_player_info(6890)
        if data["bank"]:
            for item in data["bank"]:
                if item["id"] == log:
                    general_utils.move_and_click(item["x"], item["y"], 8, 8)
                    break
            keyboard.send('esc')
            general_utils.random_sleep(0.9, 1.1)
        general_utils.antiban_rest()
        data = general_utils.get_player_info(6890)
        for item in data["inv"]:
            if item["id"] == 8007:  # varr tab
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
                break
        general_utils.random_sleep(4, 4.3)
        while True:
            data = general_utils.get_player_info(6890)
            print('debug', data['tiles'])
            if len(data['tiles']) < 1:
                general_utils.random_sleep(0.9, 1.1)
            else:
                general_utils.move_and_click(data['tiles'][0]['x'], data['tiles'][0]["y"], 8, 8)
                break
        #wait to arrive on tile to start burning
        while True:
            wp = general_utils.get_player_info(6890)['worldPoint']
            if wp['x'] == 3212 and wp['y'] == 3429:
                break
            general_utils.random_sleep(0.5, 0.6)
        while True:
            data = general_utils.get_player_info(6890)
            if len(data['inv']) <= 2:
                break
            for item in data['inv']:
                if item['id'] == 590:
                    general_utils.move_and_click(item['x'], item['y'], 5, 5)
                    general_utils.random_sleep(0.3, 0.6)
                elif item['id'] == log:
                    general_utils.move_and_click(item['x'], item['y'], 5, 5)
                    general_utils.random_sleep(0.3, 0.6)
                    break
            fm_xp = data['fmXp']
            general_utils.click_off_screen(
                random.randint(2000, 2100),
                random.randint(2300, 2400),
                random.randint(100, 110),
                random.randint(170, 180),
                False
            )
            while True:
                data = general_utils.get_player_info(6890)
                if fm_xp != data['fmXp']:
                    break


main()
