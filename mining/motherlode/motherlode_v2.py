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

import keyboard
import pyautogui

from osrs_utils import general_utils
import queries

ores = [
    453,  # coal
    444,  # gold
    447,  # mith
    449,  # addy
    451  # rune
]


def click_i1():
    while True:
        data = general_utils.query_game_data(queries.I1)
        if 'tiles' in data and '374856550' in data['tiles'] and data['tiles']['374856550']['y'] < 1010:
            general_utils.move_and_click(data['tiles']['374856550']['x'], data['tiles']['374856550']['y'], 7, 7)
            break


def walk_to_i2_sq():
    while True:
        data = general_utils.query_game_data(queries.I2_TILE)
        # since i am so zoomed out, things at the top of the screen arent fully loaded and may not be clickable
        # so, i wait until the square gets closer to assure that it is loaded
        if 'tiles' in data and '373756520' in data['tiles'] and data['tiles']['373756520']['y'] > 150:
            general_utils.move_and_click(data['tiles']['373756520']['x'], data['tiles']['373756520']['y'], 7, 7)
            break


def navigate_rockfall():
    wait_until_stationary()
    data = general_utils.query_game_data(queries.ROCKFALL_TILE)
    rft = data['tiles']['372756520']
    general_utils.move_and_click(rft['x'], rft['y'], 10, 10)
    # once rockfall is cleared, click on i2 square
    while True:
        data = general_utils.query_game_data(queries.ROCKFALL_TILE_OBJECT_AND_I2_PLAYER_WP)
        # want to basically model this off pass_rockfall_to_mine_veins but click to i2 after passing rock
        # want to check if i am past the rockfall in order to break loop
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] > 3727:
            break
        #not moving
        elif data['poseAnimation'] == 808:
            # if not, try to mine ore veins
            if '26680' not in data['gameObjects']:
                walk_to_i2_sq()
            # if rock is preset, click on the tile to mine it out
            else:
                if '372756520' in data['tiles']:
                    general_utils.move_and_click(data['tiles']['372756520']['x'], data['tiles']['372756520']['y'], 6, 6)
                    general_utils.random_sleep(0.5, 0.6)
        # still walking or running
        else:
            general_utils.random_sleep(0.2, 0.3)
        if '26680' not in data['gameObjects']:
            if '373756520' in data['tiles']:
                general_utils.move_and_click(data['tiles']['373756520']['x'], data['tiles']['373756520']['y'], 6, 6)
                break
            elif am_stationary():
                rft = data['tiles']['372756520']
                general_utils.move_and_click(rft['x'], rft['y'], 10, 10)
                general_utils.random_sleep(0.5, 0.6)
        else:
            data = general_utils.query_game_data(queries.POSE_ANIMATION)
            if 'poseAnimation' in data and data['poseAnimation'] == 808:
                data = general_utils.query_game_data(queries.ROCKFALL_TILE)
                rft = data['tiles']['372756520']
                general_utils.move_and_click(rft['x'], rft['y'], 10, 10)
                general_utils.random_sleep(0.5, 0.6)


def pass_rockfall_to_mine_veins():
    wait_until_stationary()
    data = general_utils.query_game_data(queries.ROCKFALL_TILE)
    rft = data['tiles']['372756520']
    general_utils.move_and_click(rft['x'], rft['y'], 10, 10)
    general_utils.random_sleep(0.5, 0.6)
    while True:
        data = general_utils.query_game_data(queries.ROCKFALL_TILE_AND_OBJECT_AND_ANIMATION_IS_MINING)
        # break once i start mining
        if data['isMining']:
            break
        # if im not moving, check whether or not rock is blocking me
        elif data['poseAnimation'] == 808:
            # if not, try to mine ore veins
            if '26680' not in data['gameObjects']:
                click_closest_ore_vein()
            # if rock is preset, click on the tile to mine it out
            else:
                if '372756520' in data['tiles']:
                    general_utils.move_and_click(data['tiles']['372756520']['x'], data['tiles']['372756520']['y'], 6, 6)
                    general_utils.random_sleep(0.5, 0.6)
        else:
            general_utils.random_sleep(0.2, 0.3)


def click_closest_ore_vein():
    while True:
        data = general_utils.query_game_data(queries.ORE_VEINS)
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


def should_collect_ore():
    data = general_utils.query_game_data(queries.ORE_COUNT_AND_INVENTORY)
    ore_in_inv = 0
    for item in data['inv']:
        if item['id'] == 12011:
            ore_in_inv += 1
    return ore_in_inv + data['varBit'] > 80


def deposit_paydirt():
    # deposit pay dirt
    while True:
        data = general_utils.query_game_data(queries.POSE_ANIMATION)
        # i am not moving
        if 'poseAnimation' in data and data['poseAnimation'] == 808:
            break
        else:
            general_utils.random_sleep(0.1, 0.2)
    while True:
        data = general_utils.query_game_data(queries.ORE_CART)
        if 'gameObjects' in data and '26674' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['26674']['x'], data['gameObjects']['26674']['y'], 4, 4)
            break
    # wait until everything is deposited
    while True:
        data = general_utils.query_game_data(queries.INVENTORY)
        if 'inv' in data:
            pay_dirt_present = general_utils.is_item_in_inventory(data['inv'], 12011)
            if not pay_dirt_present:
                break


def wait_until_stationary():
    while True:
        data = general_utils.query_game_data(queries.POSE_ANIMATION)
        # i am not moving
        if 'poseAnimation' in data and data['poseAnimation'] == 808:
            break
        else:
            general_utils.random_sleep(0.1, 0.2)


def am_stationary():
    data = general_utils.query_game_data(queries.POSE_ANIMATION)
    # i am not moving
    if 'poseAnimation' in data:
        return data['poseAnimation'] == 808


def bank_and_return():
    navigate_rockfall()
    general_utils.random_sleep(0.5, 6)
    click_i1()
    wait_until_stationary()
    general_utils.random_sleep(0.5, 6)
    collect_ore_decision = should_collect_ore()
    deposit_paydirt()
    if collect_ore_decision:
        # collect ore from ore sack until empty
        general_utils.random_sleep(0.7, 0.9)
        while True:
            while True:
                # blew up once here with connection reset, should investigate
                data = general_utils.query_game_data(queries.ORE_SACK)
                if 'groundObjects' in data and '26688' in data['groundObjects']:
                    general_utils.move_and_click(data['groundObjects']['26688']['x'], data['groundObjects']['26688']['y'], 3, 3)
                    break
            while True:
                data = general_utils.query_game_data(queries.INVENTORY)
                if 'inv' in data and len(data['inv']) != 0:
                    have_ore = False
                    for item in data['inv']:
                        if item['id'] in ores:
                            have_ore = True
                            break
                    if have_ore:
                        general_utils.random_sleep(0.9, 1.1)
                        data = general_utils.query_game_data(queries.BANK)
                        if 'gameObjects' in data and '25937' in data['gameObjects']:
                            general_utils.move_and_click(data['gameObjects']['25937']['x'], data['gameObjects']['25937']['y'], 5, 5)
                        break
            general_utils.deposit_box_dump_inv()
            data = general_utils.query_game_data(queries.ORE_COUNT)
            if data['varBit'] == 0:
                break
    click_i1()
    # walk to i2
    general_utils.random_sleep(1.7, 1.9)
    walk_to_i2_sq()
    general_utils.random_sleep(0.5, 0.8)
    wait_until_stationary()
    # pass the rock fall
    pass_rockfall_to_mine_veins()


def look_west_and_zoom_out():
    general_utils.query_game_data(queries.SET_YAW)
    pyautogui.scroll(-4000, 500, 500)
    general_utils.random_sleep(0.5, 0.6)
    keyboard.press('up')
    general_utils.random_sleep(1, 1.2)
    keyboard.release('up')


def main():
    # the mining animation will go to false for two ticks even though im mining
    # so i need to make sure im actually not mining
    not_mining_timestamp = -1
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 53, 59, 432, 673, 'pass_71', look_west_and_zoom_out)
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

