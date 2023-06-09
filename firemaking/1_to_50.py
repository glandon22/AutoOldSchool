import osrs
# varrok tele 8007
# reg log 1511
# right tile to be in is 3212, 3429, 0
import pyautogui


import osrs
import keyboard
import math
#bank
#get logs
# decide which spot to go to
# go to spot
# burn logs
# return to bank
items_to_keep = [
    8007,  # varr tab
    590,  # tinderbox
]
def select_log(lvl):
    if lvl < 15:
        return 1511
    elif lvl < 30:
        return 1521
    elif lvl < 50:
        return 1519
    else:
        return 1517

def main():
    prev_tile = None
    while True:
        osrs.clock.antiban_rest()
        data = osrs.server.get_player_info(6890)
        fm_level = data['fmLevel']
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
            osrs.move.move_and_click(closest_npc["x"], closest_npc["y"], 5, 6)

        while True:
            loc = osrs.util.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
            if loc:
                break
        # dump everything other than my tinderbox and varr teles
        if len(data['inv']) != 2:
            for item in data['inv']:
                if item['id'] not in items_to_keep:
                    osrs.move.move_and_click(item['x'], item['y'], 5, 5)
                    break
        data = osrs.server.get_player_info(6890)
        if data["bank"]:
            for item in data["bank"]:
                if item["id"] == select_log(fm_level):
                    osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                    break
            keyboard.send('esc')
            osrs.clock.random_sleep(0.9, 1.1)
        osrs.clock.antiban_rest()
        data = osrs.server.get_player_info(6890)
        if prev_tile != 's1':
            tile = data['tiles'][0]
            osrs.move.move_and_click(tile['x'], tile['y'], 3, 3)
            prev_tile = 's1'
        else:
            tile = data['tiles'][1]
            osrs.move.move_and_click(tile['x'], tile['y'], 3, 3)
            prev_tile = 's2'
        #wait to arrive on tile to start burning
        while True:
            wp = osrs.server.get_player_info(6890)['worldPoint']
            if prev_tile == 's1':
                if wp['x'] == 3200 and wp['y'] == 3431:
                    break
            else:
                if wp['x'] == 3200 and wp['y'] == 3432:
                    break
        while True:
            data = osrs.server.get_player_info(6890)
            if len(data['inv']) == 1:
                break

            for item in data['inv']:
                if item['id'] == 590:
                    osrs.move.move_and_click(item['x'], item['y'], 5, 5)
                    osrs.clock.random_sleep(0.3, 0.6)
                elif item['id'] == select_log(fm_level):
                    osrs.move.move_and_click(item['x'], item['y'], 5, 5)
                    osrs.clock.random_sleep(0.3, 0.6)
                    break
            fm_xp = data['fmXp']
            while True:
                data = osrs.server.get_player_info(6890)
                if fm_xp != data['fmXp']:
                    break



main()

