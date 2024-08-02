import datetime

import osrs
food = osrs.item_ids.ItemIDs.RAW_SALMON.value
cook_widget = '270,14'
range_id = 17131


def main():
    last_change = datetime.datetime.now()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({cook_widget})
    qh.set_objects_v2('game', {range_id})
    qh.set_skills({'cooking'})
    last_inv = None
    while True:
        qh.query_backend()
        if qh.get_skills('cooking') and qh.get_skills('cooking')['level'] == 99:
            exit(99)
        if not qh.get_inventory(food):
            osrs.game.break_manager_v4({
                'intensity': 'low',
                'login': False,
                'logout': False
            })
            osrs.move.go_to_loc(2442, 3488, 1)
            osrs.bank.banking_handler({
                'dump_inv': True,
                'withdraw': [{'items': [
                    food
                ]}]
            })
            osrs.clock.sleep_one_tick()
            last_change = datetime.datetime.now() - datetime.timedelta(hours=1)
        elif qh.get_inventory() != last_inv:
            last_inv = qh.get_inventory()
            last_change = datetime.datetime.now()
        elif (datetime.datetime.now() - last_change).total_seconds() > 3:
            if qh.get_widgets(cook_widget):
                osrs.keeb.press_key('space')
                osrs.clock.random_sleep(1, 1.1)
            elif qh.get_objects_v2('game', range_id):
                osrs.move.fast_click(qh.get_objects_v2('game', range_id)[0])
            else:
                osrs.move.go_to_loc(2450, 3510,1)


main()