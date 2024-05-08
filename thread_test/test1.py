import datetime

import osrs



def hop_logic():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'2471,9789,0'})
    qh.set_player_world_location()
    last_off_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') != 2471 \
                or qh.get_player_world_location('y') != 9789:
            last_off_tile = datetime.datetime.now()
            if qh.get_tiles('2471,9789,0'):
                osrs.move.fast_click(qh.get_tiles('2471,9789,0'))

        if qh.get_player_world_location('x') == 2471 \
                and qh.get_player_world_location('y') == 9789:
            osrs.player.turn_off_all_prayers()
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 11:
                return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2471, 'y': 9789, 'z': 0})


hop_logic()