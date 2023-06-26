import math

import pyautogui

import osrs.server as server


def find_closest_npc(npcs, ignore=-1):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for npc in npcs:
        if npc['id'] != ignore and npc["dist"] < closest["dist"]:
            closest = npc
    return closest


def select_chat_option(chat_options, phrase):
    if not chat_options:
        return -1
    for i, option in enumerate(chat_options):
        if phrase in option:
            return i
    return -1


def generate_game_tiles_in_coords(x_min, x_max, y_min, y_max, z, port='56799'):
    tiles = []
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            tiles.append('{},{},{}'.format(x, y, z))
    return tiles


def generate_surrounding_tiles(dist, port='56799'):
    player_loc = server.get_world_location(port)
    tiles = []
    for x in range(player_loc['x'] - dist, player_loc['x'] + dist):
        for y in range(player_loc['y'] - dist, player_loc['y'] + dist):
            tiles.append('{},{},{}'.format(x, y, player_loc['z']))
    return tiles


def find_closest_target(targs):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for targ in targs:
        if int(targ["dist"]) < int(closest["dist"]):
            closest = targ
    return closest


def find_an_npc(npcs, min_dist):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for npc in npcs:
        if closest["dist"] > npc["dist"] >= min_dist:
            closest = {
                "dist": npc["dist"],
                "x": math.floor(npc["x"]),
                "y": math.floor(npc["y"]),
                "id": npc["id"]
            }
    if closest['x'] is None:
        return False
    else:
        return closest


'''
|@@@@@@@@@@@@@@|
|@@DEPRECATED@@|
V@@@@@@@@@@@@@@V
'''


def rough_img_compare(img, confidence, region):
    while True:
        try:
            loc = pyautogui.locateOnScreen(img, confidence=confidence, region=region)
            if loc:
                return loc
            else:
                return False
        except Exception as e:
            print('error calling screenshot, retrying.', e)
