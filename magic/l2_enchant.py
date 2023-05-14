from autoscape import general_utils
import math
import keyboard

#1639 emerald ring
#2552 ring of dueling

#start with interface open to spell book
#bank
#dump all items other than cosmic runes
#withdraw emerald rings
#close bank
#loop until no emerald riungs left
    #get inv info
    #click spell
    #cick first emerald ring
#repeat


def main():
    while True:
        general_utils.antiban_rest()
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
            general_utils.move_and_click(math.floor(closest_npc["x"]), math.floor(closest_npc["y"]), 5, 6)
            while True:
                loc = general_utils.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
                if loc:
                    break
            # dump everything other than my cosmic runes
            if len(data['inv']) != 1:
                for item in data['inv']:
                    if item['id'] != 564:
                        general_utils.move_and_click(item['x'], item['y'], 5, 5)
                        break
            data = general_utils.get_player_info(8814)
            if data["bank"]:
                for item in data["bank"]:
                    if item["id"] == 1639:
                        general_utils.move_and_click(item["x"], item["y"], 8, 8)
                keyboard.send('esc')
                general_utils.random_sleep(0.9, 1.1)

            # begin enchanting
            while True:
                spell = general_utils.rough_img_compare('..\\screens\\l2_enchant.png', .9, (1500, 500, 1920, 1080))
                general_utils.move_and_click(spell[0] + 5, spell[1] + 5, 4, 4)
                data = general_utils.get_player_info(8814)
                found_emerald_ring = False
                for item in data["inv"]:
                    if item["id"] == 1639:
                        general_utils.move_and_click(item["x"], item["y"], 8, 8)
                        general_utils.move_around_center_screen(1700, 600, 1750, 650)
                        found_emerald_ring = True
                        break
                if not found_emerald_ring:
                    # click on first item to cancel spell out and get back to magic interface
                    for item in data["inv"]:
                        general_utils.move_and_click(item["x"], item["y"], 8, 8)
                        break
                    break
                general_utils.random_sleep(0.5, 0.6)


main()
