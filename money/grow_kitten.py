import datetime

import osrs


last_feed = datetime.datetime.now() - datetime.timedelta(hours=1)
last_play = datetime.datetime.now() - datetime.timedelta(hours=1)
qh = osrs.queryHelper.QueryHelper()
qh.set_npcs(['5593'])
qh.set_inventory()
qh.set_chat_options()
qh.set_canvas()
while True:
    osrs.game.break_manager_v4({
        'intensity': 'low',
        'login': False,
        'logout': False
    })
    qh.query_backend()
    osrs.keeb.press_key('f1')
    osrs.keeb.press_key('esc')
    if (datetime.datetime.now() - last_feed).total_seconds() > 23 * 60:
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.RAW_BASS.value))
        osrs.move.click(qh.get_npcs()[0])
        last_feed = datetime.datetime.now()
    elif (datetime.datetime.now() - last_play).total_seconds() > 24 * 60 and qh.get_npcs():
        res = osrs.move.right_click_v6(
            qh.get_npcs()[0],
            'Interact',
            qh.get_canvas(),
            in_inv=True
        )
        if res:
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            osrs.keeb.write('1')
            last_play = datetime.datetime.now()
    osrs.clock.random_sleep(10, 10.1)