# find a fishing spot
# start fishing
# fish until bag is full
# drop everything
# repeat
import datetime
import time

import pyautogui

import osrs
import math

fish_to_catch_config = {
    '1': 'shrimp',
    '2': 'salmon',
    '3': 'shark',
    '4': 'monkfish',
    '5': 'lobster',
    '6': 'tuna',
    '7': 'barbarian'
}

fish_to_catch = fish_to_catch_config['7']

fish_spot_ids = {
    'shrimp': [
        '1514',
        '1517',
        '1518',
        '1521',
        '1523',
        '1524',
        '1525',
        '1528',
        '1530',
        '1544',
        '3913',
        '7155',
        '7459',
        '7462',
        '7467',
        '7469',
        '7947',
        '10513'
    ],
    'salmon': [
        '394',
        '1506',
        '1507',
        '1508',
        '1509',
        '1513',
        '1515',
        '1516',
        '1526',
        '1527',
        '3417',
        '3418',
        '7463',
        '7464',
        '7468',
        '8524'
    ],
    'barbarian': ['1542']
}

fish_to_drop_ids = {
    'shrimp': [
        317, 321
    ],
    'salmon': [
        335,
        331
    ],
    'barbarian': [
            11328,
            11330,
            11332
        ]
}


def find_spot():
    q = {
        'npcsID': fish_spot_ids[fish_to_catch]
    }
    data = osrs.server.query_game_data(q)
    if 'npcs' in data:
        closest = osrs.util.find_closest_target(data['npcs'])
        if not closest:
            print('failed to find spot')
            print(data['npcs'])
            print(closest)
            osrs.move.run_towards_square_v2({'x': 2499, 'y': 3510, 'z': 0})
            return
        osrs.move.move_and_click(closest['x'], closest['y'], 8, 8)
        osrs.clock.random_sleep(0.5, 0.8)
    else:
        print('did not find any fishing spots.')
        osrs.clock.random_sleep(2, 3)


def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 53, 58, 423, 551, 'julenth', False)
        q = {
            'isFishing': True,
            'inv': True,
            'poseAnimation': True
        }
        data = osrs.server.query_game_data(q)
        if data["isFishing"]:
            print('Currently fishing.')
            continue
        elif len(data["inv"]) == 28:
            # salmon + trout = 335, 331
            # shrimp anchovie 317, 321
            # leaping trout 11328
            osrs.inv.power_drop(data["inv"], [], fish_to_drop_ids[fish_to_catch])
        elif not data["isFishing"] and data['poseAnimation'] == 808:
            print('not fishing')
            # wait a second or two so that I dont click the spot right before it disappears
            osrs.clock.random_sleep(1.2, 1.5)
            find_spot()
            osrs.clock.random_sleep(1.2, 1.5)

main()
'''#osrs.server.query_game_data({'canvas': True})
pyautogui.moveTo(0, 23)'''

# 3051 unselected
# 3055 blue, unseelcted
# 3053 selected
'''
individual chat buttons
162,1 full bar

buttons vvv
162,5
162,8
162,12
162,16
162,20
162,24
162,28


161,93 minimap
161,95 inv interface
'''
'''qh = osrs.queryHelper.QueryHelper()
qh.set_widgets({'162,1', '162,5','162,8','162,12','162,16','162,20','162,24','162,28', '161,93', '161,95'})
qh.set_canvas()
qh.query_backend()
print(qh.get_widgets('161,95'))
print(qh.get_canvas())'''