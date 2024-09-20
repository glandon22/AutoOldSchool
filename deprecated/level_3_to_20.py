
import osrs
import math


def find_bank(data):
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
        osrs.move.move_and_click(math.floor(closest_npc["x"]), math.floor(closest_npc["y"]), 5, 6)

    while True:
        loc = osrs.util.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
        if loc:
            break
    data = osrs.server.get_player_info(8815)
    if data["bank"]:
        for item in data["bank"]:
            #steel bar 2353
            # iron bar 2351
            #mith bar 2359
            if item["id"] == 2349:
                osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                osrs.clock.random_sleep(0.3, 0.7)


def smith():
    data = osrs.server.get_player_info(8815)
    if len(data["inv"]) <= 2:
        return print('nothing in inv to smith')
    if data.get("anvil") is not None:
        osrs.move.move_and_click(data["anvil"]["x"] + 5, data["anvil"]["y"] + 5, 4, 4)
    while True:
        loc = osrs.util.rough_img_compare('..\\screens\\bronze_bolts.png', .7, (0, 0, 1920, 1080))
        if loc:
            osrs.clock.random_sleep(0.2, 0.3)
            osrs.move.move_and_click(loc[0] + 7, loc[1] + 7, 5, 5)
            osrs.clock.random_sleep(0.3, 0.4)
            osrs.move.click_off_screen()
            break


def main():
    while True:
        data = osrs.server.get_player_info(8815)
        smith_lvl = data["smithingLevel"]
        if smith_lvl >= 20:
            return
        find_bank(data)
        smith()
        # from here, need to handle levels and wait until bag is fully smithed
        while True:
            data = osrs.server.get_player_info(8815)
            if len(data["inv"]) == 2:
                break
            elif data["smithingLevel"] != smith_lvl:
                smith_lvl = data["smithingLevel"]
                smith()
        osrs.clock.antiban_rest()



main()
