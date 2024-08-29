import datetime
import math

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


logger = osrs.dev.instantiate_logger()


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
    print('g', item)
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

    if 'consume' in item:
        qh1 = osrs.queryHelper.QueryHelper()
        qh1.set_inventory()
        qh1.set_canvas()
        for i in range(27):
            qh1.set_widgets({f"15,3,{i}"})
        search_id = item['consume_id_override'] if 'consume_id_override' in item else item['id']
        while True:
            qh1.query_backend()
            for i in range(27):
                if qh1.get_widgets(f"15,3,{i}") and qh1.get_widgets(f"15,3,{i}")['itemID'] == search_id:
                    res = osrs.move.right_click_v6(
                        qh1.get_widgets(f"15,3,{i}"),
                        item['consume'],
                        qh1.get_canvas(),
                        in_inv=True
                    )
                    if res:
                        return True

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
        game_state.query_backend()
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


def withdraw_v2(items, game_state: osrs.queryHelper.QueryHelper):
    for item in items:
        if type(item) is dict:
            success = withdraw_configured_items(item, game_state)
            if not success:
                return False
        else:
            banked_item = game_state.get_bank(item)
            if not banked_item:
                print(f'{ItemIDs(item).name} not found')
                return False
            else:
                osrs.move.fast_click(banked_item)

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


def deposit_items(items: list):
    input_widget = '162,42'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({input_widget})
    qh.set_canvas()
    if type(items) is not list:
        logger.error('non list passed to banking deposit function')
        return False
    for item in items:
        if 'id' not in item:
            logger.warn('deposit item missing id')
            continue
        qh.query_backend()
        inventory = list(filter(lambda inv_item: inv_item['id'] == item['id'], qh.get_inventory()))
        if not inventory:
            logger.warn('requested item to deposit was not found in inventory.')
            continue
        target_item = qh.get_inventory(item['id'])
        success = False
        if 'quantity' in item:
            success = osrs.move.right_click_v6(
                target_item,
                f'Deposit-{item["quantity"]}',
                qh.get_canvas(),
                in_inv=True
            )
        else:
            osrs.move.fast_click(target_item)
        # we are depositing X amount, tell the bank what that amount is
        if success and 'amount' in item:
            while True:
                qh.query_backend()
                if qh.get_widgets(input_widget) and not qh.get_widgets(input_widget)['isHidden']:
                    osrs.clock.sleep_one_tick()
                    osrs.keeb.write(str(item['amount']))
                    osrs.keeb.press_key('enter')
                    break
        # wait for item to be deposited
        while True:
            qh.query_backend()
            deposited = True
            for new_item in qh.get_inventory():
                if new_item == target_item:
                    deposited = False
                    break
            if deposited:
                break


def set_withdrawl_and_deposit_quantity(value):
    one_widget = '12,29'
    five_widget = '12,31'
    ten_widget = '12,33'
    x_widget = '12,35'
    all_widget = '12,37'
    input_widget = '162,42'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_canvas()
    qh.set_widgets({one_widget, five_widget, ten_widget, x_widget, all_widget, input_widget})
    while True:
        qh.query_backend()
        # setting a custom quantity
        if str(value).lower() not in ['1', '5', '10', 'all'] and qh.get_widgets(x_widget):
            success = osrs.move.right_click_v6(
                qh.get_widgets(x_widget), 'Set custom quantity',
                qh.get_canvas(),
                in_inv=True
            )
            if success:
                wait_start = datetime.datetime.now()
                while True:
                    qh.query_backend()
                    if qh.get_widgets(input_widget):
                        osrs.keeb.write(str(value))
                        osrs.keeb.press_key('enter')
                        return
                    elif (datetime.datetime.now() - wait_start).total_seconds() > 5:
                        break
        elif str(value) == '1' and qh.get_widgets(one_widget):
            osrs.move.click(qh.get_widgets(one_widget))
            return
        elif str(value) == '5' and qh.get_widgets(five_widget):
            osrs.move.click(qh.get_widgets(five_widget))
            return
        elif str(value) == '10' and qh.get_widgets(ten_widget):
            osrs.move.click(qh.get_widgets(ten_widget))
            return
        elif str(value).lower() == 'all' and qh.get_widgets(all_widget):
            osrs.move.click(qh.get_widgets(all_widget))
            return


def banking_handler(params, wait_on_deposited_items=True):
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
    bf_bank_tile = '1948,4956,0'
    bf_bank_id = 26707
    lum_top_floor_bank_tile = '3208,3221,2'
    lum_top_floor_bank_id = 18491
    draynor_bank_tile = '3091,3245,0'
    draynor_bank_id = 10355
    c_wars_bank_tile = '2444,3083,0'
    c_wars_bank_id = 4483
    v_west_bank_tile_1 = '3186,3436,0'
    v_west_bank_id_1 = '34810'
    barb_assault_bank_tile = '2537,3573,0'
    barb_assault_bank_id = '19051'
    gnome_strong_bank_tile = '2449,3481,1'
    gnome_strong_bank_id = '10355'
    ferox_bank_tile = '3130,3632,0'
    ferox_bank_id = '26711'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([*ge_banker_npc_ids, *varr_banker_npc_ids, *fally_banker_npc_ids])
    qh.set_objects(
        {bf_bank_tile, crafting_guild_bank_tile, c_wars_bank_tile, v_west_bank_tile_1, lum_top_floor_bank_tile, draynor_bank_tile, barb_assault_bank_tile, gnome_strong_bank_tile, ferox_bank_tile},
        {bf_bank_id, crafting_guild_bank_id, c_wars_bank_id, v_west_bank_id_1, lum_top_floor_bank_id, draynor_bank_id, barb_assault_bank_id, gnome_strong_bank_id, ferox_bank_id},
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
    banker_search_duration = datetime.datetime.now()
    prev_loc = None
    time_on_same_tile = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        if (datetime.datetime.now() - banker_search_duration).total_seconds() > 60:
            return {'error': 'No banker.'}

        qh.query_backend()
        # Exit Condition: successfully opened the banking interface
        if qh.get_bank():
            print('Banking interface is open.')
            break

        # combine the npcs and bank objects into one list
        all_bank_objects = osrs.util.combine_objects(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value))
        if qh.get_npcs():
            all_bank_objects += qh.get_npcs()
        c = osrs.util.find_closest_target(all_bank_objects)
        if c and osrs.move.is_clickable(c) and (datetime.datetime.now() - time_on_same_tile).total_seconds() > 1.2:
            osrs.move.fast_click_v2(c)

        if prev_loc != qh.get_player_world_location():
            prev_loc = qh.get_player_world_location()
            time_on_same_tile = datetime.datetime.now()


    dumped_inv = False
    dumped_equipment = False
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
    if wait_on_deposited_items:
        osrs.clock.random_sleep(1, 1.1)
    qh.query_backend()
    # set the default withdrawal and deposit value for banking
    if 'set_quantity' in params:
        set_withdrawl_and_deposit_quantity(params['set_quantity'])
    # Withdraw desired items
    if 'deposit' in params:
        deposit_items(params['deposit'])
    if 'withdraw' in params:
        success = withdraw(params['withdraw'], qh)
        if not success:
            print('Failed to withdraw items successfully.')
            return False
    if 'withdraw_v2' in params:
        success = withdraw_v2(params['withdraw_v2'], qh)
        if not success:
            print('Failed to withdraw items successfully.')
            return False
    if 'search' in params:
        success = search_and_withdraw(params['search'], qh)
        if not success:
            print('Failed to search and withdraw items successfully.')
            exit('failed')
            return False
    while True:
        qh.query_backend()
        if not qh.get_bank():
            break
        else:
            osrs.keeb.press_key('esc')
    return True


def abort_offer(slot=None, item_name=None):
    collect_widget = '465,6,1'
    slot_1_item_name = '465,7,19'
    slot_2_item_name = '465,8,19'
    slot_3_item_name = '465,9,19'
    slot_4_item_name = '465,10,19'
    slot_5_item_name = '465,11,19'
    slot_6_item_name = '465,12,19'
    slot_7_item_name = '465,13,19'
    slot_8_item_name = '465,14,19'
    slot_scan = [
        slot_1_item_name,
        slot_2_item_name,
        slot_3_item_name,
        slot_4_item_name,
        slot_5_item_name,
        slot_6_item_name,
        slot_7_item_name,
        slot_8_item_name,
    ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        collect_widget,
        slot_1_item_name,
        slot_2_item_name,
        slot_3_item_name,
        slot_4_item_name,
        slot_5_item_name,
        slot_6_item_name,
        slot_7_item_name,
        slot_8_item_name,
    })
    qh.set_right_click_menu()
    qh.set_canvas()
    if not slot:
        while True:
            found = False
            qh.query_backend()
            for widget in slot_scan:
                if qh.get_widgets(widget) and qh.get_widgets(widget)['text'].lower() == item_name.lower():
                    slot = qh.get_widgets(widget)
                    found = True
                    break
            if found:
                break
    while True:
        res = osrs.move.right_click_v6(slot, 'Abort offer', qh.get_canvas(), in_inv=True)
        if res:
            break

    osrs.clock.sleep_one_tick()
    osrs.clock.sleep_one_tick()
    while True:
        qh.query_backend()
        if qh.get_widgets(collect_widget):
            osrs.move.click(qh.get_widgets(collect_widget))
            break


def purchase_item(item, quantity, prev_price=0):
    print('pp', prev_price)
    logger.info('invoked')
    first_search_result = '162,50,0'
    default_item_value = '465,25,41'
    default_item_quantity = '465,25,51'
    three_dots_offer_screen = '465,25,12'
    booth_id = 10061
    chat_input_widget = '162,42'
    confirm_offer_widget = '465,29'
    ge_widget = '465,0'
    box_1_widget = '465,7'
    box_2_widget = '465,8'
    box_3_widget = '465,9'
    box_4_widget = '465,10'
    box_5_widget = '465,11'
    box_6_widget = '465,12'
    box_7_widget = '465,13'
    box_8_widget = '465,14'
    collect_widget = '465,6,1'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        ge_widget,
        box_1_widget,
        box_2_widget,
        box_3_widget,
        box_4_widget,
        box_5_widget,
        box_6_widget,
        box_7_widget,
        box_8_widget,
        chat_input_widget,
        first_search_result,
        default_item_value,
        three_dots_offer_screen,
        confirm_offer_widget,
        default_item_quantity
    })
    qh.set_objects_v2('wall', {booth_id})
    qh.set_player_world_location()
    for offer_slot in [
        box_1_widget, box_2_widget, box_3_widget, box_4_widget, box_5_widget, box_6_widget, box_7_widget, box_8_widget
    ]:
        qh1 = osrs.queryHelper.QueryHelper()
        qh1.set_widgets({f'{offer_slot},0'})
        qh1.query_backend()
        if not qh1.get_widgets(f'{offer_slot},0'):
            continue
        osrs.move.fast_click(qh1.get_widgets(f'{offer_slot},0'))
        logger.info('clicked on buy an item widget')
        while True:
            qh.query_backend()
            if qh.get_widgets(chat_input_widget):
                break
        target_item = osrs.item_ids.ItemIDs(item).name.replace('_', ' ').lower() if type(item) is int else item.lower()
        osrs.keeb.write(target_item)
        logger.info('entered in the name of item i am buying')
        osrs.clock.sleep_one_tick()
        while True:
            qh.query_backend()
            if qh.get_widgets(first_search_result):
                break
        qh2 = osrs.queryHelper.QueryHelper()
        qh2.set_widgets({'162,50,1'})
        qh2.set_widgets({'162,50,4'})
        qh2.set_widgets({'162,50,7'})
        qh2.set_widgets({'162,50,10'})
        qh2.set_widgets({'162,50,13'})
        qh2.set_widgets({'162,50,16'})
        qh2.set_widgets({'162,50,19'})
        qh2.set_widgets({'162,50,22'})
        qh2.set_widgets({'162,50,25'})
        qh2.query_backend()
        for widget in qh2.get_widgets():
            widget = qh2.get_widgets(widget)
            if widget['text'].lower() == target_item:
                osrs.move.click(widget)
        logger.info('clicked on the first returned search item')
        while True:
            qh.query_backend()
            if qh.get_widgets(default_item_value) and qh.get_widgets(default_item_value)['text']:
                break
        value = int(qh.get_widgets(default_item_value)['text'].split(' ')[0].replace(',', ''))
        if prev_price > 0:
            value = prev_price
        value = math.ceil(value * 1.2)
        logger.info('clicking on the custom price three dots')
        while True:
            qh.query_backend()
            if qh.get_widgets(three_dots_offer_screen):
                break
        osrs.move.click(qh.get_widgets(three_dots_offer_screen))
        logger.info('item price input up. entering desired price')
        while True:
            qh.query_backend()
            if qh.get_widgets(chat_input_widget) and not qh.get_widgets(chat_input_widget)['isHidden']:
                break
        osrs.keeb.write(str(value))
        osrs.keeb.press_key('enter')
        if quantity != 1:
            logger.info('clicking on the custom quantity three dots')
            while True:
                qh.query_backend()
                if qh.get_widgets(default_item_quantity):
                    break
            osrs.move.click(qh.get_widgets(default_item_quantity))
            logger.info('item price input up. entering desired quantity')
            while True:
                qh.query_backend()
                if qh.get_widgets(chat_input_widget) and not qh.get_widgets(chat_input_widget)['isHidden']:
                    break
            osrs.keeb.write(str(quantity))
            osrs.keeb.press_key('enter')
        logger.info('click on confirm offer')
        while True:
            qh.query_backend()
            if qh.get_widgets(confirm_offer_widget):
                break
        osrs.move.click(qh.get_widgets(confirm_offer_widget))
        logger.info('clicking on collect items')
        wait_time = datetime.datetime.now()
        qh.set_widgets({collect_widget})
        # sometimes clicks when the widget isnt there. make sure its actually there
        time_widget_up = datetime.datetime.now() - datetime.timedelta(hours=1)
        while True:
            qh.query_backend()
            if qh.get_widgets(collect_widget):
                if (datetime.datetime.now() - time_widget_up).total_seconds() > 1.3:
                    print('here', qh.get_widgets(collect_widget))
                    osrs.clock.sleep_one_tick()
                    break
            else:
                time_widget_up = datetime.datetime.now()
            # this offer isnt buying. up the price!

            if (datetime.datetime.now() - wait_time).total_seconds() > 5:
                abort_offer(offer_slot)
                osrs.clock.sleep_one_tick()
                return purchase_item(item, quantity, value)
        print('jj', qh.get_widgets(collect_widget))
        osrs.move.click(qh.get_widgets(collect_widget))
        return


def search_ge_inv(item):
    slots = [
        '467,0,0',
        '467,0,1',
        '467,0,2',
        '467,0,3',
        '467,0,4',
        '467,0,5',
        '467,0,6',
        '467,0,7',
        '467,0,8',
        '467,0,9',
        '467,0,10',
        '467,0,11',
        '467,0,12'
        '467,0,13',
        '467,0,14',
        '467,0,15',
        '467,0,16',
        '467,0,17',
        '467,0,18',
        '467,0,19',
        '467,0,20',
        '467,0,21',
        '467,0,22',
        '467,0,23',
        '467,0,24',
        '467,0,25',
        '467,0,26',
        '467,0,27',
    ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets(set(slots))
    qh.query_backend()
    for widget in qh.get_widgets():
        if qh.get_widgets(widget)['itemID'] == item:
            return qh.get_widgets(widget)


def sell_item(item, quantity, custom_name, value=0):
    sell_price = '465,25,41'
    first_search_result = '162,50,0'
    default_item_value = '465,25,41'
    default_item_quantity = '465,25,51'
    three_dots_offer_screen = '465,25,12'
    booth_id = 10061
    chat_input_widget = '162,42'
    confirm_offer_widget = '465,29'
    ge_widget = '465,0'
    box_1_widget = '465,7'
    box_2_widget = '465,8'
    box_3_widget = '465,9'
    box_4_widget = '465,10'
    box_5_widget = '465,11'
    box_6_widget = '465,12'
    box_7_widget = '465,13'
    box_8_widget = '465,14'
    collect_widget = '465,6,1'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        ge_widget,
        box_1_widget,
        box_2_widget,
        box_3_widget,
        box_4_widget,
        box_5_widget,
        box_6_widget,
        box_7_widget,
        box_8_widget,
        chat_input_widget,
        first_search_result,
        default_item_value,
        three_dots_offer_screen,
        confirm_offer_widget,
        default_item_quantity,
        sell_price
    })
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_widgets(three_dots_offer_screen) and not qh.get_widgets(three_dots_offer_screen)['isHidden']:
            break
        elif search_ge_inv(item):
            osrs.move.click(search_ge_inv(item))
    logger.info('fetching default sell price')
    if value == 0:
        while True:
            qh.query_backend()
            if qh.get_widgets(default_item_value) and qh.get_widgets(default_item_value)['text']:
                value = int(qh.get_widgets(default_item_value)['text'].split(' ')[0])
                break
    logger.info('clicking on the custom price three dots')
    while True:
        qh.query_backend()
        if qh.get_widgets(three_dots_offer_screen):
            break
    osrs.move.click(qh.get_widgets(three_dots_offer_screen))
    logger.info('item price input up. entering desired price')
    while True:
        qh.query_backend()
        if qh.get_widgets(chat_input_widget) and not qh.get_widgets(chat_input_widget)['isHidden']:
            break
    osrs.keeb.write(str(value))
    osrs.keeb.press_key('enter')
    if quantity != 'All':
        logger.info('clicking on the custom quantity three dots')
        while True:
            qh.query_backend()
            if qh.get_widgets(default_item_quantity):
                break
        osrs.move.click(qh.get_widgets(default_item_quantity))
        logger.info('item price input up. entering desired quantity')
        while True:
            qh.query_backend()
            if qh.get_widgets(chat_input_widget) and not qh.get_widgets(chat_input_widget)['isHidden']:
                break
        osrs.keeb.write(str(quantity))
        osrs.keeb.press_key('enter')
    logger.info('click on confirm offer')
    while True:
        qh.query_backend()
        if qh.get_widgets(confirm_offer_widget):
            break
    osrs.move.click(qh.get_widgets(confirm_offer_widget))
    logger.info('clicking on collect items')
    wait_time = datetime.datetime.now()
    qh.set_widgets({collect_widget})
    # sometimes clicks when the widget isnt there. make sure its actually there
    time_widget_up = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets(collect_widget):
            if (datetime.datetime.now() - time_widget_up).total_seconds() > 1.3:
                print('here', qh.get_widgets(collect_widget))
                osrs.clock.sleep_one_tick()
                break
        else:
            time_widget_up = datetime.datetime.now()
        # this offer isnt buying. up the price!

        if (datetime.datetime.now() - wait_time).total_seconds() > 5:
            item_to_search_for = custom_name if custom_name else item
            abort_offer(item_name=item_to_search_for)
            osrs.clock.sleep_one_tick()
            return sell_item(item, quantity, custom_name, math.floor(value * 0.8))
    print('jj', qh.get_widgets(collect_widget))
    osrs.move.click(qh.get_widgets(collect_widget))
    return


def ge_handler(items):
    '''
    items: {'id': 123, 'quantity': 10, 'id_override': 'prayer potion(4)'}
    :return: True || False
    '''
    first_search_result = '162,50,0'
    default_item_value = '465,25,41'
    three_dots_offer_screen = '465,25,12'
    booth_id = 10061
    chat_input_widget = '162,42'
    confirm_offer_widget = '465,29'
    ge_widget = '465,0'
    box_1_widget = '465,7'
    box_2_widget = '465,8'
    box_3_widget = '465,9'
    box_4_widget = '465,10'
    box_5_widget = '465,11'
    box_6_widget = '465,12'
    box_7_widget = '465,13'
    box_8_widget = '465,14'
    collect_widget = '465,6,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        ge_widget,
        box_1_widget,
        box_2_widget,
        box_3_widget,
        box_4_widget,
        box_5_widget,
        box_6_widget,
        box_7_widget,
        box_8_widget,
        collect_widget,
        chat_input_widget,
        first_search_result,
        default_item_value,
        three_dots_offer_screen,
        confirm_offer_widget
    })
    qh.set_objects_v2('wall', {booth_id})
    qh.set_player_world_location()
    last_loc = None
    last_loc_change = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location() != last_loc:
            last_loc_change = datetime.datetime.now()
            last_loc = qh.get_player_world_location()

        if qh.get_widgets(ge_widget) and not qh.get_widgets(ge_widget)['isHidden']:
            break
        elif qh.get_objects_v2('wall', booth_id) and (datetime.datetime.now() - last_loc_change).total_seconds() > 3:
            last_loc_change = datetime.datetime.now()
            c = sorted(qh.get_objects_v2('wall', booth_id), key=lambda obj: obj['dist'])
            osrs.move.fast_click(c[0])
    for item in items:
        search_id = item['id'] if 'id_override' not in item else item['id_override']
        if 'sell' in item:
            sell_item(item['id'], item['quantity'], search_id)
            continue
        purchase_item(search_id, item['quantity'])
    osrs.keeb.press_key('esc')
    return

