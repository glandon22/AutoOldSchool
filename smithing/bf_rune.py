import datetime
import osrs

import osrs
from pynput.keyboard import Key, Controller

keyboard = Controller()
port = '56799'
coal = 453
rune_ore = 451
coal_bag = 12019
single_dose_stam = 12631
vial = 229
rune_bar_id = 2363


def click_ore_belt(qh):
    while True:
        while True:
            qh.query_backend()
            if qh.get_game_objects('9100') and len(qh.get_game_objects('9100')) > 0:
                break
        osrs.move.click(qh.get_game_objects('9100')[0])
        start = datetime.datetime.now()
        while True:
            qh.query_backend()
            inv = qh.get_inventory()
            if len(inv) == 1 and inv[0]['id'] == coal_bag:
                return
            elif (datetime.datetime.now() - start).total_seconds() > 8:
                break


def put_ore_on_belt(qh):
    click_ore_belt(qh)
    coal_bag_inv = qh.get_inventory(coal_bag)
    osrs.move.click(coal_bag_inv)
    click_ore_belt(qh)


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


def click_bank(qh: osrs.queryHelper.QueryHelper):
    while True:
        while True:
            qh.query_backend()
            if qh.get_game_objects('26707') and len(qh.get_game_objects('26707')) > 0:
                break
        osrs.move.click(qh.get_game_objects('26707')[0])
        start = datetime.datetime.now()
        while True:
            qh.query_backend()
            if qh.get_widgets('12,42'):
                return
            elif (datetime.datetime.now() - start).total_seconds() > 8:
                break


def bank(trip_count, qh):
    qh.query_backend()
    click_bank(qh)
    qh.query_backend()
    rune_bar = qh.get_inventory(rune_bar_id)
    if rune_bar:
        osrs.move.click(rune_bar)
    coal_bag_inv = qh.get_inventory(coal_bag)
    osrs.move.click(coal_bag_inv)
    run_energy = qh.get_widgets('160,28')
    if run_energy and int(run_energy['text']) < 35:
        drink_stam(qh.get_bank())
        click_bank(qh)
        qh.query_backend()
    if trip_count in [1, 2, 4]:
        coal_bank = qh.get_bank(coal)
        if not coal_bank:
            exit('no coal')
        osrs.move.move_and_click(coal_bank['x'], coal_bank['y'], 3, 3)
    else:
        rune_bank = qh.get_bank(rune_ore)
        if not rune_bank:
            exit('no rune')
        osrs.move.move_and_click(rune_bank['x'], rune_bank['y'], 3, 3)
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)
# 9100 1943,4967,0


def collect_bars(qh):
    while True:
        qh.query_backend()
        print('vb', qh.get_varbit())
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


def main():
    trip_count = 1
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_bank()
    qh.set_widgets({'160,28', '270,4', '12,42'})
    qh.set_game_objects(
        {'1948,4956,0', '1943,4967,0', '1940,4963,0'},
        {'26707', '9100', '9092'}
    )
    qh.set_tiles({
        '1939,4963,0',
        '1940,4963,0'
    })
    qh.set_varbit('946')
    while True:
        osrs.game.break_manager_v4(script_config)
        bank(trip_count % 5, qh)
        put_ore_on_belt(qh)
        if trip_count % 5 in [1, 4] and trip_count > 1:
            print('collecting!')
            collect_bars(qh)
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
        trip_count += 1

main()
