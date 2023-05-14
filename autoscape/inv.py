import math
import random

from autoscape import general_utils


def power_drop(curr_inv, slots_to_skip, items_to_drop):
    patterns = [
        [
            0, 1, 2, 3,
            7, 6, 5, 4,
            8, 9, 10, 11,
            15, 14, 13, 12,
            16, 17, 18, 19,
            23, 22, 21, 20,
            24, 25, 26, 27
        ],
        [
            0, 4, 8, 12, 16, 20, 24,
            25, 21, 17, 13, 9, 5, 1,
            2, 6, 10, 14, 18, 22, 26,
            27, 23, 19, 15, 11, 7, 3
        ],
        [
            0, 4, 5, 1,
            2, 3, 7, 6,
            11, 10, 9, 8,
            12, 16, 20, 24,
            25, 21, 17, 13,
            14, 15, 19, 18,
            22, 23, 27, 26
        ],
        [
            3, 7, 11, 15,
            19, 23, 27, 26,
            25, 24, 20, 21,
            22, 18, 17, 16,
            12, 13, 14, 10,
            6, 2, 1, 5,
            9, 8, 4, 0
        ]
    ]
    pattern = random.randint(0, len(patterns * 2) - 1)
    # reverse the array
    if pattern >= len(patterns):
        pattern = patterns[math.floor(pattern / 2)]
        pattern = pattern[::-1]
        print('here', pattern)
    else:
        pattern = patterns[pattern]
    for num in pattern:
        # dont drop whatever is in this slot
        if len(slots_to_skip) != 0 and num in slots_to_skip:
            continue
        # make sure slot is in range
        elif num >= len(curr_inv):
            continue
        # dont drop this item type
        elif curr_inv[num]["id"] in items_to_drop:
            general_utils.move_and_click(curr_inv[num]["x"], curr_inv[num]["y"], 5, 5)


# check if one particular item is in curr_inventory
def is_item_in_inventory(curr_inv, item_to_find):
    if not curr_inv:
        return False
    for item in curr_inv:
        if item['id'] == item_to_find:
            return [item['x'], item['y']]
    return False


# check if one particular item is in curr_inventory
def is_item_in_inventory_v2(curr_inv, item_to_find):
    if not curr_inv:
        return False
    for item in curr_inv:
        if item['id'] == int(item_to_find):
            return item
    return False


# check for presence of one of multiple items
# this is useful for supporting multiple food types in combat
# if you don't care which food is consumed
def are_items_in_inventory(curr_inv, items_to_find):
    if not curr_inv:
        return False
    for item in curr_inv:
        if item['id'] in items_to_find:
            return [item['x'], item['y']]
    return False


def are_items_in_inventory_v2(curr_inv, items_to_find):
    if not curr_inv:
        return False
    for item in curr_inv:
        if item['id'] in items_to_find:
            return item
    return False


#  this call occasionally fails on the backend, so if we know there should be something in inventory,
#  retry until its returned
def get_inv(port='56799', reject_empty=True):
    while True:
        q = {
            'inv': True
        }
        data = general_utils.query_game_data(q, port)
        if 'inv' in data:
            if len(data['inv']) > 0 or not reject_empty:
                return data['inv']