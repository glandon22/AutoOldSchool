from osrs_utils import general_utils
import math
import keyboard

#need to be able to handle level ups
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
                if item["id"] == 13421 or item["id"] == 6032:
                    general_utils.move_and_click(item["x"], item["y"], 8, 8)
            keyboard.send('esc')
            general_utils.random_sleep(0.9, 1.1)
        data = general_utils.get_player_info(8814)
        for item in data["inv"]:
            if item["id"] == 13421:
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
                break
        for item in data["inv"]:
            if item["id"] == 6032:
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
                break
        general_utils.random_sleep(.9, 1.2)
        general_utils.click_off_screen()
        cycles = 0
        while True:
            if cycles > 250:
                break
            data = general_utils.get_player_info(8814)
            if len(data["inv"]) == 14:
                general_utils.antiban_rest()
                break
            cycles += 1
main()