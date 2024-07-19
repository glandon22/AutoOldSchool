import datetime
import logging
import requests
import os

import osrs.util as util
import osrs.dev as dev

config = dev.load_yaml()
session = requests.Session()
establish_conn = {
    'helloWorld': True
}
print('here', os.environ)
session.get(url=f'http://localhost:{os.environ["SERVER_PORT"]}/osrs', json=establish_conn)


def query_game_data(q, port='56799'):
    while True:
        try:
            r = session.get(url='http://localhost:{}/osrs'.format(port), json=q)
            return r.json()
        except Exception as e:
            print('Got an error trying to query the game server: ', e)
            print('failed query: ', q)


def post_game_status(q, updated_config, port='56798'):
    while True:
        try:
            start = updated_config['timings']['break_start']
            start = type(start) is datetime.datetime and f'{start.hour}:{str(start.minute).zfill(2)}:{str(start.second).zfill(2)}'
            end = updated_config['timings']['break_end']
            end = type(end) is datetime.datetime and f'{end.hour}:{str(end.minute).zfill(2)}:{str(end.second).zfill(2)}'
            logging.info(f'Timing variables. Start: {start}, end: {end}')
            enhanced_q = {
                'status': q,
                'next_break': start,
                'break_end': end
            }
            r = session.post(url='http://localhost:{}/manager'.format(port), json=enhanced_q)
            parsed = r.json()
            logging.info('Parsed response from game server: {}'.format(parsed))
            if parsed and 'terminate' in parsed and parsed['terminate']:
                logging.info('Process killed by game server.')
                exit(99)
            return r.json()
        except Exception as e:
            print('Got an error trying to post to the game server: ', e)
            return


# not sure if this even works anymore
def get_player_info(port=1488):
    import socket
    import re
    import json

    host = 'localhost'
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host, port))
    socket.listen(1)
    conn, addr = socket.accept()
    data = bytearray()
    while True:
        data.extend(conn.recv(1024))
        try:
            decoded = data.decode('utf-8')
            body = re.split(r"\s(?=[{\[])", decoded)[-1]
            parsed = json.loads(body)
            # print(json.dumps(parsed, sort_keys=True, indent=4))
            return parsed
        except ValueError:
            continue
    conn.close()


def get_world_location(port='56799'):
    """

    :param port:
    :return: {'x': 2638, 'y': 2653, 'z': 0}
    """
    q = {
        'playerWorldPoint': True
    }
    while True:
        data = query_game_data(q, port)
        if 'playerWorldPoint' in data:
            return data['playerWorldPoint']


def get_nearby_players():

    q = {
        'players': True
    }
    while True:
        data = query_game_data(q, config['port'])
        if 'players' in data:
            return data['players']


def get_ground_items_in_coords(x_min, x_max, y_min, y_max, z, items, port='56799'):
    tiles = util.generate_game_tiles_in_coords(x_min, x_max, y_min, y_max, z,)
    q = {
        'groundItems': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['groundItems'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'groundItems' in data:
        return data['groundItems']


def get_widget(widget_string, port='56799'):
    q = {
        'widget': widget_string
    }
    data = query_game_data(q, port)
    if 'widget' in data:
        return data['widget']
    else:
        return False


def get_widgets(widgets, port='56799'):
    q = {
        'widgets': widgets
    }
    data = query_game_data(q, port)
    if 'widgets' in data:
        return data['widgets']
    else:
        return False


def get_projectiles():
    """

    :return: Array of ints: [1477]
    """
    q = {
        'projectiles': True
    }

    res = query_game_data(q)
    if 'projectiles' in res:
        return res['projectiles']
    else:
        return False


def get_interacting(port):
    q = {
        'interactingWith': True,
    }
    data = query_game_data(q, port)
    if 'interactingWith' in data:
        return data['interactingWith']
    else:
        return False


def set_yaw(val, port):
    q = {
        'setYaw': str(val)
    }
    query_game_data(q, port)


def is_mining(port='56799'):
    q = {
        'isMining': True,
    }
    data = query_game_data(q, port)
    if 'isMining' in data:
        return data['isMining']
    return False


def have_leveled_up(port='56799'):
    leveled_up_widget = get_widget('233,0', port)
    if leveled_up_widget:
        return True
    return False


def get_varbit_value(varbit):
    q = {
        'varBit': varbit
    }
    vb = query_game_data(q, config['port'])
    if 'varBit' in vb:
        return vb['varBit']
    return False


def get_chat_options(port='56799'):
    q = {
        'chatOptions': True
    }
    chat = query_game_data(q, port)
    if 'chatOptions' in chat:
        return chat['chatOptions']
    return False


def get_npcs_by_id(npc_id, port='56799'):
    q = {
        'npcsID': [x.strip() for x in npc_id.split(',')]
    }
    npcs = query_game_data(q, port)
    if 'npcs' in npcs:
        return npcs['npcs']
    return False


def get_npc_by_id(npc_id, port='56799'):
    q = {
        'npcsID': [npc_id]
    }
    npcs = query_game_data(q, port)
    if 'npcs' in npcs:
        for npc in npcs['npcs']:
            if str(npc['id']) == npc_id:
                return npc
    return False


def get_target_npc(port='56799'):
    q = {
        'getTargetNPC': True
    }
    data = query_game_data(q, port)
    print(data)
    if 'targetNPC' in data:
        return data['targetNPC']
    else:
        return


def get_target_obj(port='56799'):
    q = {
        'getTargetObj': True
    }
    data = query_game_data(q, port)
    if 'targetObj' in data:
        return data['targetObj']
    else:
        return -1


def get_player_animation(port='56799'):
    q = {
        'playerAnimation': True
    }
    data = query_game_data(q, port)
    if 'playerAnimation' in data:
        return data['playerAnimation']
    else:
        return -1


def get_multiple_surrounding_game_objects(dist, items, port='56799'):
    tiles = util.generate_surrounding_tiles(dist, port)
    q = {
        'multipleGameObjects': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['multipleGameObjects'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'multipleGameObjects' in data:
        return data['multipleGameObjects']


def get_surrounding_wall_objects(dist, items, port='56799'):
    tiles = util.generate_surrounding_tiles(dist, port)
    q = {
        'wallObjects': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['wallObjects'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'wallObjects' in data:
        return data['wallObjects']


def get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, items, port='56799'):
    """
    :param x_min:
    :param x_max:
    :param y_min:
    :param y_max:
    :param z:
    :param port: default is 56799
    :return: {'9345': {'x': 881, 'y': 538, 'dist': 1}}
    """
    tiles = util.generate_game_tiles_in_coords(x_min, x_max, y_min, y_max, z)
    q = {
        'multipleGameObjects': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['multipleGameObjects'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'multipleGameObjects' in data:
        return data['multipleGameObjects']


def get_surrounding_game_objects(dist, items, port='56799'):
    """

    :param dist: integer, how many tiles around to look for items, ie 7x7
    :param items: array of strings of item codes to search for
    :param port: default is 56799
    :return: {'9345': {'x': 881, 'y': 538, 'dist': 1}}
    """
    tiles = util.generate_surrounding_tiles(dist, port)
    q = {
        'gameObjects': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['gameObjects'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'gameObjects' in data:
        return data['gameObjects']


def get_ground_items(tile, item, port='56799'):
    """

    :param tile: '3407,3091,0'
    :param item: 954
    :param port:
    :return: {'954': [{'x': 816, 'y': 533, 'dist': 0, 'id': 954}]}
    """
    q = {
        'groundItems': [{
            'tile': tile,
            'object': str(item)
        }]
    }
    data = query_game_data(q, port)
    if 'groundItems' in data:
        return data['groundItems']


def get_surrounding_ground_items_any_ids(dist, port='56799'):
    tiles = util.generate_surrounding_tiles(dist)
    q = {
        'allGroundItems': []
    }
    for tile in tiles:
        q['allGroundItems'].append({
            'tile': tile,
            'object': '20997'
        })
    data = query_game_data(q, port)
    if 'allGroundItems' in data:
        return data['allGroundItems']


def get_surrounding_ground_items(dist, items, port='56799'):
    tiles = util.generate_surrounding_tiles(dist)
    q = {
        'groundItems': []
    }
    for tile in tiles:
        item_to_find = '20997'
        if len(items) > 0:
            item_to_find = items[len(items) - 1]
            items.pop()
        q['groundItems'].append({
            'tile': tile,
            'object': str(item_to_find)
        })
    data = query_game_data(q, port)
    if 'groundItems' in data:
        return data['groundItems']


def get_skill_data(skill, port='56799'):
    """

    :param skill: 'hitpoints' or ['prayer', 'strength']
    :return:
    {'level': 98, 'xp': 12164703, 'boostedLevel': 98}
    """
    q = {}
    if type(skill) is list:
        q['skills'] = skill
    else:
        q['skills'] = [skill]
    while True:
        skill_data = query_game_data(q, port)
        if 'skills' in skill_data and type(skill) is not list and skill in skill_data['skills']:
            return skill_data['skills'][skill]
        else:
            return skill_data['skills']


def get_game_objects(lookup, port='56799'):
    q = {
        'gameObjects': lookup
    }
    data = query_game_data(q, port)
    if 'gameObjects' in data:
        return data['gameObjects']
    else:
        return False


def get_game_object(tile, obj, port='56799'):
    """

    :param tile: string
    :param obj: string
    :param port: string
    :return: {'x': 1088, 'y': 572, 'dist': 1, 'x_coord': 2197, 'y_coord': 2792}
    """
    q = {
        'gameObjects': [
            {
                'tile': tile,
                'object': obj
            }
        ]
    }
    data = query_game_data(q, port)
    if 'gameObjects' in data and obj in data['gameObjects']:
        return data['gameObjects'][obj]
    else:
        return False


def get_ground_object(tile, obj, port='56799'):
    q = {
        'groundObjects': [
            {
                'tile': tile,
                'object': obj
            }
        ]
    }
    data = query_game_data(q, port)
    if 'groundObjects' in data and obj in data['groundObjects']:
        return data['groundObjects'][obj]
    else:
        return False


def get_wall_object(tile, obj, port='56799'):
    q = {
        'wallObjects': [
            {
                'tile': tile,
                'object': obj
            }
        ]
    }
    data = query_game_data(q, port)
    if 'wallObjects' in data and obj in data['wallObjects']:
        return data['wallObjects'][obj][0]
    else:
        return False
