import time
import math
from osrs_utils import general_utils
import random


supported_food = [
    329,  # salmon
    361, # tuna
]

items_to_loot = [
    563, # law rune
    562, # chaos rune
    561, # nature rune
    564, # cosmic
    565, # blood rune
    560, # death rune
    5295, # ranarr seed
    5300, # snapdragon seed
    5304, # torstol seed
    22374, # mossy key
]

def findMonsterToKill(npc_to_ignore):
    print('k',npc_to_ignore)
    # Find monster to kill
    id = -1
    cycles = 0
    while True:
        print('00000')
        cycles += 1
        if cycles > 50:
            return 'too many cycles'
        data = general_utils.get_player_info(8889)
        if not data or len(data["npcs"]) == 0:
            print('kkkk')
            continue
        closest = general_utils.find_closest_npc(data["npcs"], npc_to_ignore)
        if closest["x"] is None or closest["y"] is None:
            print('zzzzzz', closest)
            time.sleep(1)
            continue
        general_utils.quick_click(math.floor(closest['x']), math.floor(closest['y']))
        id = closest['id']
        general_utils.random_sleep(0.7, 0.8)
        data = general_utils.get_player_info(8889)
        if data and data["interactingWith"] != "not interacting":
            print('here1111')
            general_utils.click_off_screen()
            return id


def get_loot():
    while True:
        found_something = False
        data = general_utils.get_player_info(8889)
        if len(data['groundItems']) != 0:
            for item in data['groundItems']:
                if item['id'] in items_to_loot:
                    found_something = True
                    general_utils.move_and_click(item['x'], item['y'], 2, 2, 'right')
                    general_utils.random_sleep(0.3, 0.4)
                    take = general_utils.rough_img_compare('..\\screens\\take.png', 0.8, (0, 0, 1920, 1080))
                    print('take', take)
                    if not take:
                        return
                    general_utils.move_and_click(take[0] + take[2], take[1] + take[3], 3, 3)
                    prev_inv = general_utils.get_player_info(8889)['inv']
                    # wait until i pick up the thing
                    while True:
                        curr_inv = general_utils.get_player_info(8889)['inv']
                        if curr_inv != prev_inv:
                            break
        if not found_something:
            break


def main():
    attacking_npc = -1
    while True:
        # find npc to kill and save its id
        attacking_npc = findMonsterToKill(attacking_npc)
        if isinstance(attacking_npc, str):
            return attacking_npc
        while True:
            data = general_utils.get_player_info(8889)
            if data["hpLevel"] / data["unboostedHpLevel"] < 0.6:
                food = general_utils.are_items_in_inventory(data['inv'], supported_food)
                if not food:
                    print('cant find food')
                    return
                general_utils.move_and_click(food[0], food[1], 4, 6)
                break
            # i have killed the npc
            elif data and data["interactingWith"] == "not interacting":
                print('here', data)
                get_loot()
                break
            # do some random mouse movements
            if random.randint(1, 50) == 1:
                general_utils.move_around_center_screen()
                general_utils.click_off_screen()

main()
