import datetime

import osrs.inv as inv_util
import osrs.clock as clock
import osrs.move as move
import osrs.queryHelper
import osrs.server as server
import osrs.util as util
import osrs.keeb as keeb
from osrs.item_ids import ItemIDs
import osrs.queryHelper as queryHelper
from osrs.widget_ids import WidgetIDs
from collections import Counter

withdraw_item_widget = '12,22'
withdraw_noted_widget = '12,24'

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


def withdraw_configured_items(item, game_state: osrs.queryHelper.QueryHelper):
    banked_item = game_state.get_bank(item['id'])
    if not banked_item:
        print(f'{ItemIDs(item).name} not found')
        return False
    if item['quantity'] not in ['All', 'X', 'x'] and banked_item['quantity'] < int(item['quantity']):
        print(f'not enough {ItemIDs(item).name} to satisfy request')
        return False
    if 'noted' in item and item['noted']:
        osrs.move.fast_click(game_state.get_widgets(withdraw_noted_widget))
    osrs.move.right_click_v3(banked_item, f'Withdraw-{item["quantity"]}')
    if 'noted' in item and item['noted']:
        osrs.move.fast_click(game_state.get_widgets(withdraw_item_widget))

    if item['quantity'] == 'X':
        osrs.clock.sleep_one_tick()
        osrs.keeb.write(str(item['amount']))
        osrs.keeb.press_key('enter')
    return True


def withdraw_items(item, quantities, game_state: osrs.queryHelper.QueryHelper):
    banked_item = game_state.get_bank(item)
    if not banked_item:
        print(f'{ItemIDs(item).name} not found')
        return False
    if banked_item['quantity'] < quantities['item']:
        print(f'not enough {ItemIDs(item).name} to satisfy request')
        return False

    osrs.move.click(game_state.get_bank(item))
    return True


def withdraw(searches, game_state: osrs.queryHelper.QueryHelper):
    for search in searches:
        filtered_items = [item for item in search['items'] if type(item) is not dict]
        # if there are no dicts in this list it will return a nested list
        # if that happens i have to flatten it
        if len(filtered_items) > 0 and type(filtered_items[0]) is list:
            filtered_items = sum(filtered_items, [])
        print('u', filtered_items)
        quantities = Counter(filtered_items)
        for item in search['items']:
            if type(item) is dict:
                success = withdraw_configured_items(item, game_state)
                if not success:
                    return False
            else:
                success = withdraw_items(item, quantities, game_state)
                if not success:
                    return False
    return True


def search_and_withdraw(searches, game_state: osrs.queryHelper.QueryHelper):
    for search in searches:
        osrs.move.click(game_state.get_widgets_v2(WidgetIDs.BANK_SEARCH_BUTTON_BACKGROUND.value))
        osrs.keeb.write(search['query'])
        osrs.keeb.press_key('enter')
        osrs.clock.sleep_one_tick()
        game_state.query_backend()
        filtered_items = [item for item in search['items'] if type(item) is not dict]
        print('o', filtered_items)
        # if there are no dicts in this list it will return a nested list
        # if that happens i have to flatten it
        if len(filtered_items) > 0 and type(filtered_items[0]) is list:
            filtered_items = sum(filtered_items, [])
        print('u', filtered_items)
        quantities = Counter(filtered_items)
        for item in search['items']:
            print(item, type(search['items']), search['items'])
            if type(item) is dict:
                success = withdraw_configured_items(item, game_state)
                if not success:
                    return False
                if 'quantity' in item and item['quantity'] == 'X':
                    osrs.move.click(game_state.get_widgets_v2(WidgetIDs.BANK_SEARCH_BUTTON_BACKGROUND.value))
                    osrs.clock.random_sleep(0.1, 0.2)
                    osrs.keeb.write(search['query'])
                    osrs.keeb.press_key('enter')
            else:
                success = withdraw_items(item, quantities, game_state)
                if not success:
                    return False
    return True


def banking_handler(params):
    """
    Supports banking in GE, Varrock, Fally, C Wars, Crafting Guild, Camelot

    :param params: {
        dump_inv: True | False
        dump_equipment: True | False
        deposit: [itemID, itemID...]
        withdraw: [itemID, itemID...]: Repeat item IDs to withdraw multiple
        search: [{ query: 'metal_dragons', items:[itemID, itemID....] }]
    }
    """
    ge_banker_npc_ids = [
        1613, 1633, 1634, 3089
    ]
    varr_banker_npc_ids = [
        2897, 2898
    ]
    fally_banker_npc_ids = [
        1618, 1613, 3094
    ]
    crafting_guild_bank_tile = '2936,3280,0'
    crafting_guild_bank_id = 14886
    lum_top_floor_bank_tile = '3208,3221,2'
    lum_top_floor_bank_id = 18491
    draynor_bank_tile = '3091,3245,0'
    draynor_bank_id = 10355
    c_wars_bank_tile = '2444,3083,0'
    c_wars_bank_id = 4483
    v_west_bank_tile_1 = '3186,3436,0'
    v_west_bank_id_1 = '34810'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([*ge_banker_npc_ids, *varr_banker_npc_ids, *fally_banker_npc_ids])
    qh.set_objects(
        {crafting_guild_bank_tile, c_wars_bank_tile, v_west_bank_tile_1, lum_top_floor_bank_tile, draynor_bank_tile},
        {crafting_guild_bank_id, c_wars_bank_id, v_west_bank_id_1, lum_top_floor_bank_id, draynor_bank_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_player_world_location()
    qh.set_widgets_v2({
        WidgetIDs.BANK_ITEM_CONTAINER.value,
        WidgetIDs.BANK_DEPOSIT_INVENTORY.value,
        WidgetIDs.BANK_DEPOSIT_EQUIPMENT.value,
        WidgetIDs.BANK_SEARCH_BUTTON_BACKGROUND.value
    })
    qh.set_widgets({withdraw_item_widget, withdraw_noted_widget})
    qh.set_bank()
    last_banker_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    banker_search_duration = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - banker_search_duration).total_seconds() > 60:
            return {'error': 'No banker.'}

        qh.query_backend()
        # Exit Condition: successfully opened the banking interface
        if qh.get_widgets_v2(WidgetIDs.BANK_ITEM_CONTAINER.value):
            print('Banking interface is open.')
            break

        # combine the npcs and bank objects into one list
        all_bank_objects = osrs.util.combine_objects(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value))
        if qh.get_npcs():
            all_bank_objects += qh.get_npcs()
        c = osrs.util.find_closest_target(all_bank_objects)
        if c and osrs.move.is_clickable(c) and (datetime.datetime.now() - last_banker_click).total_seconds() > 13:
            osrs.move.fast_click(c)
            osrs.move.fast_click(c)
            last_banker_click = datetime.datetime.now()

    dumped_inv = False
    dumped_equipment = False
    osrs.clock.random_sleep(1, 1.1)
    # Deposit desired items
    wait_time = datetime.datetime.now()
    while True:
        qh.query_backend()
        if (datetime.datetime.now() - wait_time).total_seconds() > 15:
            return banking_handler(params)
        if 'dump_inv' in params and params['dump_inv'] \
                and qh.get_widgets_v2(WidgetIDs.BANK_DEPOSIT_INVENTORY.value) and not dumped_inv:
            osrs.move.click(qh.get_widgets_v2(WidgetIDs.BANK_DEPOSIT_INVENTORY.value))
            dumped_inv = True

        if 'dump_equipment' in params and params['dump_equipment'] \
                and qh.get_widgets_v2(
            WidgetIDs.BANK_DEPOSIT_EQUIPMENT.value
        ) and not dumped_equipment:
            osrs.move.click(qh.get_widgets_v2(WidgetIDs.BANK_DEPOSIT_EQUIPMENT.value))
            dumped_equipment = True

        if ('dump_inv' not in params or not params['dump_inv'] or dumped_inv) \
                and ('dump_equipment' not in params or not params['dump_equipment'] or dumped_equipment):
            break
    # sleep for a second so that all the items i deposited will register and be return on query
    osrs.clock.random_sleep(1, 1.1)
    qh.query_backend()
    # Withdraw desired items
    if 'deposit' in params:
        # TODO!
        print('not implemented')
    if 'withdraw' in params:
        success = withdraw(params['withdraw'], qh)
        if not success:
            print('Failed to withdraw items successfully.')
            return False
    if 'search' in params:
        success = search_and_withdraw(params['search'], qh)
        if not success:
            print('Failed to search and withdraw items successfully.')
            return False
    osrs.keeb.press_key('esc')
    return True
