
import osrs
import math
import keyboard

#need to be able to handle level ups
def main():
    while True:

        osrs.clock.antiban_rest()
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
        # dump everything other than my knife
        if len(data['inv']) != 1:
            for item in data['inv']:
                if item['id'] != 21622:
                    osrs.move.move_and_click(item['x'], item['y'], 5, 5)
                    break
        data = osrs.server.get_player_info(8814)
        if data["bank"]:
            for item in data["bank"]:
                if item["id"] == 6034:
                    osrs.move.move_and_click(item["x"], item["y"], 8, 8)
            keyboard.send('esc')
            osrs.clock.random_sleep(0.9, 1.1)
        data = osrs.server.get_player_info(8814)
        osrs.clock.antiban_rest()
        for item in data["inv"]:
            if item["id"] == 21622:
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                break
        for item in data["inv"]:
            if item["id"] == 6034:
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                break
        osrs.clock.random_sleep(.9, 1.2)
        keyboard.send('space')
        osrs.clock.random_sleep(0.3, 0.4)
        osrs.move.click_off_screen()
        while True:
            data = osrs.server.get_player_info(8814)
            found = False
            for item in data["inv"]:
                if item["id"] == 6034:
                    found = True
                    break
            if not found:
                break
main()