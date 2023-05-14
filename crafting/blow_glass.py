from autoscape import general_utils
import keyboard
import math
import datetime
import random
import time


def craft():
    data = general_utils.get_player_info(8814)
    crafting_level = data["craftingLevel"]
    item_to_make = determine_item_to_make(crafting_level)
    general_utils.antiban_rest()
    for item in data["inv"]:
        if item["id"] == 1785:
            general_utils.move_and_click(item["x"], item["y"], 8, 8)
            break
    for item in data["inv"]:
        if item["id"] == 1775:
            general_utils.move_and_click(item["x"], item["y"], 8, 8)
            break
    general_utils.random_sleep(.9, 1.2)
    keyboard.send(item_to_make)
    general_utils.random_sleep(0.3, 0.4)

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


def main():
    start_time = datetime.datetime.now()
    while True:
        take_break = general_utils.break_every_hour(random.randint(56, 63), start_time)
        if take_break:
            general_utils.logout()
            break_start_time = datetime.datetime.now()
            while (datetime.datetime.now() - break_start_time).total_seconds() < random.randint(587, 874):
                time.sleep(5)
                general_utils.click_off_screen()
            start_time = datetime.datetime.now()
            general_utils.login('pass_70')
            general_utils.random_sleep(0.4, 0.5)
        data = general_utils.get_player_info(8814)
        crafting_level = data["craftingLevel"]
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
            general_utils.move_and_click(math.floor(closest_npc["x"]),math.floor( closest_npc["y"]), 5, 6)
        while True:
            loc = general_utils.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
            if loc:
                break
        # dump everything other than my pipe
        if len(data['inv']) != 1:
            for item in data['inv']:
                if item['id'] != 1785:
                    general_utils.move_and_click(item['x'], item['y'], 5, 5)
                    break
        data = general_utils.get_player_info(8814)
        found = False
        if data["bank"]:
            for item in data["bank"]:
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

main()