from osrs_utils import general_utils
import math
import time
import keyboard


def main():
    while True:
        data = general_utils.get_player_info(8814)
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
                if item["id"] == 205:
                    general_utils.move_and_click(item["x"], item["y"], 8, 8)
                    general_utils.random_sleep(0.3, 0.7)
                    keyboard.send('esc')
                    general_utils.random_sleep(0.9, 1.1)
        data = general_utils.get_player_info(8814)
        general_utils.power_drop(data["inv"], [], [205])
        general_utils.click_off_screen()
        general_utils.random_sleep(1.4, 1.9)
        general_utils.antiban_randoms()
        general_utils.antiban_randoms()



main()