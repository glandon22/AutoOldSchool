import datetime
import random
import time
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

cooking_animations = [896, 897]
possible_raw_fish = [327, 335, 331, 359, 377, 371, 383, 363]


def determine_fish(lvl):
    if lvl < 15:
        return 327 # raw sardine, get 200
    elif lvl < 25:
        return 335 # trout 200
    elif lvl < 40:
        return 331 # salmon 700
    elif lvl < 71:
        return 359 # tuna 10k
    elif lvl < 99:
        return 363
    else:
        return 383


def cook_fish_on_fire(port):
    fire = general_utils.get_game_object('3043,4973,1', '43475', port)
    if fire:
        general_utils.move_and_click(fire['x'], fire['y'], 4, 5)
    general_utils.random_sleep(.9, 1.2)
    keyboard.send('space')
    general_utils.click_off_screen(300, 1400, 200, 1000, False)


def bank(port):
    q = {
        'npcsID': ['3194']
    }
    npcs = general_utils.query_game_data(q, port)
    if 'npcs' in npcs:
        for npc in npcs['npcs']:
            print('l',npc)
            if npc['id'] == 3194:
                general_utils.move_and_click(npc['x'], npc['y'], 3, 4)
                general_utils.wait_for_bank_interface(port)
                general_utils.bank_dump_inv(port)
                general_utils.random_sleep(0.9, 1)
                bank_data = general_utils.get_bank_data(port)
                cooking_lvl = general_utils.get_skill_data('cooking', port)
                fish = determine_fish(cooking_lvl['level'])
                fish_loc = general_utils.is_item_in_inventory_v2(bank_data, fish)
                if fish_loc:
                    general_utils.move_and_click(fish_loc['x'], fish_loc['y'], 4, 4)
                    general_utils.random_sleep(0.5, 0.6)
                    keyboard.send('esc')
                    return True
                keyboard.send('esc')
    return False


def cook_handler(port):
    animation_timeout = datetime.datetime.now()
    cooking = False
    while (datetime.datetime.now() - animation_timeout).total_seconds() < 2 and not cooking:
        animation = general_utils.get_player_animation(port)
        if animation in cooking_animations:
            cooking = True
    if cooking:
        return print('Currently cooking.')
    inv = general_utils.get_inv(port)
    more_fish = general_utils.are_items_in_inventory_v2(inv, possible_raw_fish)
    if not more_fish:
        bank(port)
    return cook_fish_on_fire(port)


