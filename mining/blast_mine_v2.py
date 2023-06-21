'''
TODO

check to make sure all spots available and no one in area before starting blasting
withdraw ores when at max capacity
be able to recover from failed blasts
'''


import datetime
import random
from pynput.keyboard import Key, Controller

import osrs

# 13573 dynamite
# does not handle leveling yet
port = '56799'
noted_mith_id = 448
world_list = [
    '374',
    '375',
    '376',
    '377',
    '378',
    '386',
    '387',
    '388',
    '389',
    '390'
]

states = [
    ['1473,3885,0', '28580'],
    ['1471,3886,0', '28579'],
    ['1467,3883,0', '28579'],
    ['1468,3884,0', '28579'],
    ['1470,3886,0', '28580'],
    ['1469,3885,0', '28580']
]

actions = [
    ['1473,3885,0', '28580', '28582'],
    ['1473,3885,0', '28582', '28584'],
    ['1473,3885,0', '28584', '28586'],
    ['1471,3886,0', '28579', '28581'],
    ['1471,3886,0', '28581', '28583'],
    ['1471,3886,0', '28583', '28585'],
    ['1467,3883,0', '28579', '28581'],
    ['1468,3884,0', '28579', '28581'],
    ['1467,3883,0', '28581', '28583'],
    ['1468,3884,0', '28581', '28583'],
    ['1467,3883,0', '28583', '28585'],
    ['1468,3884,0', '28583', '28585'],
    ['1470,3886,0', '28580', '28582'],
    ['1469,3885,0', '28580', '28582'],
    ['1470,3886,0', '28582', '28584'],
    ['1469,3885,0', '28582', '28584'],
    ['1470,3886,0', '28584', '28586'],
    ['1469,3885,0', '28584', '28586'],
]

ore_varbits = [
    '4924', # coal
    '4925', # gold
    '4926', # mith
    '4921', # addy
    '4922' # rune
]

noted_ores_id = [
    '445', # gold
    '448', # mith
    '450', # addy
    '452', # rune
    '454', # coal
]

keyboard = Controller()


def drink_stam():
    run_energy = osrs.server.get_widget('160,28', port)
    if run_energy and int(run_energy['text']) < 45:
        inv = osrs.inv.get_inv(port, True)
        stam = osrs.inv.are_items_in_inventory_v2(inv, [12631, 12629, 12627, 12625])
        if stam:
            osrs.move.move_and_click(stam['x'], stam['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.1)
        else:
            while True:
                bank_chest = osrs.server.get_game_object('1476,3877,0', '28595', port)
                if bank_chest:
                    osrs.move.move_and_click(bank_chest['x'], bank_chest['y'], 3, 3)
                    osrs.bank.wait_for_bank_interface(port)
                    bank_data = osrs.bank.get_bank_data(port)
                    stam_in_bank = osrs.inv.are_items_in_inventory_v2(bank_data, [12631, 12629, 12627, 12625])
                    if not stam_in_bank:
                        exit('no more stams')
                    osrs.move.move_and_click(stam_in_bank['x'], stam_in_bank['y'], 3, 3)
                    osrs.clock.sleep_one_tick()
                    keyboard.press(Key.esc)
                    keyboard.release(Key.esc)
                    drink_stam()


def bank_v2():
    drink_stam()
    inv = osrs.inv.get_inv(port)
    dyna = osrs.inv.get_item_quantity_in_inv(inv, 13573)
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    if dyna < 6:
        while True:
            co = osrs.server.get_chat_options(port)
            if co:
                osrs.keeb.keyboard.type('1')
                osrs.clock.sleep_one_tick()
                return
            bank_chest = osrs.server.get_game_object('1476,3877,0', '28595', port)
            if bank_chest and (datetime.datetime.now() - last_click).total_seconds() > 8:
                noted_dyna = osrs.inv.is_item_in_inventory_v2(inv, 13574)
                if not noted_dyna:
                    exit('out of dyna')
                osrs.move.move_and_click(noted_dyna['x'], noted_dyna['y'], 3, 3)
                osrs.move.move_and_click(bank_chest['x'], bank_chest['y'], 3, 3)
                last_click = datetime.datetime.now()


def deposit():
    while True:
        sack = osrs.server.get_ground_object('1478,3874,0', '28592', port)
        if sack:
            osrs.move.move_and_click(sack['x'], sack['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                inv = osrs.inv.get_inv(port)
                ore = osrs.inv.is_item_in_inventory_v2(inv, 13575)
                if not ore:
                    # finish animation
                    osrs.clock.sleep_one_tick()
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 10:
                    break


def do_action_v3(tile, obj, next_obj):
    print('in do action with vars {}, {}, {}'.format(tile, obj, next_obj))
    start_time = datetime.datetime.now()
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        next_expected = osrs.server.get_game_object(tile, next_obj, port)
        if next_expected:
            return True
        spot = osrs.server.get_game_object(tile, obj, port)
        if spot and (datetime.datetime.now() - last_click).total_seconds() > 5:
            osrs.move.move_and_click(spot['x'], spot['y'], 3, 3)
            last_click = datetime.datetime.now()
        elif (datetime.datetime.now() - start_time).total_seconds() > 35:
            return False
        osrs.clock.random_sleep(0.1, 0.2)


def verify_rocks_ready_to_blast():
    start_time = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - start_time).total_seconds() > 30:
            return False
        failed_state = False
        for state in states:
            spot = osrs.server.get_game_object(state[0], state[1], port)
            if not spot:
                failed_state = True
                break
        if failed_state:
            continue
        else:
            return True


def hop_reset():
    for world in world_list:
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        keyboard.type('::hop {}'.format(world))
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        osrs.clock.random_sleep(20, 25)
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        empty_world = verify_rocks_ready_to_blast()
        if empty_world:
            return


def blast_ore():
    for action in actions:
        result = do_action_v3(*action)
        if not result:
            hop_reset()
            return
    osrs.move.spam_click('1468,3883,0', 2.5)  # pick up 3 and 4
    osrs.clock.sleep_one_tick()
    osrs.clock.sleep_one_tick()
    osrs.move.spam_click('1470,3885,0', 2.5)  # pick up 5 and 6
    osrs.move.spam_click('1471,3885,0', 1.2)  # pick up 2
    osrs.move.spam_click('1473,3884,0', 1.2)  # pick up 1
    osrs.clock.sleep_one_tick()


def collect_ore():
    for ore in ore_varbits:
        ore_count = osrs.server.get_varbit_value(ore)
        if ore_count and int(ore_count) > 450:
            # move my viewpoint up so i can see tiles to move to
            osrs.keeb.keyboard.press(Key.up)
            osrs.clock.random_sleep(2, 3)
            osrs.keeb.keyboard.release(Key.up)
            # click the operator to get my ore
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
            while True:
                operator = osrs.server.get_npc_by_id('7072')
                inv = osrs.inv.get_inv()
                if inv and osrs.inv.is_item_in_inventory_v2(inv, noted_mith_id):
                    break
                elif operator and (datetime.datetime.now() - last_click).total_seconds() > 8:
                    osrs.move.move_and_click(operator['x'], operator['y'], 2, 2)
                    last_click = datetime.datetime.now()
                elif not operator:
                    osrs.move.run_towards_square_v2({'x': 1499, 'y': 3863, 'z': 0})
            # bank my ore
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
            while True:
                bank_chest = osrs.server.get_game_object('1476,3877,0', '28595', port)
                bank_portal = osrs.server.get_widget('12,1')
                if bank_chest and (datetime.datetime.now() - last_click).total_seconds() > 8:
                    osrs.move.move_and_click(bank_chest['x'], bank_chest['y'], 3, 3)
                    last_click = datetime.datetime.now()
                elif bank_portal:
                    break
                elif not bank_chest:
                    osrs.move.run_towards_square_v2({'x': 1479, 'y': 3880, 'z': 0})
            inv = osrs.inv.get_inv()
            if inv:
                for noted_ore in noted_ores_id:
                    found_ore = osrs.inv.is_item_in_inventory_v2(inv, noted_ore)
                    if found_ore:
                        osrs.move.right_click_menu_select(found_ore, None, '56799', )

            osrs.keeb.keyboard.press(Key.down)
            osrs.clock.random_sleep(2, 3)
            osrs.keeb.keyboard.release(Key.down)
            return


def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 49, 54, 432, 673, 'julenth')
        osrs.server.set_yaw(random.randint(300, 325), port)
        osrs.clock.sleep_one_tick()
        blast_ore()
        osrs.server.set_yaw(random.randint(800, 825), port)
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()
        deposit()
        collect_ore()
        bank_v2()


main()
'''inv = osrs.inv.get_inv()
t = osrs.inv.is_item_in_inventory_v2(inv, '448')
osrs.move.right_click_menu_select_v2(t, 'Drop')'''