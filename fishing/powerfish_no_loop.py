# find a fishing spot
# start fishing
# fish until bag is full
# drop everything
# repeat
import datetime
import time

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
    ]
}

fish_to_drop_ids = {
    'shrimp': [
        317, 321
    ],
    'salmon': [
        335,
        331
    ]
}


def find_spot(fish_to_catch, port):
    q = {
        'npcsID': fish_spot_ids[fish_to_catch]
    }
    data = osrs.server.query_game_data(q, port)
    if 'npcs' in data:
        closest = osrs.util.find_closest_target(data['npcs'])
        osrs.move.move_and_click(closest['x'], closest['y'], 8, 8)
        osrs.clock.random_sleep(0.5, 0.8)
        osrs.move.click_off_screen(click=False)
    else:
        print('did not find any fishing spots.')
        osrs.clock.random_sleep(2, 3)


def catch_fish(fish_num, port):
    """
    :param fish_num:
    '1': 'shrimp',
    '2': 'salmon',
    '3': 'shark',
    '4': 'monkfish',
    '5': 'lobster',
    '6': 'tuna',
    '7': 'barbarian'
    """
    fish_to_catch = fish_to_catch_config[fish_num]
    q = {
        'isFishing': True,
        'inv': True,
        'poseAnimation': True
    }
    data = osrs.server.query_game_data(q, port)
    if data["isFishing"]:
        return print('Currently fishing.')
    elif len(data["inv"]) == 28:
        # salmon + trout = 335, 331
        # shrimp anchovie 317, 321
        # leaping trout 11328
        osrs.inv.power_drop(data["inv"], [], fish_to_drop_ids[fish_to_catch])
        return print('power dropped inv')
    elif not data["isFishing"] and data['poseAnimation'] == 808:
        print('not fishing')
        # wait a second or two so that I dont click the spot right before it disappears
        osrs.clock.random_sleep(1.2, 1.5)
        find_spot(fish_to_catch, port)
        osrs.clock.random_sleep(1.2, 1.5)
