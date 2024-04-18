import osrs.inv as inv_util
import osrs.clock as clock
import osrs.move as move
import osrs.queryHelper
import osrs.server as server
import osrs.util as util
import osrs.keeb as keeb
import osrs.dev as dev
import osrs.queryHelper as queryHelper
import logging

def deposit_all_of_x(items, port='56799'):
    while True:
        found_additional_items = False
        inv = inv_util.get_inv(port)
        for item in inv:
            if item['id'] in items:
                found_additional_items = True
                move.move_and_click(item['x'], item['y'], 3, 3)
                clock.random_sleep(0.5, 0.6)
                break
        if not found_additional_items:
            break
    clock.random_sleep(0.5, 0.6)


def deposit_all_but_x_in_bank(items, port='56799'):
    while True:
        found_additional_items = False
        inv = inv_util.get_inv(port)
        for item in inv:
            if item['id'] not in items:
                found_additional_items = True
                move.move_and_click(item['x'], item['y'], 3, 3)
                clock.random_sleep(0.5, 0.6)
                break
        if not found_additional_items:
            break
    clock.random_sleep(0.5, 0.6)


def click_banker(port='56799'):
    q = {
        'npcs': ['Banker']
    }
    data = server.query_game_data(q, port)
    if len(data["npcs"]) != 0:
        closest = util.find_closest_npc(data['npcs'])
        move.move_and_click(closest['x'], closest['y'], 5, 6)


def get_bank_data(port='56799'):
    q = {
        'bank': True
    }
    while True:
        data = server.query_game_data(q, port)
        if 'bankItems' in data:
            return data['bankItems']


def get_deposit_box_data(port='56799'):
    q = {
        'depositBox': True
    }
    while True:
        data = server.query_game_data(q, port)
        if 'depositBox' in data:
            return data['depositBox']


def find_item_in_bank(item_to_find, port='56799'):
    q = {
        'bank': True
    }
    while True:
        data = server.query_game_data(q, port)
        if 'bankItems' in data:
            for item in data['bankItems']:
                if item['id'] == item_to_find:
                    return item
            return False


def bank_dump_inv(port='56799'):
    q = {
        'dumpInvButton': True
    }
    while True:
        data = server.query_game_data(q, port)
        if 'dumpInvButton' in data:
            move.move_and_click(data['dumpInvButton']['x'], data['dumpInvButton']['y'], 3, 4)
            break


def wait_for_bank_interface(port='56799'):
    q = {
        'dumpInvButton': True
    }
    while True:
        data = server.query_game_data(q, port)
        if 'dumpInvButton' in data:
            clock.random_sleep(0.9, 0.8)
            return


def deposit_box_dump_inv():
    q = {
        'widget': '192,5'
    }
    # wait to first see the button,
    # since there is a lag from its first appearance
    # to actually being on screen in the correct location
    while True:
        data = server.query_game_data(q)
        if 'widget' in data:
            break
    clock.random_sleep(0.5, 0.61)
    while True:
        data = server.query_game_data(q)
        if 'widget' in data:
            move.move_and_click(data['widget']['x'], data['widget']['y'], 6, 6)
            break
    keeb.keyboard.press(keeb.Key.esc)
    keeb.keyboard.release(keeb.Key.esc)


def dump_items():
    qh = queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({'12,42'})
    qh.query_backend()
    if qh.get_inventory() and len(qh.get_inventory()) != 0:
        dump_inv = qh.get_widgets('12,42')
        if dump_inv:
            move.click(dump_inv)
