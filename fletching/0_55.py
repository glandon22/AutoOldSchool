from autoscape import general_utils
import math
import keyboard

def determine_log(lvl):
    if lvl < 20:
        return 1511  # logs
    elif lvl < 35:
        return 1521  # oak logs
    elif lvl < 50:
        return 1519  # willow logs
    elif lvl < 55:
        return 1517  # maple logs
    else:
        return None

def determine_button(lvl):
    if lvl < 5:
        return '1'  # arrow shafts
    elif lvl < 10:
        return '3'  # shortbow
    elif lvl < 20:
        return '4'  # longbow
    elif lvl < 25:
        return '2'  # shortbow
    elif lvl < 35:
        return '3'  # longbow
    elif lvl < 40:
        return '2'  # shortbow
    elif lvl < 50:
        return '3'  # longbow
    elif lvl < 55:
        return '2'  # shortbow
    else:
        return None

def main():
    general_utils.random_sleep(5, 6)
    while True:
        general_utils.antiban_rest()
        data = general_utils.get_player_info(8814)
        fletching_level = data['fletchingLevel']
        log_to_withdraw = determine_log(fletching_level)
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
        data = general_utils.get_player_info(8814)
        # dump everything other than my knife
        if len(data['inv']) != 1:
            items_not_to_click = [946, log_to_withdraw]
            for item in data['inv']:
                if item['id'] not in items_not_to_click:
                    items_not_to_click.append(item['id'])
                    general_utils.move_and_click(item['x'], item['y'], 5, 5)
        found_log = False
        if data["bank"]:
            for item in data["bank"]:
                if item["id"] == log_to_withdraw:
                    found_log = True
                    general_utils.move_and_click(item["x"], item["y"], 8, 8)
            if not found_log:
                print('didnt find log')
                return
            keyboard.send('esc')
            general_utils.random_sleep(0.9, 1.1)
        data = general_utils.get_player_info(8814)
        general_utils.antiban_rest()
        for item in data["inv"]:
            if item["id"] == 946:  # knife
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
                break
        for item in data["inv"]:
            if item["id"] == log_to_withdraw:
                general_utils.move_and_click(item["x"], item["y"], 8, 8)
                break
        general_utils.random_sleep(.9, 1.2)
        keyboard.send(determine_button(fletching_level))
        general_utils.random_sleep(0.3, 0.4)
        general_utils.click_off_screen()
        while True:
            data = general_utils.get_player_info(8814)
            found = False
            for item in data["inv"]:
                if item["id"] == log_to_withdraw:
                    found = True
                    break
            if not found:
                break
            elif data['fletchingLevel'] != fletching_level:
                break
main()