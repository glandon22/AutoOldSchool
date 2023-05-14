import time

from autoscape import general_utils
import pyautogui
import random
def main():
    # find the npc i want to slaughter
    # find the closest one, then click it
    # check if i clicked
        # if not retry

    # make sure my health is above a certain level
        # if it falls below eat
            # if i dont have food exit

    #once im done killing, repeat
    while True:
        while True:
            data = general_utils.get_player_info(8889)
            print(data["npcs"])
            if not data:
                continue
            if len(data["npcs"]) == 0:
                time.sleep(1)
                continue
            closest = {
                "dist": 999,
                "x": None,
                "y": None
            }
            for npc in data["npcs"]:
                if npc["dist"] < closest["dist"]:
                    closest = {
                        "dist": npc["dist"],
                        "x": npc["x"],
                        "y": npc["y"]
                    }
            general_utils.advanced_move_and_click(closest["x"], closest["y"], 3, 3)
            general_utils.random_sleep(0.6, 0.7)
            general_utils.move_around_center_screen()
            data = general_utils.get_player_info(8889)
            if data and data["interactingWith"] != "not interacting":
                break
        while True:
            data = general_utils.get_player_info(8889)
            if data and data["interactingWith"] == "not interacting":
                general_utils.random_sleep(2.6, 2.76)
                break
            if random.randint(1, 11) == 1:
                general_utils.move_around_center_screen()

main()