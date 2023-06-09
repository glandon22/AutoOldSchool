import datetime
import random
from pynput.keyboard import Key, Controller

import osrs

# 13573 dynamite
# does not handle leveling yet
port = '56799'

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


def bank():
    drink_stam()
    inv = osrs.inv.get_inv(port)
    dyna = osrs.inv.get_item_quantity_in_inv(inv, 13573)
    if dyna < 6:
        while True:
            bank_chest = osrs.server.get_game_object('1476,3877,0', '28595', port)
            if bank_chest:
                noted_dyna = osrs.inv.is_item_in_inventory_v2(inv, 13574)
                if not noted_dyna:
                    exit('out of dyna')
                osrs.move.move_and_click(noted_dyna['x'], noted_dyna['y'], 3, 3)
                osrs.move.move_and_click(bank_chest['x'], bank_chest['y'], 3, 3)
                if str(osrs.server.get_target_obj(port)) == '28595':
                    break
        while True:
            co = osrs.server.get_chat_options(port)
            if co:
                osrs.keeb.keyboard.type('1')
                osrs.clock.sleep_one_tick()
                return


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


def do_action(tile, obj, next_obj):
    while True:
        spot = osrs.server.get_game_object(tile, obj, port)
        if spot:
            osrs.move.move_and_click(spot['x'], spot['y'], 3, 3)
            break
    while True:
        next_expected = osrs.server.get_game_object(tile, next_obj, port)
        if next_expected:
            break


def do_action_v2(tile, obj, next_obj):
    while True:
        spot = osrs.server.get_game_object(tile, obj, port)
        if spot:
            osrs.move.move_and_click(spot['x'], spot['y'], 3, 3)
            if str(osrs.server.get_target_obj(port)) == obj:
                break
        osrs.clock.random_sleep(0.1, 0.2)
    while True:
        next_expected = osrs.server.get_game_object(tile, next_obj, port)
        if next_expected:
            break
        osrs.clock.random_sleep(0.1, 0.2)


def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 53, 59, 432, 673, 'julenth')
        osrs.server.set_yaw(random.randint(300, 325), port)
        osrs.clock.sleep_one_tick()

        do_action_v2('1473,3885,0', '28580', '28582')  # chisel 1
        do_action_v2('1473,3885,0', '28582', '28584')  # dyna 1
        do_action_v2('1473,3885,0', '28584', '28586')  # blow up 1

        do_action_v2('1471,3886,0', '28579', '28581')  # chisel 2
        do_action_v2('1471,3886,0', '28581', '28583')  # dyna 2
        do_action_v2('1471,3886,0', '28583', '28585')  # blow up 2

        do_action_v2('1467,3883,0', '28579', '28581')  # chisel 3
        do_action_v2('1468,3884,0', '28579', '28581')  # chisel 4

        do_action_v2('1467,3883,0', '28581', '28583')  # dyna 3
        do_action_v2('1468,3884,0', '28581', '28583')  # dyna 4

        do_action_v2('1467,3883,0', '28583', '28585')  # blow up 3
        do_action_v2('1468,3884,0', '28583', '28585')  # blow up 4

        do_action_v2('1470,3886,0', '28580', '28582')  # chisel 5
        do_action_v2('1469,3885,0', '28580', '28582')  # chisel 6

        do_action_v2('1470,3886,0', '28582', '28584')  # dyna 5
        do_action_v2('1469,3885,0', '28582', '28584')  # dyna 6

        do_action_v2('1470,3886,0', '28584', '28586')  # blow up 5
        do_action_v2('1469,3885,0', '28584', '28586')  # blow up 6

        osrs.move.spam_click('1468,3883,0', 2.5)  # pick up 3 and 4
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()
        osrs.move.spam_click('1470,3885,0', 2.5)  # pick up 5 and 6
        osrs.move.spam_click('1471,3885,0', 1.2)  # pick up 2
        osrs.move.spam_click('1473,3884,0', 1.2)  # pick up 1
        osrs.clock.sleep_one_tick()

        osrs.server.set_yaw(random.randint(800, 825), port)
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()

        deposit()
        bank()


main()
