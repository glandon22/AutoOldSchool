import datetime

import keyboard
import pyautogui

import queries
from autoscape import general_utils

ores = [
    453,  # coal
    444,  # gold
    447,  # mith
    449,  # addy
    451  # rune
]


def click_towards_sack():
    while True:
        data = general_utils.query_game_data(queries.I3)
        if 'tiles' in data and '375056620' in data['tiles'] and data['tiles']['375056620']['y'] < 1010:
            general_utils.move_and_click(data['tiles']['375056620']['x'], data['tiles']['375056620']['y'], 7, 7)
            break

def click_closest_ore_vein():
    while True:
        data = general_utils.query_game_data(queries.UPPER_ORE_VEINS)
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
            closest = general_utils.find_closest_target(ore_veins)
            general_utils.move_and_click(closest['x'], closest['y'], 6, 6)
            general_utils.click_off_screen(click=False)
            break


def look_north_and_zoom_out():
    general_utils.query_game_data(queries.SET_YAW_NORTH)
    pyautogui.scroll(-4000, 500, 500)
    general_utils.random_sleep(0.5, 0.6)
    keyboard.press('up')
    general_utils.random_sleep(1, 1.2)
    keyboard.release('up')


def should_collect_ore():
    data = general_utils.query_game_data(queries.ORE_COUNT_AND_INVENTORY)
    ore_in_inv = 0
    for item in data['inv']:
        if item['id'] == 12011:
            ore_in_inv += 1
    return ore_in_inv + data['varBit'] > 80


def click_upper_ladder():
    while True:
        data = general_utils.query_game_data(queries.UPPER_LADDER)
        if 'gameObjects' in data and '19045' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['19045']['x'], data['gameObjects']['19045']['y'], 5, 5)
        general_utils.random_sleep(0.1, 0.2)
        data = general_utils.query_game_data(queries.CLICKED_OBJECT)
        if 'targetObj' in data and data['targetObj'] == 19045:
            break
        else:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(1, 1.1)


def click_lower_ladder():
    while True:
        data = general_utils.query_game_data(queries.LOWER_LADDER)
        if 'gameObjects' in data and '19044' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['19044']['x'], data['gameObjects']['19044']['y'] - 15, 5, 5)
        general_utils.random_sleep(0.1, 0.2)
        data = general_utils.query_game_data(queries.CLICKED_OBJECT)
        if 'targetObj' in data and data['targetObj'] == 19044:
            break
        else:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(1, 1.1)


def click_bank_deposit():
    while True:
        data = general_utils.query_game_data(queries.BANK)
        if 'gameObjects' in data and '25937' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['25937']['x'], data['gameObjects']['25937']['y'], 5, 5)
        general_utils.random_sleep(0.1, 0.2)
        data = general_utils.query_game_data(queries.CLICKED_OBJECT)
        if 'targetObj' in data and data['targetObj'] == 25937:
            break
        else:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(1, 1.1)
    general_utils.deposit_box_dump_inv()


def deposit_paydirt():
    while True:
        data = general_utils.query_game_data(queries.ORE_CART)
        if 'gameObjects' in data and '26674' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['26674']['x'], data['gameObjects']['26674']['y'], 4, 4)
        general_utils.random_sleep(0.1, 0.2)
        data = general_utils.query_game_data(queries.CLICKED_OBJECT)
        if 'targetObj' in data and data['targetObj'] == 26674:
            break
        else:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(1, 1.1)
    # wait until everything is deposited
    while True:
        data = general_utils.query_game_data(queries.INVENTORY)
        if 'inv' in data:
            pay_dirt_present = general_utils.is_item_in_inventory(data['inv'], 12011)
            if not pay_dirt_present:
                break


def plunder_sack():
    while True:
        data = general_utils.query_game_data(queries.ORE_SACK)
        if 'groundObjects' in data and '26688' in data['groundObjects']:
            general_utils.move_and_click(data['groundObjects']['26688']['x'], data['groundObjects']['26688']['y'], 3, 3)
        general_utils.random_sleep(0.1, 0.2)
        data = general_utils.query_game_data(queries.CLICKED_OBJECT)
        if 'targetObj' in data and data['targetObj'] == 26688:
            break
        else:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
    while True:
        data = general_utils.query_game_data(queries.INVENTORY)
        if 'inv' in data and len(data['inv']) != 0:
            have_ore = False
            for item in data['inv']:
                if item['id'] in ores:
                    have_ore = True
                    break
            if have_ore:
                break


def bank_and_return():
    click_upper_ladder()
    general_utils.random_sleep(0.6, 0.7)
    general_utils.wait_until_stationary()
    general_utils.random_sleep(2.0, 2.1)
    collect_ore_decision = should_collect_ore()
    deposit_paydirt()
    general_utils.random_sleep(0.5, 0.6)
    if collect_ore_decision:
        click_towards_sack()
        general_utils.wait_until_stationary()
        general_utils.random_sleep(0.5, 0.6)
        while True:
            plunder_sack()
            general_utils.random_sleep(0.7, 0.8)
            click_bank_deposit()
            general_utils.random_sleep(0.9, 1.1)
            data = general_utils.query_game_data(queries.ORE_COUNT)
            if data['varBit'] == 0:
                break
    click_lower_ladder()
    general_utils.random_sleep(0.5, 0.6)
    general_utils.wait_until_stationary()
    general_utils.random_sleep(0.5, 0.6)


def main():
    # the mining animation will go to false for two ticks even though im mining
    # so i need to make sure im actually not mining
    not_mining_timestamp = -1
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 53, 59, 432, 673, 'pass_71', look_north_and_zoom_out)
        data = general_utils.query_game_data(queries.MINING_STATUS_AND_INV_AND_POSE)
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
                general_utils.random_sleep(0.5, 0.6)


main()
