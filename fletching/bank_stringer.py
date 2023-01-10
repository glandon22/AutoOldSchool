import datetime
import random
import time

from osrs_utils import general_utils
import math
import keyboard

def string():
    data = general_utils.get_player_info(8814)
    for item in data["inv"]:
        # 66 yew long
        # 70 mage long
        # 62 maple long
        if item["id"] == 1777:
            general_utils.move_and_click(item["x"], item["y"], 8, 8)
            break
    for item in data["inv"]:
        if item["id"] == 66:
            general_utils.move_and_click(item["x"], item["y"], 8, 8)
            break
    general_utils.random_sleep(.9, 1.2)
    keyboard.send('space')
    general_utils.random_sleep(0.3, 0.4)
    general_utils.click_off_screen()

#need to be able to handle level ups
def main():
    fletching_level = -1
    start_time = datetime.datetime.now()
    while True:
        take_break = general_utils.break_every_hour(random.randint(53, 69), start_time)
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
        fletching_level = data['fletchingLevel']
        print(data)
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
        if data.get("inv") is not None:
            loc = general_utils.rough_img_compare('..\\screens\\dump.png', .9, (0, 0, 1920, 1080))
            general_utils.move_and_click(loc[0] + 5, loc[1] + 5, 4, 4)
            general_utils.random_sleep(.5,.6)
        data = general_utils.get_player_info(8814)
        if data["bank"]:
            for item in data["bank"]:
                if item["id"] == 66 or item["id"] == 1777:
                    general_utils.move_and_click(item["x"], item["y"], 8, 8)
            keyboard.send('esc')
            general_utils.random_sleep(0.9, 1.1)
        string()
        while True:
            data = general_utils.get_player_info(8814)
            if 'inv' in data and len(data["inv"]) == 14:
                general_utils.antiban_rest(40, 100, 150)
                break
            elif data['fletchingLevel'] != fletching_level:
                fletching_level = data['fletchingLevel']
                string()
main()