import datetime

from autoscape import general_utils
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
#coal_bank = general_utils.is_item_in_inventory_v2(bank_data, coal)


def put_ore_on_belt():
    general_utils.run_to_loc(['1943,4969,0'], port)
    while True:
        inv = general_utils.get_inv(port)
        if len(inv) == 1 and inv[0]['id'] == coal_bag:
            break
        elif general_utils.am_stationary(port):
            general_utils.run_to_loc(['1943,4968,0'], port)
    inv_data = general_utils.get_inv(port)
    coal_bag_inv = general_utils.is_item_in_inventory_v2(inv_data, coal_bag)
    general_utils.right_click_menu_select(coal_bag_inv, None, port, 'Coal bag', 'Empty')
    general_utils.run_to_loc(['1943,4967,0'], port)
    while True:
        inv = general_utils.get_inv(port)
        if len(inv) == 1 and inv[0]['id'] == coal_bag:
            break
        elif general_utils.am_stationary(port):
            general_utils.run_to_loc(['1943,4967,0'], port)


def drink_stam(bank_data):
    stam = general_utils.is_item_in_inventory_v2(bank_data, single_dose_stam)
    if stam:
        general_utils.right_click_menu_select(stam, 2, port)
    else:
        exit('out of stams')
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)
    general_utils.random_sleep(0.8, 0.9)
    inv = general_utils.get_inv(port, True)
    print('inv', inv)
    stam_inv = general_utils.is_item_in_inventory_v2(inv, single_dose_stam)
    if stam_inv:
        general_utils.move_and_click(stam_inv['x'], stam_inv['y'], 2, 2)
        general_utils.random_sleep(0.6, 0.7)
        while True:
            inv = general_utils.get_inv(port)
            vial_inv = general_utils.is_item_in_inventory_v2(inv, vial)
            if vial_inv:
                general_utils.right_click_menu_select(vial_inv, 2, port)
                break


def click_bank():
    bank_chest = general_utils.get_game_object('1948,4956,0', '26707', port)
    general_utils.move_and_click(bank_chest['x'], bank_chest['y'], 3, 3)
    general_utils.wait_for_bank_interface(port)
    return general_utils.get_bank_data(port)


def bank(trip_count):
    bank_data = click_bank()
    inv_data = general_utils.get_inv(port)
    general_utils.deposit_all_but_x_in_bank([coal_bag], port)
    coal_bag_inv = general_utils.is_item_in_inventory_v2(inv_data,  coal_bag)
    general_utils.right_click_menu_select(coal_bag_inv, None, port, 'Coal bag', 'Fill')
    run_energy = general_utils.get_widget('160,28', port)
    if run_energy and int(run_energy['text']) < 35:
        drink_stam(bank_data)
        bank_data = click_bank()
        general_utils.deposit_all_but_x_in_bank([coal_bag], port)
    if trip_count == 0:
        coal_bank = general_utils.is_item_in_inventory_v2(bank_data, coal)
        if not coal_bank:
            exit('no coal')
        general_utils.move_and_click(coal_bank['x'], coal_bank['y'], 3, 3)
    else:
        mith_bank = general_utils.is_item_in_inventory_v2(bank_data, mith_ore)
        if not mith_bank:
            exit('no mith')
        general_utils.move_and_click(mith_bank['x'], mith_bank['y'], 3, 3)
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)


def collect_bars():
    general_utils.run_to_loc(['1939,4963,0'], port)
    general_utils.random_sleep(0.5, 0.6)
    general_utils.wait_until_stationary(port)
    while True:
        mith_bars_in_dispenser = general_utils.get_varbit_value('944', port)
        if mith_bars_in_dispenser == 27:
            general_utils.run_to_loc(['1940,4963,0'], port)
            while True:
                interface = general_utils.get_widget('270,4', port)
                if interface and 'text' in interface:
                    break
                elif general_utils.am_stationary(port):
                    general_utils.run_to_loc(['1940,4963,0'], port)
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            break


def main():
    trip_count = 0
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 49, 54, 432, 673, 'pass_70', False, port)
        bank(trip_count % 3)
        put_ore_on_belt()
        print(trip_count, trip_count % 3, trip_count % 3 != 0)
        if trip_count % 3 != 0:
            collect_bars()
        trip_count += 1

general_utils.random_sleep(2, 3)
main()
