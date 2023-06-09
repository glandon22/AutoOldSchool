import datetime
import osrs

import osrs
import base64
import keyboard
port = '56799'
knife_id = 946

def determine_log(lvl):
    if lvl < 20:
        return 1511  # logs
    elif lvl < 35:
        return 1521  # oak logs
    elif lvl < 50:
        return 1519  # willow logs
    elif lvl < 55:
        return 1517  # maple logs
    else:
        return None


def determine_button(lvl):
    if lvl < 5:
        return '1'  # arrow shafts
    elif lvl < 10:
        return '3'  # shortbow
    elif lvl < 20:
        return '4'  # longbow
    elif lvl < 25:
        return '2'  # shortbow
    elif lvl < 35:
        return '3'  # longbow
    elif lvl < 40:
        return '2'  # shortbow
    elif lvl < 50:
        return '3'  # longbow
    elif lvl < 55:
        return '2'  # shortbow
    else:
        return None

def fletch(log, lvl):
    inv = osrs.inv.get_inv(port)
    knife = osrs.inv.is_item_in_inventory_v2(inv, knife_id)
    osrs.move.move_and_click(knife['x'], knife['y'], 3, 4)
    osrs.clock.random_sleep(0.5, 0.6)
    log_in_inv = osrs.inv.is_item_in_inventory_v2(inv, log)
    osrs.move.move_and_click(log_in_inv['x'], log_in_inv['y'], 4, 4)
    osrs.clock.random_sleep(0.9, 1)
    button = determine_button(lvl)
    keyboard.send(button)

def bank(log):
    osrs.bank.click_banker(port)
    osrs.bank.wait_for_bank_interface(port)
    osrs.bank.deposit_all_but_x_in_bank([knife_id], port)
    bank = osrs.bank.get_bank_data(port)
    log_to_withdraw = osrs.inv.is_item_in_inventory_v2(bank, log)
    print('33333', log_to_withdraw)
    osrs.move.move_and_click(log_to_withdraw['x'], log_to_withdraw['y'], 3, 3)
    osrs.clock.random_sleep(0.5, 0.6)

def main():
    osrs.clock.random_sleep(5, 6)
    # do some checking to make sure my inv is changing, if not, start fletching again
    prev_inv_hash = '1'
    inv_updated = datetime.datetime.now()
    while True:
        fletching_level = osrs.server.get_skill_data('fletching', port)
        log = determine_log(fletching_level['level'])
        inv = osrs.inv.get_inv(port)
        inv_hash = base64.b64encode(str(inv).encode('ascii'))
        have_more_logs = osrs.inv.is_item_in_inventory_v2(inv, log)
        have_leveled = osrs.server.have_leveled_up(port)
        if not have_more_logs:
            bank(log)
            fletch(log, fletching_level['level'])
        elif have_leveled:
            fletch(log, fletching_level['level'])
        elif inv_hash == prev_inv_hash and (datetime.datetime.now() - inv_updated).total_seconds() > 5:
            fletch(log, fletching_level['level'])
            inv_updated = datetime.datetime.now()
            osrs.clock.random_sleep(1, 1.2)
        elif inv_hash != prev_inv_hash:
            prev_inv_hash = inv_hash
            inv_updated = datetime.datetime.now()
main()