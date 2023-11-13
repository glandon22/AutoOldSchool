import datetime

import osrs

POT = 91 # guam unf
SECONDARY = 221 # eye newt


def open_bank_interface(qh: osrs.queryHelper.QueryHelper):
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        bank_data = qh.get_bank()
        if bank_data:
            return
        elif (datetime.datetime.now() - last_click).total_seconds() > 7:
            closest = osrs.util.find_closest_target(qh.get_npcs())
            if not closest:
                continue
            osrs.move.click(closest)
            last_click = datetime.datetime.now()


def dump_inventory_in_bank():
    q = {
        'dumpInvButton': True
    }
    while True:
        data = osrs.server.query_game_data(q)
        if 'dumpInvButton' in data:
            # wait for button to settle on screen
            osrs.clock.sleep_one_tick()
            data = osrs.server.query_game_data(q)
            if 'dumpInvButton' in data:
                center = data['dumpInvButton']
                osrs.move.move_and_click(center['x'], center['y'], 10, 10)
                osrs.clock.random_sleep(.5, .6)
                break


def withdraw_materials():
    found_pot = False
    found_secondary = False
    data = osrs.bank.get_bank_data()
    pot = osrs.inv.is_item_in_inventory_v2(data, POT)
    if not pot:
        exit(' out of pots')
    osrs.move.move_and_click(pot['x'], pot['y'], 3, 3)
    sec = osrs.inv.is_item_in_inventory_v2(data, SECONDARY)
    if not sec:
        exit('out of secondaries')
    osrs.move.move_and_click(sec['x'], sec['y'], 3, 3)
    osrs.keeb.press_key('esc')
    osrs.clock.random_sleep(0.9, 1.1)


def make_pot():
    inv = osrs.inv.get_inv()
    pot = osrs.inv.is_item_in_inventory_v2(inv, POT)
    osrs.move.move_and_click(pot['x'], pot['y'], 3, 3)
    secondary = osrs.inv.is_item_in_inventory_v2(inv, SECONDARY)
    osrs.move.move_and_click(secondary['x'], secondary['y'], 3, 3)
    osrs.clock.random_sleep(.9, 1.2)
    osrs.keeb.keyboard.type(' ')
    osrs.clock.random_sleep(0.3, 0.4)
    osrs.move.click_off_screen(click=False)


def withdraw_materials_v2(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    if not qh.get_bank():
        return
    pot = qh.get_bank(POT)
    secondary_ingredient = qh.get_bank(SECONDARY)
    if not pot:
        exit('out of pot')
    if not secondary_ingredient:
        exit('out secondary_ingredient uns')
    osrs.move.click(pot)
    osrs.move.click(secondary_ingredient)
    osrs.keeb.keyboard.press(osrs.keeb.key.esc)
    osrs.keeb.keyboard.release(osrs.keeb.key.esc)
    start_time = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_inventory(POT) and qh.get_inventory(SECONDARY):
            break
        elif (datetime.datetime.now() - start_time).total_seconds() > 5:
            break


bankers_ids = [
    '1633',
    '1613',
    '1634',
    '3089'
]

script_config = {
    'intensity': 'high',
    'login': False,
    'logout': False
}


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_bank()
    qh.set_widgets({'233,0', '270,14'})
    qh.set_npcs(bankers_ids)
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        updated_config = osrs.game.break_manager_v3(script_config)
        inv = osrs.inv.get_inv()
        leveled_up_widget = osrs.server.get_widget('233,0')
        have_pot = osrs.inv.is_item_in_inventory_v2(inv, POT)
        have_sec = osrs.inv.is_item_in_inventory_v2(inv, SECONDARY)
        if not have_sec or not have_pot:
            osrs.server.post_game_status('Out of supplies, opening bank.', updated_config)
            open_bank_interface(qh)
            osrs.server.post_game_status('Dumping inventory in bank.', updated_config)
            osrs.bank.dump_items()
            osrs.server.post_game_status('Withdrawing materials from bank.', updated_config)
            withdraw_materials_v2(qh)
        elif leveled_up_widget or (datetime.datetime.now() - last_click).total_seconds() > 18:
            make_pot()
            last_click = datetime.datetime.now()

main()
