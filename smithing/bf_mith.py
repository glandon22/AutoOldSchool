import datetime
import osrs

import osrs
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
coal = 453
mith_ore = 447
coal_bag = 12019
single_dose_stam = 12631
vial = 229
mithril_bar = 2359
#  get_varbit_value('25', '56800') returns 1 if i am under stam pot effects
#coal_bank = osrs.inv.is_item_in_inventory_v2(bank_data, coal)


def put_ore_on_belt():
    osrs.move.run_to_loc(['1943,4969,0'], port)
    while True:
        inv = osrs.inv.get_inv(port)
        if len(inv) == 1 and inv[0]['id'] == coal_bag:
            break
        elif osrs.move.am_stationary(port):
            osrs.move.run_to_loc(['1943,4968,0'], port)
    inv_data = osrs.inv.get_inv(port)
    coal_bag_inv = osrs.inv.is_item_in_inventory_v2(inv_data, coal_bag)
    osrs.move.right_click_menu_select(coal_bag_inv, None, port, 'Coal bag', 'Empty')
    osrs.move.run_to_loc(['1943,4967,0'], port)
    while True:
        inv = osrs.inv.get_inv(port)
        if len(inv) == 1 and inv[0]['id'] == coal_bag:
            break
        elif osrs.move.am_stationary(port):
            osrs.move.run_to_loc(['1943,4967,0'], port)


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


def click_bank():
    bank_chest = osrs.server.get_game_object('1948,4956,0', '26707', port)
    osrs.move.move_and_click(bank_chest['x'], bank_chest['y'], 3, 3)
    osrs.bank.wait_for_bank_interface(port)
    return osrs.bank.get_bank_data(port)


def bank(trip_count):
    bank_data = click_bank()
    inv_data = osrs.inv.get_inv(port)
    osrs.bank.deposit_all_but_x_in_bank([coal_bag], port)
    coal_bag_inv = osrs.inv.is_item_in_inventory_v2(inv_data,  coal_bag)
    osrs.move.right_click_menu_select(coal_bag_inv, None, port, 'Coal bag', 'Fill')
    run_energy = osrs.server.get_widget('160,28', port)
    if run_energy and int(run_energy['text']) < 35:
        drink_stam(bank_data)
        bank_data = click_bank()
        osrs.bank.deposit_all_but_x_in_bank([coal_bag], port)
    if trip_count == 0:
        coal_bank = osrs.inv.is_item_in_inventory_v2(bank_data, coal)
        if not coal_bank:
            exit('no coal')
        osrs.move.move_and_click(coal_bank['x'], coal_bank['y'], 3, 3)
    else:
        mith_bank = osrs.inv.is_item_in_inventory_v2(bank_data, mith_ore)
        if not mith_bank:
            exit('no mith')
        osrs.move.move_and_click(mith_bank['x'], mith_bank['y'], 3, 3)
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)


def collect_bars():
    osrs.move.run_to_loc(['1939,4963,0'], port)
    osrs.clock.random_sleep(0.5, 0.6)
    osrs.move.wait_until_stationary(port)
    while True:
        mith_bars_in_dispenser = osrs.server.get_varbit_value('944', port)
        if mith_bars_in_dispenser == 27:
            osrs.move.run_to_loc(['1940,4963,0'], port)
            while True:
                interface = osrs.server.get_widget('270,4', port)
                if interface and 'text' in interface:
                    break
                elif osrs.move.am_stationary(port):
                    osrs.move.run_to_loc(['1940,4963,0'], port)
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            break


def main():
    trip_count = 0
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 49, 54, 432, 673, 'pass_70', False, port)
        bank(trip_count % 3)
        put_ore_on_belt()
        print(trip_count, trip_count % 3, trip_count % 3 != 0)
        if trip_count % 3 != 0:
            collect_bars()
        trip_count += 1

osrs.clock.random_sleep(2, 3)
main()
