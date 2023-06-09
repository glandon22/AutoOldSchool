import datetime

import keyboard


import osrs

minimum_eat_health = 35
absorption_pots = [11734, 11735, 11736, 11737]
port = '56800'
nmz_to_bank = [
    '2615,3111,0',
    '2613,3102,0',
    '2605,3097,0'
]

# npc id list - if im out of super combats, it will stop clicking, may need to handle that - 7895, 6383, 8528, 3535, 639
'''
DO NOT USE - got banned using this script.
'''

def main():
    start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    script_start = datetime.datetime.now()
    while True:
        q = {
            'skills': ['strength'],
            'inv': True,
            'playerWorldPoint': True
        }
        data = osrs.server.query_game_data(q, port)
        absorption_amt = osrs.server.get_varbit_value('3956', port)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['z'] < 3:
            script_start = osrs.game.break_manager(script_start, 30, 35, 320, 508, 'pass_71', False, port)
            print('Dead, re supplying.')
            osrs.clock.random_sleep(3, 3.1)
            bank_and_return()
            print('Returned to NMZ.')
            withdraw_absorption_pots()
            print('Starting new dream.')
            start_dream()
        elif absorption_amt < 50 and 'inv' in data:
            food = osrs.inv.are_items_in_inventory(data['inv'], absorption_pots)
            if not food:
                print('out of food')
                continue
            else:
                while absorption_amt < 950:
                    inv = osrs.inv.get_inv(port)
                    food = osrs.inv.are_items_in_inventory_v2(inv, absorption_pots)
                    if not food:
                        print('out of food')
                        break
                    osrs.move.move_and_click(food['x'], food['y'], 4, 4)
                    osrs.clock.random_sleep(0.2, 0.3)
                    absorption_amt = osrs.server.get_varbit_value('3956', port)
            osrs.move.click_off_screen(200, 1230, 200, 800, False)
        elif (datetime.datetime.now() - start_time).total_seconds() > 900:
            print('Potting up.')
            super_combat = osrs.inv.are_items_in_inventory_v2(data['inv'], [12695, 12697, 12699, 12701])
            if not super_combat:
                print('out of super combats')
            else:
                osrs.move.move_and_click(super_combat['x'], super_combat['y'], 4, 4)
                osrs.move.click_off_screen(300, 1000, 300, 700, False)
            start_time = datetime.datetime.now()
            osrs.clock.random_sleep(0.5, 0.6)


def bank_and_return():
    osrs.move.run_to_loc(nmz_to_bank, port)
    osrs.clock.random_sleep(0.5, 0.6)
    bank = osrs.server.get_game_object('2614,3094,0', '10356', port)
    osrs.move.move_and_click(bank['x'], bank['y'], 3, 3)
    osrs.bank.wait_for_bank_interface(port)
    osrs.clock.random_sleep(0.5, 0.6)
    osrs.bank.bank_dump_inv(port)
    bank_data = osrs.bank.get_bank_data(port)
    super_combat = osrs.inv.is_item_in_inventory_v2(bank_data, 12695)
    osrs.move.right_click_menu_select(super_combat, 3, port)
    osrs.clock.random_sleep(0.3, 0.4)
    osrs.move.right_click_menu_select(super_combat, 2, port)
    osrs.clock.random_sleep(0.3, 0.4)
    keyboard.send('esc')
    osrs.clock.random_sleep(0.3, 0.4)
    osrs.move.run_to_loc(nmz_to_bank[::-1], port)
    osrs.clock.random_sleep(0.6, 0.7)


def withdraw_absorption_pots():
    barrel = osrs.server.get_game_object('2600,3117,0', '26280', port)
    osrs.move.right_click_menu_select(barrel, None, port, 'Absorption', 'Take')
    osrs.clock.random_sleep(8, 8.1)
    osrs.keeb.keyboard.type('88')
    osrs.clock.random_sleep(0.2, 0.3)
    keyboard.send('enter')
    keyboard.send('esc')


def start_dream():
    dom = osrs.server.get_npc_by_id('1120', port)
    osrs.move.move_and_click(dom['x'], dom['y'], 2, 2)
    while True:
        chat = osrs.server.get_chat_options(port)
        if chat:
            for i, option in enumerate(chat):
                if 'Customisable Rumble' in option:
                    keyboard.send(str(i))
                    break
            break
    osrs.clock.random_sleep(1, 1.1)
    keyboard.send('space')
    osrs.clock.random_sleep(1, 1.1)
    keyboard.send('1')
    osrs.clock.random_sleep(0.6, 0.7)
    pot = osrs.server.get_game_object('2605,3117,0', '26291', port)
    osrs.move.move_and_click(pot['x'], pot['y'], 1, 3)
    osrs.clock.random_sleep(0.5, 0.6)
    osrs.move.wait_until_stationary(port)
    osrs.clock.random_sleep(1, 1.1)
    while True:
        accept = osrs.server.get_widget('129,6', port)
        if accept:
            osrs.move.move_and_click(accept['x'], accept['y'], 6, 3)
            break
    while True:
        loc = osrs.server.get_world_location(port)
        if 'z' in loc and loc['z'] == 3:
            osrs.clock.random_sleep(1, 1.1)
            break
    loc = osrs.server.get_world_location(port)
    osrs.move.run_to_loc(['{},{},3'.format(loc['x'] - 5, loc['y'] + 14)], port) # for whatever reason, the world points are different in NMZ.


main()
