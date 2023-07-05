import datetime

import osrs

POT = 99
SECONDARY = 231


def click_banker():
    q = {
        'npcs': ['Banker']
    }
    data = osrs.server.query_game_data(q)
    if len(data["npcs"]) != 0:
        closest = osrs.util.find_closest_npc(data['npcs'])
        osrs.move.move_and_click(closest['x'], closest['y'], 5, 6)


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


def main():
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        inv = osrs.inv.get_inv()
        leveled_up_widget = osrs.server.get_widget('233,0')
        have_pot = osrs.inv.is_item_in_inventory_v2(inv, POT)
        have_sec = osrs.inv.is_item_in_inventory_v2(inv, SECONDARY)
        if not have_sec or not have_pot:
            click_banker()
            dump_inventory_in_bank()
            withdraw_materials()
        elif leveled_up_widget or (datetime.datetime.now() - last_click).total_seconds() > 18:
            make_pot()
            last_click = datetime.datetime.now()

main()
