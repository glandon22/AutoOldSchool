### lighting brazier animation id is 733
# entrance door 29322 -- 1630, 3965,0
# unlit brazier 29312 -- 1621, 3998, 0
# bruma root 29311 - 1621, 3988, 0
# safe cutting tile 1622, 3988,0
# snow from sky 26990 object code
# lit brazier 29314
# 29313 broken brazier
# bank chest 29321 -- 1641, 3944, 0
# tile to click after banking - 1631-2, 3956-7
# tile to click inside 1623-7, 3993-1
# snow is 29324 that falls in x pattern
# snow that explodes brazier is 26690
# intermediate swquare to elave game 1628-1630, 3976-9
# when snow spawns or something i can save it to obj w timestamp and check the timestamp instead of having to add and remove shit
# wine 1993
# jug 1935
# hammer 2347 tinderbox 590
# bank
# click intermediate tile
# click dinhs door
# click intermediate tile in game
# go to brazier
# wait until game starts
# click to light
# wait til fm xp go up
# run to safe bruma cutting area
# wait until on safe tile
# begin cutting
# while cutting, monitor health. eat if necessary
# go to brazier on full bag
# start feeding
# feed until empty, checking to see if i stopped or brazier broke/ went out
# go back to safe spot, and begin cutting
# cut bag and monitor the energy percent
# click intermediate tile
# click dinhs door
# click bank chest

"""
Script must be started with a Hammer and Tinder box in inventory
"""

from osrs_utils import general_utils
import datetime
import random
import time
import keyboard

status = 'init'


def bank():
    global status
    data = general_utils.get_player_info(4200)
    if not data['tiles']['bank']:
        print('did not find bank tile on init.')
    bank_chest = data['tiles']['bank']
    print('Walking to bank chest.')
    general_utils.move_and_click(bank_chest["x"], bank_chest["y"], 5, 6)
    general_utils.click_off_screen(click=False)
    # wait for bank interface to appear
    print('waiting for bank interface.')
    while True:
        loc = general_utils.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
        if loc:
            break
    print('bank interface opened, dumping jugs and loot crates.')
    wine_count = 0
    for item in data['inv']:
        if item['id'] == 1993:
            wine_count += 1
        elif item['id'] in [2347, 590]:
            continue
        else:
            general_utils.move_and_click(item["x"], item["y"], 5, 6)
    # dump everything but hammer, tinderbox, and jugs of wine
    # keep track of jugs of wine in inventory, want to have five total after banking
    data = general_utils.get_player_info(4200)
    print('withdrawing wines.')
    for item in data['bankStuff']:
        if item['id'] == 1993:
            for x in range(5 - wine_count):
                general_utils.move_and_click(item["x"], item["y"], 5, 6)
    keyboard.send('esc')
    print('finished banking.')


def walk_to_game():
    global status
    saved_coords = {
        'x': 0,
        'y': 0
    }
    '''
    @@TODO: this needs to be refactored to use the square "i1"
    '''
    general_utils.move_and_click(200, 930, 100, 50)
    general_utils.click_off_screen(click=False)
    while True:
        data = general_utils.get_player_info(4200)
        print('saved_coords', saved_coords)
        if 'dinhs' in data['tiles'] and 'gameObjects' in data['tiles']['dinhs'] and '29322' in data['tiles']['dinhs']['gameObjects']:
            print('have dinhs game object', data['tiles']['dinhs'])
            dinhs_door = data['tiles']['dinhs']['gameObjects']['29322']
            if 'x' in dinhs_door and 'y' in dinhs_door:
                print('game object has x and y values')
                if dinhs_door['x'] == saved_coords['x'] and dinhs_door['y'] == saved_coords['y']:
                    print('values match up')
                    break
                else:
                    print(' value mismatch')
                    print(saved_coords)
                    print(dinhs_door['x'],dinhs_door['y'])
                    saved_coords = {
                        'x': dinhs_door['x'],
                        'y': dinhs_door['y']
                    }
    general_utils.move_and_click(saved_coords["x"], saved_coords["y"], 5, 6)
    general_utils.random_sleep(2.5, 3)


def go_to_arena_sq():
    print('i2')
    while True:
        data = general_utils.get_player_info(4200)
        print(data)
        if 'i2' in data['tiles']:
            print('breaking')
            intermediate_sq = data['tiles']['i2']
            general_utils.move_and_click(intermediate_sq['x'], intermediate_sq['y'], 25, 25)
            general_utils.random_sleep(0.5, 0.6)
            break


def go_to_cutting_square():
    saved_coords = {
        'x': 0,
        'y': 0
    }
    while True:
        data = general_utils.get_player_info(4200)
        if 'safe' in data['tiles']:
            safe_square = data['tiles']['safe']
            if 'x' in safe_square and 'y' in safe_square:
                if safe_square['x'] == saved_coords['x'] and safe_square['y'] == saved_coords['y']:
                    print('values match up')
                    break
                else:
                    print(' value mismatch')
                    print(saved_coords)
                    print(safe_square['x'],safe_square['y'])
                    saved_coords = {
                        'x': safe_square['x'],
                        'y': safe_square['y']
                    }
    general_utils.move_and_click(saved_coords["x"], saved_coords["y"], 5, 6)
    saved_coords = {
        'x': 0,
        'y': 0
    }
    while True:
        data = general_utils.get_player_info(4200)
        if 'bruma' in data['tiles'] and 'gameObjects' in data['tiles']['bruma'] and '29311' in data['tiles']['bruma'][
            'gameObjects']:
            bruma_roots = data['tiles']['bruma']['gameObjects']['29311']
            if 'x' in bruma_roots and 'y' in bruma_roots:
                if bruma_roots['x'] == saved_coords['x'] and bruma_roots['y'] == saved_coords['y']:
                    print('values match up')
                    break
                else:
                    print(' value mismatch')
                    print(saved_coords)
                    print(bruma_roots['x'], bruma_roots['y'])
                    saved_coords = {
                        'x': bruma_roots['x'],
                        'y': bruma_roots['y']
                    }
    general_utils.move_and_click(saved_coords["x"], saved_coords["y"], 5, 6)


def determine_game_state():
    global status
    data = general_utils.get_player_info(4200)
    # timer is zero,
    if 'wtTimer' in data and data['wtTimer'] == 0:
        print('here')
        if 'wtHealth' in data:
            parsed_health = data['wtHealth'].split(' ')[2]
            health_len = len(parsed_health)
            print('xx', parsed_health, health_len)
            parsed_health = parsed_health[:health_len-1]
            if int(parsed_health) >= 90:
                return 'cut'
            # wait until next game starts
            else:
                return 'wait'


def wait_for_game():
    global status
    while True:
        data = general_utils.get_player_info(4200)
        if 'wtTimer' in data and data['wtTimer'] != 0:
            break
        general_utils.click_off_screen(click=False)


def start_new_game():
    global status
    data = general_utils.get_player_info(4200)
    intermed_sq = data['tiles']['i2']
    general_utils.move_and_click(intermed_sq['x'], intermed_sq['y'], 10, 10)
    saved_coords = {
        'x': 0,
        'y': 0
    }
    while True:
        data = general_utils.get_player_info(4200)
        if 'brazier' in data['tiles'] and 'gameObjects' in data['tiles']['brazier'] and '29312' in \
                data['tiles']['brazier']['gameObjects']:
            brazier = data['tiles']['brazier']['gameObjects']['29312']
            if 'x' in brazier and 'y' in brazier:
                if brazier['x'] == saved_coords['x'] and brazier['y'] == saved_coords['y']:
                    print('values match up')
                    break
                else:
                    saved_coords = {
                        'x': brazier['x'],
                        'y': brazier['y']
                    }
    # click and run to brazier
    general_utils.move_and_click(saved_coords["x"], saved_coords["y"], 5, 6)
    while True:
        data = general_utils.get_player_info(4200)
        if 'wtTimer' in data and data['wtTimer'] < 5:
            prev_fmxp = data['fmXp']
            while True:
                data = general_utils.get_player_info(4200)
                #successfully lit brazier
                if data['fmXp'] != prev_fmxp:
                    break
                elif '29314' in data['tiles']['brazier']['gameObjects']:
                    print('failed to light the brazier on game start. going to chop roots.')
                #click the brazier
                else:
                    brazier = data['tiles']['brazier']['gameObjects']['29312']
                    general_utils.move_and_click(brazier["x"], brazier["y"], 5, 6)
            break


def main():
    global status
    start_time = datetime.datetime.now()
    while True:
        if status == 'init':
            bank()
            status = 'walking to game'
        elif status == 'walking to game':
            walk_to_game()
            status = 'entered lobby'
        elif status == 'entered lobby':
            game_state = determine_game_state()
            if game_state == 'wait':
                status = 'waiting for game'
            elif game_state == 'cut':
                go_to_arena_sq()
                go_to_cutting_square()
                status = 'cutting'
        elif status == 'waiting for game':
            wait_for_game()
            print('done waiting')
            status = 'ready to start game'
        elif status == 'ready to start game':
            print('starting new game')
            start_new_game()
            print('started game')
            status = 'begin cutting'
        elif status == 'begin cutting':
            print('cutting')
            go_to_cutting_square()
            status = 'cutting'

main()