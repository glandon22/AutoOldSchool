import datetime
import random
import time

import osrs
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
    if lvl < 15:
        return 327
    elif lvl < 25:
        return 335
    elif lvl < 40:
        return 331
    elif lvl < 71:
        return 359
    elif lvl < 85:
        return 377
    elif lvl < 99:
        return 371
    else:
        return 383


def cook_fish_on_fire(fish_to_cook):
    data = osrs.server.get_player_info(3375)
    found_fish = False
    for item in data["inv"]:
        if item["id"] == fish_to_cook:
            found_fish = True
            break
    if not found_fish:
        return print('didnt find any fish')
    for obj in data["fire"]:
        if obj['Id'] == 43475:
            osrs.move.move_and_click(obj["x"], obj["y"], 8, 8)
            break
    osrs.clock.random_sleep(.9, 1.2)
    keyboard.send('space')


def main():
    start_time = datetime.datetime.now()
    while True:
        take_break = osrs.clock.break_every_hour(random.randint(53, 59), start_time)
        if take_break:
            osrs.game.logout()
            break_start_time = datetime.datetime.now()
            while (datetime.datetime.now() - break_start_time).total_seconds() < random.randint(496, 631):
                time.sleep(5)
                osrs.move.click_off_screen()
            start_time = datetime.datetime.now()
            osrs.game.login_v2('pass_70')
            osrs.clock.random_sleep(0.4, 0.5)
        data = osrs.server.get_player_info(3375)
        cooking_level = data["cookingLevel"]
        fish_to_cook = determine_fish(cooking_level)
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
            osrs.move.move_and_click(math.floor(closest_npc["x"]), math.floor(closest_npc["y"]), 5, 6)
        # wait for interface and withdraw item
        while True:
            loc = osrs.util.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
            if loc:
                break
        if data.get('inv') is not None:
            loc = osrs.util.rough_img_compare('..\\screens\\dump.png', .9, (0, 0, 1920, 1080))
            osrs.move.move_and_click(loc[0] + 5, loc[1] + 5, 4, 4)
            osrs.clock.random_sleep(.5, .6)
        data = osrs.server.get_player_info(3375)
        if data["bank"]:
            found_fish = False
            for item in data["bank"]:
                if item["id"] == fish_to_cook:
                    osrs.move.move_and_click(item["x"], item["y"], 8, 8)
                    osrs.clock.random_sleep(0.3, 0.7)
                    found_fish = True
            if not found_fish:
                return print('no more fish to cook')
        keyboard.send('esc')
        osrs.clock.antiban_rest()
        cook_fish_on_fire(fish_to_cook)
        osrs.move.click_off_screen()
        #cook until the bag is full
        while True:
            data = osrs.server.get_player_info(3375)
            if data['isCooking']:
                osrs.clock.random_sleep(2.1, 2.4)
            elif data['cookingLevel'] != cooking_level:
                cooking_level = data['cookingLevel']
                cook_fish_on_fire(fish_to_cook)
                osrs.move.click_off_screen()
            if not osrs.inv.is_item_in_inventory(data['inv'], fish_to_cook):
                break


main()
