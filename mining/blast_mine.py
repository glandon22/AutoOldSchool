import datetime
import random

from osrs_utils import general_utils
# 13573 dynamite
# does not handle leveling yet
port = '56799'


def bank():
    inv = general_utils.get_inv(port)
    dyna = general_utils.get_item_quantity_in_inv(inv, 13573)
    if dyna < 6:
        while True:
            bank_chest = general_utils.get_game_object('1476,3877,0', '28595', port)
            if bank_chest:
                noted_dyna = general_utils.is_item_in_inventory_v2(inv, 13574)
                if not noted_dyna:
                    exit('out of dyna')
                general_utils.move_and_click(noted_dyna['x'], noted_dyna['y'], 3, 3)
                general_utils.move_and_click(bank_chest['x'], bank_chest['y'], 3, 3)
                while True:
                    co = general_utils.get_chat_options(port)
                    if co:
                        general_utils.type_something('1')
                        general_utils.sleep_one_tick()
                        return

def deposit():
    while True:
        sack = general_utils.get_ground_object('1478,3874,0', '28592', port)
        if sack:
            general_utils.move_and_click(sack['x'], sack['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                inv = general_utils.get_inv(port)
                ore = general_utils.is_item_in_inventory_v2(inv, 13575)
                if not ore:
                    # finish animation
                    general_utils.sleep_one_tick()
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 10:
                    break


def do_action(tile, obj, next_obj):
    while True:
        spot = general_utils.get_game_object(tile, obj, port)
        if spot:
            general_utils.move_and_click(spot['x'], spot['y'], 3, 3)
            break
    while True:
        next = general_utils.get_game_object(tile, next_obj, port)
        if next:
            break

# pick up 3 and 4 ore

def main():
    while True:
        general_utils.set_yaw(random.randint(300, 325), port)
        general_utils.sleep_one_tick()

        do_action('1473,3885,0', '28580', '28582')  # chisel 1
        do_action('1473,3885,0', '28582', '28584')  # dyna 1
        do_action('1473,3885,0', '28584', '28586')  # blow up 1

        do_action('1471,3886,0', '28579', '28581')  # chisel 2
        do_action('1471,3886,0', '28581', '28583')  # dyna 2
        do_action('1471,3886,0', '28583', '28585')  # blow up 2

        do_action('1467,3883,0', '28579', '28581')  # chisel 3
        do_action('1468,3884,0', '28579', '28581')  # chisel 4

        do_action('1467,3883,0', '28581', '28583')  # dyna 3
        do_action('1468,3884,0', '28581', '28583')  # dyna 4

        do_action('1467,3883,0', '28583', '28585')  # blow up 3
        do_action('1468,3884,0', '28583', '28585')  # blow up 4

        do_action('1470,3886,0', '28580', '28582')  # chisel 5
        do_action('1469,3885,0', '28580', '28582')  # chisel 6

        do_action('1470,3886,0', '28582', '28584')  # dyna 5
        do_action('1469,3885,0', '28582', '28584')  # dyna 6

        do_action('1470,3886,0', '28584', '28586')  # blow up 5
        do_action('1469,3885,0', '28584', '28586')  # blow up 6

        general_utils.spam_click('1468,3883,0', 2.5) # pick up 3 and 4
        general_utils.sleep_one_tick()
        general_utils.sleep_one_tick()
        general_utils.spam_click('1470,3885,0', 2.5) # pick up 5 and 6
        general_utils.spam_click('1471,3885,0', 1.2) # pick up 2
        general_utils.spam_click('1473,3884,0', 1.2) # pick up 1
        general_utils.sleep_one_tick()

        general_utils.set_yaw(random.randint(800, 825), port)
        general_utils.sleep_one_tick()
        general_utils.sleep_one_tick()

        deposit()
        bank()

# yaw 300 - 325to mine
# yaw 800 - 825 to deposit

main()

