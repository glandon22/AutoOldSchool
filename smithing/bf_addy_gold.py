import datetime

import osrs
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
coal = 453
addy_ore = 449
coal_bag = 12019
single_dose_stam = 12631
vial = 229
addy_bar_id = 2361
gold_bar_id = 2361


def click_ore_belt(qh):
    while True:
        qh.query_backend()
        if qh.get_game_objects('9100') and len(qh.get_game_objects('9100')) > 0:
            break
    osrs.move.click(qh.get_game_objects('9100')[0])


def out_of_ore():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory([
        osrs.item_ids.ItemIDs.COAL.value,
        osrs.item_ids.ItemIDs.ADAMANTITE_ORE.value,
        osrs.item_ids.ItemIDs.GOLD_ORE.value,
    ]):
        return True


def put_ore_on_belt(tc, qh):
    osrs.move.interact_with_object(
        9100, 'x', 1, False, right_click_option='Put-ore-on',
        custom_exit_function=out_of_ore, timeout=15
    )
    # put on gold smith gauntlets when smelting gold
    if tc != 0:
        osrs.player.equip_item([osrs.item_ids.ItemIDs.GOLDSMITH_GAUNTLETS.value])
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.COAL_BAG_12019.value):
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.item_ids.ItemIDs.COAL_BAG_12019.value),
                'Empty',
                qh.get_canvas(),
                in_inv=True
            )
            break
    while True:
        qh.query_backend()
        if qh.get_inventory([
            osrs.item_ids.ItemIDs.COAL.value,
            osrs.item_ids.ItemIDs.GOLD_ORE.value,
            osrs.item_ids.ItemIDs.ADAMANTITE_ORE.value,
        ]):
            break
    osrs.move.interact_with_object(
        9100, 'x', 1, False, right_click_option='Put-ore-on',
        custom_exit_function=out_of_ore, timeout=4
    )


def drink_stam(bank_data):
    stam = osrs.inv.is_item_in_inventory_v2(bank_data, single_dose_stam)
    if stam:
        osrs.move.right_click_menu_select(stam, 2, port)
    else:
        exit('out of stams')
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)
    osrs.clock.random_sleep(0.8, 0.9)
    inv = osrs.inv.get_inv(port, True)
    print('inv', inv)
    stam_inv = osrs.inv.is_item_in_inventory_v2(inv, single_dose_stam)
    if stam_inv:
        osrs.move.move_and_click(stam_inv['x'], stam_inv['y'], 2, 2)
        osrs.clock.random_sleep(0.6, 0.7)
        while True:
            inv = osrs.inv.get_inv(port)
            vial_inv = osrs.inv.is_item_in_inventory_v2(inv, vial)
            if vial_inv:
                osrs.move.right_click_menu_select(vial_inv, 2, port)
                break


def click_bank(bank_chest):
    print(bank_chest)
    osrs.move.click(bank_chest)
    osrs.bank.wait_for_bank_interface(port)


def bank(trip_count, qh):
    banking_config = {
        'deposit': [{'id': osrs.item_ids.ItemIDs.GOLD_BAR.value}, {'id': osrs.item_ids.ItemIDs.ADAMANTITE_BAR.value}],
        'withdraw_v2': [osrs.item_ids.ItemIDs.COAL.value]
    }
    run_energy = qh.get_widgets('160,28')
    if run_energy and int(run_energy['text']) < 35:
        banking_config['withdraw_v2'] = [{
            'id': osrs.item_ids.ItemIDs.STAMINA_POTION1.value,
            'quantity': 1,
            'consume': 'Drink'
        }] + banking_config['withdraw_v2']
    osrs.bank.banking_handler(banking_config, wait_on_deposited_items=False)
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.COAL_BAG_12019.value):
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.COAL_BAG_12019.value))
            break
    osrs.bank.banking_handler({
        'withdraw_v2': [
            osrs.item_ids.ItemIDs.GOLD_ORE.value if trip_count != 0 else osrs.item_ids.ItemIDs.ADAMANTITE_ORE.value
        ]
    }, wait_on_deposited_items=False)
    while True:
        qh.query_backend()
        if qh.get_inventory([
            osrs.item_ids.ItemIDs.COAL.value,
            osrs.item_ids.ItemIDs.GOLD_ORE.value,
            osrs.item_ids.ItemIDs.ADAMANTITE_ORE.value,
        ]):
            break


def collect_bars(tc, qh):
    qh.query_backend()
    if qh.get_varbit() == 27:
        while True:
            qh.query_backend()
            osrs.move.click(qh.get_tiles('1940,4963,0'))
            start_time = datetime.datetime.now()
            while True:
                qh.query_backend()
                if (datetime.datetime.now() - start_time).total_seconds() > 6:
                    break
                elif qh.get_widgets('270,4'):
                    keyboard.press(Key.space)
                    keyboard.release(Key.space)
                    return


# 9092 1940,4963,0
script_config = {
    'intensity': 'high',
    'login': lambda: osrs.clock.random_sleep(3, 4),
    'logout': False
}


def confirm_bars():
    osrs.keeb.press_key('space')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory([
        osrs.item_ids.ItemIDs.GOLD_BAR.value,
        osrs.item_ids.ItemIDs.ADAMANTITE_BAR.value,
    ]) and (osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.ItemIDs.GOLD_BAR.value) >= 26
            or osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.ItemIDs.ADAMANTITE_BAR.value) >= 26):
        return True


def equip():
    osrs.player.equip_item([osrs.item_ids.ItemIDs.ICE_GLOVES.value])

def main():
    trip_count = 1
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_bank()
    qh.set_canvas()
    qh.set_widgets({'160,28', '270,4'})
    qh.set_game_objects(
        {'1948,4956,0', '1943,4967,0', '1940,4963,0'},
        {'26707', '9100', '9092'}
    )
    qh.set_tiles({
        '1939,4963,0',
        '1940,4963,0'
    })
    qh.set_varbit('945')
    while True:
        qh.query_backend()
        osrs.game.break_manager_v4(script_config)
        bank(trip_count % 3, qh)
        put_ore_on_belt(trip_count, qh)
        osrs.move.go_to_loc(1939, 4963)
        osrs.move.interact_with_object(
            9092, 'x', 1, False,
            custom_exit_function=confirm_bars, right_click_option='Take', timeout=2, pre_interact=equip
        )
        trip_count += 1

main()