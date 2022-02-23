from osrs_utils import general_utils
import math
import keyboard
# check my fishing level
# decide which fish to look for based on fishing level
# go bank
# if not empty, dump bag
# withdraw the needed fish
# cook the fish on the fire
# if i level, cook again, plan for muli levels per bag
# repeat
def determine_fish(lvl):
    if lvl < 5:
        return 327
    elif lvl < 10:
        return 345
    elif lvl < 15:
        return 353
    elif lvl < 20:
        return 335
    elif lvl < 25:
        return 349
    elif lvl < 30:
        return 331



def main():
    data = general_utils.get_player_info(3375)
    fish_to_cook = determine_fish(data["fishingLevel"])
    if len(data['npcs']) == 0:
        return
    else:
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
        general_utils.move_and_click(math.floor(closest_npc["x"]), math.floor(closest_npc["y"]), 5, 6)
    # wait for interface and withdraw item
    while True:
        loc = general_utils.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
        if loc:
            break
    if data['inv'] is not None:
        loc = general_utils.rough_img_compare('..\\screens\\dump.png', .9, (0, 0, 1920, 1080))
        general_utils.move_and_click(loc[0] + 5, loc[1] + 5, 4, 4)
        general_utils.random_sleep(.5, .6)
    data = general_utils.get_player_info(3375)
    if data["bank"]:
        for item in data["bank"]:
            if item["id"] == fish_to_cook:
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
                general_utils.random_sleep(0.3, 0.7)
    data = general_utils.get_player_info(3375)
    general_utils.antiban_rest()
    for item in data["inv"]:
        if item["id"] == fish_to_cook:
            general_utils.move_and_click(item["x"], item["y"], 8, 8)
            break
    for obj in data["fire"]:
        if obj['Id'] == 26185:
            general_utils.move_and_click(obj["x"], obj["y"], 8, 8)
            break
    general_utils.random_sleep(2, 3.1)
    keyboard.send('space')
