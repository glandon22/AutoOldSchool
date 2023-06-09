
import osrs
import math
import keyboard

#need to be able to handle level ups
def main():
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

        osrs.bank.wait_for_bank_interface('56799')
        if data.get("inv") is not None:
            loc = osrs.util.rough_img_compare('..\\screens\\dump.png', .9, (0, 0, 1920, 1080))
            osrs.move.move_and_click(loc[0] + 5, loc[1] + 5, 4, 4)
            osrs.clock.random_sleep(.5,.6)
        data = osrs.server.get_player_info(8814)
        if data["bank"]:
            for item in data["bank"]:
                if item["id"] == 13421 or item["id"] == 6032:
                    osrs.move.move_and_click(item["x"], item["y"], 8, 8)
            keyboard.send('esc')
            osrs.clock.random_sleep(0.9, 1.1)
        data = osrs.server.get_player_info(8814)
        for item in data["inv"]:
            if item["id"] == 13421:
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                break
        for item in data["inv"]:
            if item["id"] == 6032:
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                break
        osrs.clock.random_sleep(.9, 1.2)
        osrs.move.click_off_screen()
        cycles = 0
        while True:
            if cycles > 250:
                break
            data = osrs.server.get_player_info(8814)
            if len(data["inv"]) == 14:
                osrs.clock.antiban_rest()
                break
            cycles += 1
main()