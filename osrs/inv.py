import math
import random
import time
import osrs.keeb
import osrs.server as server
import osrs.move as move

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

def get_inv(port='56799', reject_empty=True):
    while True:
        q = {
            'inv': True
        }
        data = server.query_game_data(q, port)
        if 'inv' in data:
            if len(data['inv']) > 0 or not reject_empty:
                return data['inv']


def get_item_quantity_in_inv(inv, targ):
    quantity = 0
    for item in inv:
        if (type(targ) is list and item['id'] in targ) or (type(targ) in [str, int] and item['id'] == int(targ)):
            quantity += item['quantity']
    return quantity


def are_items_in_inventory_v2(inv, items_to_find):
    if not inv:
        return False
    for item in inv:
        if item['id'] in items_to_find:
            return item
    return False


def are_items_in_inventory(inv, items_to_find):
    if not inv:
        return False
    for item in inv:
        if item['id'] in items_to_find:
            return [item['x'], item['y']]
    return False


def is_item_in_inventory_v2(inv, item_to_find):
    if not inv:
        return False
    for item in inv:
        if item['id'] == int(item_to_find):
            return item
    return False


def is_item_in_inventory(inv, item_to_find):
    if not inv:
        return False
    for item in inv:
        if item['id'] == item_to_find:
            return [item['x'], item['y']]
    return False


def power_drop(inv, slots_to_skip, items_to_drop):
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
        elif num >= len(inv):
            continue
        # dont drop this item type
        elif inv[num]["id"] in items_to_drop:
            move.move_and_click(inv[num]["x"], inv[num]["y"], 5, 5)


def dump_inv_right_click(qh, items_to_drop: list):
    for item in qh.get_inventory():
        if item['id'] in items_to_drop:
            move.right_click_v6(item, 'Drop', qh.get_canvas(), in_inv=True)


def power_drop_v2(qh, items_to_drop):
    pattern = random.randint(0, len(patterns * 2) - 1)
    # reverse the array
    if pattern >= len(patterns):
        pattern = patterns[math.floor(pattern / 2)]
        pattern = pattern[::-1]
    else:
        pattern = patterns[pattern]
    osrs.keeb.keyboard.press(osrs.keeb.key.shift)
    time.sleep(0.15)
    for num in pattern:
        # make sure slot is in range
        if num >= len(qh.get_inventory()):
            continue
        elif qh.get_inventory()[num]["id"] in items_to_drop:
            move.fast_click_v2(qh.get_inventory()[num])
    osrs.keeb.keyboard.release(osrs.keeb.key.shift)


def in_inv_check(item):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(item):
        return True


def not_in_inv_check(item):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(item):
        return True
