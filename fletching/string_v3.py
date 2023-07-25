import datetime

import osrs

bankers_ids = [
    '1633',
    '1613',
    '1634',
    '3089'
]
BOWSTRING = 1777
# 66 yew long
# 70 mage long
# 62 maple long
# 64 maple short
UNSTRUNG_BOW = 70


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


def withdraw_materials_v2(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    if not qh.get_bank():
        return
    bstring = qh.get_bank(BOWSTRING)
    uns = qh.get_bank(UNSTRUNG_BOW)
    if not bstring:
        exit('out of bstring')
    if not uns:
        exit('out of uns')
    osrs.move.click(bstring)
    osrs.move.click(uns)
    osrs.keeb.keyboard.press(osrs.keeb.key.esc)
    osrs.keeb.keyboard.release(osrs.keeb.key.esc)
    osrs.clock.sleep_one_tick()


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
        osrs.game.break_manager_v3(script_config)
        qh.query_backend()
        bstring = qh.get_inventory(BOWSTRING)
        bow = qh.get_inventory(UNSTRUNG_BOW)
        if not bow or not bstring:
            open_bank_interface(qh)
            osrs.bank.dump_items()
            withdraw_materials_v2(qh)
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
        elif bstring and bow and (datetime.datetime.now() - last_click).total_seconds() > 25:
            osrs.move.click(bstring)
            osrs.move.click(bow)
            wait_time = datetime.datetime.now()
            while True:
                qh.query_backend()
                if qh.get_widgets('270,14'):
                    osrs.keeb.keyboard.press(osrs.keeb.key.space)
                    osrs.keeb.keyboard.release(osrs.keeb.key.space)
                    last_click = datetime.datetime.now()
                    break
                elif (datetime.datetime.now() - wait_time).total_seconds() > 4:
                    break
        elif qh.get_widgets('233,0'):
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)

main()
