import datetime

import keyboard

from osrs_utils import general_utils

minimum_eat_health = 35
food_to_eat = [7946, 379, 361]
port = '56800'
nmz_to_bank = [
    '2615,3111,0',
    '2613,3102,0',
    '2605,3097,0'
]


def main():
    start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    script_start = datetime.datetime.now()
    while True:
        q = {
            'interactingWith': True,
            'skills': ['hitpoints'],
            'inv': True,
            'playerWorldPoint': True
        }
        data = general_utils.query_game_data(q, port)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['z'] < 3:
            script_start = general_utils.break_manager(script_start, 30, 35, 320, 508, 'pass_71', False, port)
            print('Dead, re supplying.')
            general_utils.random_sleep(3, 3.1)
            bank_and_return()
            print('Starting new dream.')
            start_dream()
        elif 'skills' in data and \
                'hitpoints' in data['skills'] and \
                data['skills']['hitpoints']['boostedLevel'] < minimum_eat_health and 'inv' in data:
            food = general_utils.are_items_in_inventory(data['inv'], food_to_eat)
            if not food:
                print('out of food')
            else:
                general_utils.move_and_click(food[0], food[1], 4, 4)
                general_utils.click_off_screen(300, 1000, 300, 1100, False)
                general_utils.random_sleep(1, 1.1)
        elif (datetime.datetime.now() - start_time).total_seconds() > 900 and 'inv' in data:
            print('Potting up.')
            super_combat = general_utils.are_items_in_inventory_v2(data['inv'], [12695, 12697, 12699, 12701])
            if not super_combat:
                print('out of super combats')
            else:
                general_utils.move_and_click(super_combat['x'], super_combat['y'], 4, 4)
                general_utils.click_off_screen(300, 1000, 300, 700, False)
            start_time = datetime.datetime.now()
            general_utils.random_sleep(0.5, 0.6)
        elif 'interactingWith' in data:
            print('In combat, no action needed.')
            general_utils.random_sleep(0.5, 0.6)


def bank_and_return():
    general_utils.run_to_loc(nmz_to_bank, port)
    general_utils.random_sleep(0.5, 0.6)
    bank = general_utils.get_game_object('2614,3094,0', '10356', port)
    general_utils.move_and_click(bank['x'], bank['y'], 3, 3)
    general_utils.wait_for_bank_interface(port)
    general_utils.random_sleep(0.5, 0.6)
    general_utils.bank_dump_inv(port)
    bank_data = general_utils.get_bank_data(port)
    super_combat = general_utils.is_item_in_inventory_v2(bank_data, 12695)
    general_utils.right_click_menu_select(super_combat, 2, port)
    general_utils.random_sleep(0.3, 0.4)
    monkfish = general_utils.is_item_in_inventory_v2(bank_data, 7946)
    general_utils.move_and_click(monkfish['x'], monkfish['y'], 3, 3)
    general_utils.random_sleep(0.3, 0.4)
    keyboard.send('esc')
    general_utils.random_sleep(0.3, 0.4)
    general_utils.run_to_loc(nmz_to_bank[::-1], port)
    general_utils.random_sleep(0.6, 0.7)


def start_dream():
    dom = general_utils.get_npc_by_id('1120', port)
    general_utils.move_and_click(dom['x'], dom['y'], 2, 2)
    while True:
        chat = general_utils.get_chat_options(port)
        if chat:
            for i, option in enumerate(chat):
                if 'Customisable Rumble' in option:
                    keyboard.send(str(i))
                    break
            break
    general_utils.random_sleep(1, 1.1)
    keyboard.send('space')
    general_utils.random_sleep(1, 1.1)
    keyboard.send('1')
    general_utils.random_sleep(0.6, 0.7)
    pot = general_utils.get_game_object('2605,3117,0', '26291', port)
    general_utils.move_and_click(pot['x'], pot['y'], 1, 3)
    general_utils.random_sleep(0.5, 0.6)
    general_utils.wait_until_stationary(port)
    general_utils.random_sleep(1, 1.1)
    while True:
        accept = general_utils.get_widget('129,6', port)
        if accept:
            general_utils.move_and_click(accept['x'], accept['y'], 6, 3)
            break
    while True:
        loc = general_utils.get_world_location(port)
        if 'z' in loc and loc['z'] == 3:
            general_utils.random_sleep(1, 1.1)
            break
    loc = general_utils.get_world_location(port)
    general_utils.run_to_loc(['{},{},3'.format(loc['x'] - 5, loc['y'] + 14)], port) # for whatever reason, the world points are different in NMZ.


main()