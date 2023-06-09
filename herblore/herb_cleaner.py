
import osrs
import math
import time
import keyboard


def main():
    # guam 199
    # marrentill 201
    while True:
        data = osrs.server.get_player_info(8814)
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
            osrs.move.move_and_click(math.floor(closest_npc["x"]),math.floor( closest_npc["y"]), 5, 6)

        while True:
            loc = osrs.util.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
            if loc:
                break
        if data.get("inv") is not None:
            loc = osrs.util.rough_img_compare('..\\screens\\dump.png', .9, (0, 0, 1920, 1080))
            osrs.move.move_and_click(loc[0] + 5, loc[1] + 5, 4, 4)
            osrs.clock.random_sleep(.5,.6)
        data = osrs.server.get_player_info(8814)
        if data["bank"]:
            for item in data["bank"]:
                if item["id"] == 201:
                    osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                    osrs.clock.random_sleep(0.3, 0.7)
                    keyboard.send('esc')
                    osrs.clock.random_sleep(0.9, 1.1)
        data = osrs.server.get_player_info(8814)
        osrs.inv.power_drop(data["inv"], [], [201])
        osrs.move.click_off_screen()
        osrs.clock.random_sleep(1.4, 1.9)



main()