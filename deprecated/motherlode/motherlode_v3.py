'''
query for i1 and i2 squares
q = {
    'tiles': ['3748,5655,0', '3737,5652,0']
}

query for game objects

'''
# deposit box dump all 192,5
# anim id 808 is standing still
# 819 is walking
# 824 is running
import datetime
import random
import time

import pyautogui
from pynput.keyboard import Key, Controller

keyboard = Controller()

import osrs
import queries

ores = [
    453,  # coal
    444,  # gold
    447,  # mith
    449,  # addy
    451,  # rune
    12012, # nugget
]

gems = [
    1623, #sap
    1621, # em
    1619, #ruby
    1617, #dia
]

def navigate_rockfall_v2():
    start_point = osrs.server.get_world_location()
    dest = '3728' if start_point and start_point['x'] < 3727 else '3726'
    while True:
        curr_loc = osrs.server.get_world_location()
        if curr_loc and curr_loc['x'] == 3727 and curr_loc['y'] == 5652:
            osrs.move.spam_click(f'{dest},5652,0', 0.6)
        elif curr_loc and curr_loc['x'] == int(dest):
            break
        else:
            osrs.move.spam_click('3727,5652,0', 0.6)


def click_closest_ore_vein():
    while True:
        data = osrs.server.query_game_data(queries.ORE_VEINS)
        if 'wallObjects' in data and bool(data['wallObjects']):  # oreVeins are present
            ore_veins = []
            if '26661' in data['wallObjects']:
                ore_veins.extend(data['wallObjects']['26661'])
            if '26662' in data['wallObjects']:
                ore_veins.extend(data['wallObjects']['26662'])
            if '26663' in data['wallObjects']:
                ore_veins.extend(data['wallObjects']['26663'])
            if '26664' in data['wallObjects']:
                ore_veins.extend(data['wallObjects']['26664'])
            closest = osrs.util.find_closest_target(ore_veins)
            osrs.move.move_and_click(closest['x'], closest['y'], 6, 6)
            osrs.move.click_off_screen(click=False)
            break


def should_collect_ore():
    data = osrs.server.query_game_data(queries.ORE_COUNT_AND_INVENTORY)
    ore_in_inv = 0
    for item in data['inv']:
        if item['id'] == 12011:
            ore_in_inv += 1
    return ore_in_inv + data['varBit'] > 80


#need to make this retry TODO
def deposit_paydirt():
    # deposit pay dirt
    while True:
        data = osrs.server.query_game_data(queries.POSE_ANIMATION)
        # i am not moving
        if 'poseAnimation' in data and data['poseAnimation'] == 808:
            break
        else:
            osrs.clock.random_sleep(0.1, 0.2)
    osrs.clock.random_sleep(0.6, 0.7)
    while True:
        data = osrs.server.query_game_data(queries.ORE_CART)
        if 'gameObjects' in data and '26674' in data['gameObjects']:
            osrs.move.move_and_click(data['gameObjects']['26674']['x'], data['gameObjects']['26674']['y'], 4, 4)
            break
    # wait until everything is deposited
    while True:
        data = osrs.server.query_game_data(queries.INVENTORY)
        if 'inv' in data:
            pay_dirt_present = osrs.inv.is_item_in_inventory(data['inv'], 12011)
            if not pay_dirt_present:
                break


def ore_handler():
    clicked_sack = datetime.datetime.now() - datetime.timedelta(hours=1)
    clicked_bank = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        data = osrs.server.query_game_data(queries.ORE_COUNT)
        inv = osrs.inv.get_inv(reject_empty=False)
        bank_data = osrs.bank.get_deposit_box_data()
        if 'varBit' in data and data['varBit'] == 0 and not osrs.inv.are_items_in_inventory_v2(inv, ores + gems):
            return
        elif not osrs.inv.are_items_in_inventory_v2(inv, ores + gems) and (datetime.datetime.now() - clicked_sack).total_seconds() > 10:
            data = osrs.server.query_game_data(queries.ORE_SACK)
            if 'groundObjects' in data and '26688' in data['groundObjects']:
                osrs.move.move_and_click(data['groundObjects']['26688']['x'], data['groundObjects']['26688']['y'], 3, 3)
                clicked_sack = datetime.datetime.now()
                clicked_bank = datetime.datetime.now() - datetime.timedelta(hours=1)
        elif bank_data:
            dumps = {}
            dep = osrs.bank.get_deposit_box_data()
            print('dep', dep)
            if dep:
                for item in dep:
                    if item['id'] != 11920:
                        dumps[item['id']] = item
                print('dumps', dumps)
                for key in dumps:
                    osrs.move.click(dumps[key])
                osrs.keeb.keyboard.press(osrs.keeb.key.esc)
                osrs.keeb.keyboard.release(osrs.keeb.key.esc)
        elif osrs.inv.are_items_in_inventory_v2(inv, ores + gems) and (datetime.datetime.now() - clicked_bank).total_seconds() > 10:
            data = osrs.server.query_game_data(queries.BANK)
            if 'gameObjects' in data and '25937' in data['gameObjects']:
                osrs.move.move_and_click(data['gameObjects']['25937']['x'], data['gameObjects']['25937']['y'], 5, 5)
                clicked_sack = datetime.datetime.now() - datetime.timedelta(hours=1)
                clicked_bank = datetime.datetime.now()


def bank_and_return():
    navigate_rockfall_v2()
    collect_ore_decision = should_collect_ore()
    osrs.move.run_towards_square_v2({'x': 3748, 'y': 5672, 'z': 0})
    deposit_paydirt()
    if collect_ore_decision:
        osrs.move.run_towards_square_v2({'x': 3748, 'y': 5659, 'z': 0})
        ore_handler()
    osrs.move.run_towards_square_v2({'x': 3727, 'y': 5652, 'z': 0})
    # pass the rock fall
    navigate_rockfall_v2()

def main():
    # the mining animation will go to false for two ticks even though im mining
    # so i need to make sure im actually not mining
    not_mining_timestamp = -1
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 53, 59, 432, 673, 'julenth', False)
        data = osrs.server.query_game_data(queries.MINING_STATUS_AND_INV_AND_POSE)
        if 'inv' in data and len(data['inv']) == 28:
            not_mining_timestamp = -1
            bank_and_return()
        elif data['isMining']:
            not_mining_timestamp = -1
        elif 'poseAnimation' in data and data['poseAnimation'] != 808:
            continue
        elif not data['isMining']:
            if not_mining_timestamp == -1:
                not_mining_timestamp = datetime.datetime.now()
            elif (datetime.datetime.now() - not_mining_timestamp).total_seconds() > 3:
                click_closest_ore_vein()
                not_mining_timestamp = -1
                osrs.clock.random_sleep(0.5, 0.6)

main()
