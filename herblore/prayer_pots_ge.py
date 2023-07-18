import datetime

import osrs

POT = '99'
SECONDARY = '231'
bankers_ids = [
    '1633',
    '1613',
    '1634',
    '3089'
]
amulet_of_chem_id = '21163'


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


def withdraw_materials_v2(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    if not qh.get_bank():
        return
    have_chem = qh.get_equipment(amulet_of_chem_id)
    print(have_chem, qh.get_equipment())
    if not have_chem:
        chem = qh.get_bank(amulet_of_chem_id)
        if not chem:
            exit('out of amulets of chemistry')
        osrs.move.click(chem)
        osrs.clock.sleep_one_tick()
        osrs.keeb.keyboard.press(osrs.keeb.key.esc)
        osrs.keeb.keyboard.release(osrs.keeb.key.esc)
        osrs.clock.sleep_one_tick()
        qh.query_backend()
        chem_inv = qh.get_inventory(amulet_of_chem_id)
        osrs.move.click(chem_inv)
        open_bank_interface(qh)
        osrs.clock.sleep_one_tick()
    osrs.bank.dump_items()
    pot = qh.get_bank(POT)
    sec = qh.get_bank(SECONDARY)
    if not pot:
        exit('out of pots')
    if not sec:
        exit('out of secondaries')
    osrs.move.click(pot)
    osrs.move.click(sec)
    osrs.keeb.keyboard.press(osrs.keeb.key.esc)
    osrs.keeb.keyboard.release(osrs.keeb.key.esc)
    osrs.clock.sleep_one_tick()


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


script_config = osrs.game.ScriptConfiguration(
    osrs.game.ScriptConfiguration.low,
    None,
    None
)


def main():
    global last_click
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.game.break_manager_v3(script_config.config)
        qh = osrs.queryHelper.QueryHelper()
        qh.set_inventory()
        qh.set_npcs(bankers_ids)
        qh.set_bank()
        qh.set_widgets({'233,0', '270,5'})
        qh.set_equipment()
        qh.query_backend()
        pot = qh.get_inventory(POT)
        sec = qh.get_inventory(SECONDARY)
        if not pot or not sec:
            osrs.keeb.keyboard.press(osrs.keeb.key.f4)
            osrs.keeb.keyboard.release(osrs.keeb.key.f4)
            osrs.keeb.keyboard.press(osrs.keeb.key.esc)
            osrs.keeb.keyboard.release(osrs.keeb.key.esc)
            open_bank_interface(qh)
            withdraw_materials_v2(qh)
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
        elif pot and sec and ((datetime.datetime.now() - last_click).total_seconds() > 30 or qh.get_widgets('233,0')):
            osrs.move.click(pot)
            osrs.move.click(sec)
            wait_time = datetime.datetime.now()
            while True:
                qh.query_backend()
                if (datetime.datetime.now() - wait_time).total_seconds() > 5:
                    break
                elif qh.get_widgets('270,5'):
                    osrs.keeb.keyboard.press(osrs.keeb.key.space)
                    osrs.keeb.keyboard.release(osrs.keeb.key.space)
                    break
            last_click = datetime.datetime.now()



main()
