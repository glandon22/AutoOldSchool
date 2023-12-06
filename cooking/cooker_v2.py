import datetime

import osrs
from pynput.keyboard import Key, Controller

keyboard = Controller()


cooking_animations = [896, 897]
possible_raw_fish = [327, 335, 331, 359, 377, 371, 383, 363]


def determine_fish(lvl):
    '''if lvl < 15:
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
        return 383'''
    return 3144


def cook_fish_on_fire(port):
    fire = osrs.server.get_game_object('3043,4973,1', '43475', port)
    if fire:
        osrs.move.move_and_click(fire['x'], fire['y'], 4, 5)
    osrs.clock.random_sleep(.9, 1.2)
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    osrs.move.click_off_screen(300, 1400, 200, 1000, False)


def bank(port):
    q = {
        'npcsID': ['3194']
    }
    npcs = osrs.server.query_game_data(q, port)
    if 'npcs' in npcs:
        for npc in npcs['npcs']:
            if npc['id'] == 3194:
                osrs.move.move_and_click(npc['x'], npc['y'], 3, 4)
                osrs.bank.wait_for_bank_interface(port)
                osrs.bank.bank_dump_inv(port)
                osrs.clock.random_sleep(0.9, 1)
                bank_data = osrs.bank.get_bank_data(port)
                cooking_lvl = osrs.server.get_skill_data('cooking', port)
                fish = determine_fish(cooking_lvl['level'])
                fish_loc = osrs.inv.is_item_in_inventory_v2(bank_data, fish)
                if fish_loc:
                    osrs.move.move_and_click(fish_loc['x'], fish_loc['y'], 4, 4)
                    osrs.clock.random_sleep(0.5, 0.6)
                    keyboard.press(Key.esc)
                    keyboard.release(Key.esc)
                    return True
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
                exit('no more fish to cook')
    return False


def cook_handler(port):
    animation_timeout = datetime.datetime.now()
    cooking = False
    while (datetime.datetime.now() - animation_timeout).total_seconds() < 2 and not cooking:
        animation = osrs.server.get_player_animation(port)
        if animation in cooking_animations:
            cooking = True
    if cooking:
        return print('Currently cooking.')
    inv = osrs.inv.get_inv(port)
    more_fish = osrs.inv.are_items_in_inventory_v2(inv, possible_raw_fish)
    if not more_fish:
        bank(port)
    return cook_fish_on_fire(port)


