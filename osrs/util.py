from collections.abc import Callable
import osrs.dev as dev
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


def find_closest_alive_npc(npcs):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for npc in npcs:
        if npc["dist"] < closest["dist"] and npc['health'] != 0:
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


def generate_surrounding_tiles_from_point(dist, player_loc):
    tiles = []
    for x in range(player_loc['x'] - dist, player_loc['x'] + dist):
        for y in range(player_loc['y'] - dist, player_loc['y'] + dist):
            tiles.append('{},{},{}'.format(x, y, player_loc['z']))
    return tiles


def find_closest_target(targs):
    if not targs:
        return False
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for targ in targs:
        if int(targ["dist"]) < int(closest["dist"]):
            closest = targ
    if closest['x'] is None:
        return False
    else:
        return closest


def tile_objects_to_strings(tiles):
    parsed_tiles = []
    for tile in tiles:
        parsed_tiles.append(f'{tile["x"]},{tile["y"]},{tile["z"]}')
    return parsed_tiles


def combine_objects(objects):
    reduced = []
    if not objects:
        return reduced
    for k in objects:
        target = objects[k]
        # allow combining lists or objects
        target = target if type(target) is list else [target]
        reduced = reduced + target
    return reduced


# instead of using game distance to calculate
# the closest target, it uses screen coordinates
# i.e. which target will the mouse travel the shortest distance
def find_closest_target_on_screen(targets: list[dict], additional_filter: Callable = None):
    '''

    :param targets: List<Targets> items in list MUST contain 'x' and 'y' keys which correspond to on-screen coordinates
    :param additional_filter: fn() :: this is optional filter logic to remove unwanted elements
    :return: {'x': 235, 'y': 243} :: object with coords to click on screen
    '''
    mouse_position = pyautogui.position()
    if not targets:
        return None
    if additional_filter is not None:
        targets = list(filter(additional_filter, targets))
    closest = None
    for targ in targets:
        dist_from_mouse = dev.point_dist(mouse_position[0], mouse_position[1], targ['x'], targ['y'])
        if not closest or (dist_from_mouse < closest['dist']):
            closest = {**targ, 'dist': dist_from_mouse}
    return closest


def find_closest_target_in_game(targets: list[dict], player_loc, additional_filter: Callable = None):
    '''

    :param targets: List<Targets> items in list MUST contain 'x' and 'y' keys which correspond to on-screen coordinates
    :param additional_filter: fn() :: this is optional filter logic to remove unwanted elements
    :return: {'x': 235, 'y': 243} :: object with coords to click on screen
    '''
    if not targets or not player_loc:
        return None
    if additional_filter is not None:
        targets = list(filter(additional_filter, targets))
    closest = None
    for targ in targets:
        dist_from_mouse = dev.point_dist(player_loc['x'], player_loc['y'], targ['x_coord'], targ['y_coord'])
        if not closest or (dist_from_mouse < closest['dist']):
            closest = targ
    return closest


def is_point_in_rectangle(x, y, x1, y1, x2, y2):
    return x1 <= x <= x2 and y1 <= y <= y2


def determine_large_monster_area(sw_tile, size: int):
    area = []
    for x in range(sw_tile['x_coord'], sw_tile['x_coord'] + size):
        for y in range(sw_tile['y_coord'], sw_tile['y_coord'] + size):
            area.append({
                'x': x,
                'x_coord': x,
                'y': y,
                'y_coord': y,
            })
    return area


def monster_perimeter_coordinates(size, sw_tile, z=0):
    #coordinates = []
    coordinates = {}
    x_start = sw_tile['x_coord'] - 1
    y_start = sw_tile['y_coord'] - 1
    # Bottom edge (excluding corners)
    for x in range(x_start + 1, x_start + size - 1):
        #coordinates.append({'x': x, 'y': y_start, 'z': z})
        coordinates[f"{x},{y_start},{z}"] = True

    # Right edge (excluding corners)
    for y in range(y_start + 1, y_start + size - 1):
        #coordinates.append({'x': x_start + size - 1, 'y': y, 'z': z})
        coordinates[f"{x_start + size - 1},{y},{z}"] = True

    # Top edge (excluding corners)
    for x in range(x_start + size - 2, x_start, -1):
        #coordinates.append({'x': x, 'y': y_start + size - 1, 'z': z})
        coordinates[f"{x},{y_start + size - 1},{z}"] = True
    # Left edge (excluding corners)
    for y in range(y_start + size - 2, y_start, -1):
        #coordinates.append({'x': x_start, 'y': y, 'z': z})
        coordinates[f"{x_start},{y},{z}"] = True

    return coordinates
