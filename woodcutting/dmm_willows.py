import datetime

import osrs

wc_animations = [
    879,877,875,873,871,869,867,8303,2846,24,2117,7264,8324,8778
]


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_animation()
    qh.set_objects(
        {'3234,3244,0', '3235,3238,0', '2391,3429,0', '2392,3424,0', '2396,3419,0'},
        {'10819'},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    fletching = None
    while True:
        qh.query_backend()
        if fletching:
            if not qh.get_inventory(osrs.item_ids.ItemIDs.WILLOW_LOGS.value) or (datetime.datetime.now() - fletching).total_seconds() > 60:
                fletching = None
        elif len(qh.get_inventory()) == 28:
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.KNIFE.value))
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.WILLOW_LOGS.value))
            osrs.clock.sleep_one_tick()
            osrs.keeb.write('1')
            fletching = datetime.datetime.now()
        elif qh.get_player_animation() not in wc_animations and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, '10819'):
            osrs.game.break_manager_v4({
                'login': False,
                'logout': False,
                'intensity': 'low'
            })
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, '10819')[0])


main()