import time
import math
from osrs_utils import general_utils
import random


supported_food = [
    329,  # salmon
    361, # tuna
]


def main():
    while True:
        # Find monster to kill
        cycles = 0
        while True:
            cycles += 1
            if cycles > 50:
                return
            data = general_utils.get_player_info(8889)
            if not data or len(data["npcs"]) == 0:
                continue
            closest = general_utils.find_closest_npc(data["npcs"])
            if closest["x"] is None or closest["y"] is None:
                time.sleep(1)
                continue
            general_utils.quick_click(math.floor(closest['x']), math.floor(closest['y']))
            general_utils.random_sleep(0.7, 0.8)
            data = general_utils.get_player_info(8889)
            if data and data["interactingWith"] != "not interacting":
                general_utils.click_off_screen()
                break
        # monitor health and wait to kill npc
        while True:
            data = general_utils.get_player_info(8889)
            if data["hpLevel"] / data["unboostedHpLevel"] < 0.6:
                food = general_utils.are_items_in_inventory(data['inv'], supported_food)
                if not food:
                    print('cant find food')
                    return
                general_utils.move_and_click(food[0], food[1], 4, 6)
                break
            elif data and data["interactingWith"] == "not interacting":
                general_utils.random_sleep(2.5, 2.6)
                break
            # do some random mouse movements
            if random.randint(1, 50) == 1:
                general_utils.move_around_center_screen()
                general_utils.click_off_screen()

main()
