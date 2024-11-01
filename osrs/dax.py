import datetime
from functools import cache

import requests

import osrs.dev
import osrs.dev as dev

config = dev.load_yaml()
session = requests.Session()

# Store previous calls
CACHE = {}


def generate_path(start, end):
    """

    :param start: {'x': 3489, 'y': 3391, 'z': 0} :param end: {"x": 3502, 'y': 3391, 'z': 0} :return: [] ||
    List<tiles> : [{'x': 3489, 'y': 3391, 'z': 0}, {'x': 3490, 'y': 3391, 'z': 0}, {'x': 3491, 'y': 3391, 'z': 0}]
    """

    if type(start) is not dict:
        raise Exception('start must be a dict, {} is not a valid value.'.format(start))
    if type(end) is not dict:
        raise Exception('end must be a dict, {} is not a valid value.'.format(end))
    cache_lookup = f"{start['x']},{start['y']},{start['z']}-{end['x']},{end['y']},{end['z']}"
    if cache_lookup in CACHE:
        osrs.dev.logger.info("Found a dax path in cache - returning store value.")
        return CACHE[cache_lookup]

    q = {
        "start": start,
        "end": end,
        "player": {"members": True}
    }
    try:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'key': config['dax']['key'],
            'secret': config['dax']['secret']
        }
        start = datetime.datetime.now()
        r = session.post(url='https://walker.dax.cloud/walker/generatePath', json=q, headers=headers)
        print('latency: ', (datetime.datetime.now() - start).total_seconds())
        data = r.json()
        if 'pathStatus' in data and data['pathStatus'] == 'SUCCESS':
            CACHE[cache_lookup] = data['path']
            return data['path']
        else:
            return []
    except Exception as e:
        print('Got an error trying to query dax: ', e)
        print('failed query: ', q)
        return []
