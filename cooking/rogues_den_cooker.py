import datetime

import osrs

banker_id = '3194'
cook_widget = '270,13'
fish_id = '3142'
fire_id = '43475'

def bank(qh: osrs.queryHelper.QueryHelper):
    last_bank_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        banker = qh.get_npcs()
        if banker and (datetime.datetime.now() - last_bank_click).total_seconds() > 5:
            osrs.move.click(banker[0])
            last_bank_click = datetime.datetime.now()
        elif qh.get_bank():
            print('here')
            break
    osrs.bank.dump_items()
    qh.query_backend()
    if not qh.get_bank(fish_id):
        exit('no fish')
    osrs.move.click(qh.get_bank(fish_id))
    osrs.keeb.press_key('esc')


def cook_fish(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    osrs.move.click(qh.get_game_objects(fire_id)[0])
    while True:
        qh.query_backend()
        if qh.get_widgets(cook_widget):
            osrs.keeb.write('2')
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            break


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([banker_id])
    qh.set_inventory()
    qh.set_bank()
    qh.set_widgets({cook_widget})
    qh.set_game_objects(
        {'3043,4973,1'},
        {fire_id}
    )
    while True:
        qh.query_backend()
        if not qh.get_inventory(fish_id):
            bank(qh)
            cook_fish(qh)


main()
