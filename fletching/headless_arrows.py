from osrs_utils import general_utils
import math
import keyboard

#need to be able to handle level ups
def main():
    while True:
        data = general_utils.get_player_info(8814)
        fletching_level = data["fletchingLevel"]
        materials = {}
        for item in data["inv"]:
            if item["id"] == 52 or item["id"] == 314:
                materials[item["id"]] = item["quantity"]
                general_utils.move_and_click(item["x"], item["y"], 8, 8)

        general_utils.random_sleep(.9, 1.2)
        keyboard.send('space')
        general_utils.random_sleep(0.3, 0.4)
        general_utils.click_off_screen()
        print(materials)
        while True:
            data = general_utils.get_player_info(8814)
            if fletching_level != data["fletchingLevel"]:
                general_utils.antiban_rest()
                break
            # 150 arrows have been made, we are now idle
            found = False
            for item in data["inv"]:
                if item["id"] == 52 or item["id"] == 314:
                    print('x', materials[item["id"]] - 150, item["quantity"])
                    if materials[item["id"]] - 150 == item["quantity"]:
                        general_utils.antiban_rest()
                        found = True
                        break
            if found:
                break

main()