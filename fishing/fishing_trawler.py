import datetime

import osrs


def start_game():
    boat_entry_ramp_id = '4977'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'2675,3170,0'},
        {boat_entry_ramp_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') > 4000:
            print(qh.get_player_world_location())
            return
        elif 2671 <= qh.get_player_world_location('x') <= 2673 and 3168 <= qh.get_player_world_location('y') <= 3172:
            print('on boat')
            continue
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, boat_entry_ramp_id):
            osrs.move.click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, boat_entry_ramp_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2676, 'y': 3167, 'z': 0})


def handle_game():
    ladder_to_deck_id = '4060'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name(['Enormous Tentacle'])
    seen_tent = False
    while True:
        qh.query_backend()
        tiles = osrs.util.generate_surrounding_tiles_from_point(10, qh.get_player_world_location())
        qh.clear_objects(osrs.queryHelper.ObjectTypes.GAME.value)
        qh.set_objects(
            set(tiles),
            {ladder_to_deck_id},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.query_backend()
        if qh.get_player_world_location('y') < 4500 and seen_tent:
            return
        elif qh.get_npcs_by_name() and qh.get_player_world_location('z') == 1:
            seen_tent = True
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_to_deck_id):
            ladder = qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_to_deck_id)[0]
            if qh.get_player_world_location('z') == 0:
                osrs.move.click(ladder)
                osrs.clock.sleep_one_tick()


def get_loot():
    net_id = '2483'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_widgets({'367,19'})
    qh.set_objects(
        {'2667,3167,0'},
        {net_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    # had a misclick here. might check to see if i get the fishing xp after getting loot
    # if so  i can use that to determine when  i have received my loot and can start next game
    last_net_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets('367,19'):
            wait_start = datetime.datetime.now()
            while True:
                qh.query_backend()
                if qh.get_widgets('367,19') and (datetime.datetime.now() - wait_start).total_seconds() > 2:
                    print('screen up two seconds')
                    osrs.move.click(qh.get_widgets('367,19'))
                    osrs.clock.sleep_one_tick()
                    return
                elif not qh.get_widgets('367,19'):
                    print('accidentally clicked out of screen')
                    break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, net_id) and (datetime.datetime.now() - last_net_click).total_seconds() > 5:
            osrs.move.click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, net_id)[0])
            last_net_click = datetime.datetime.now()


script_config = {
    'intensity': 'low',
    'login': lambda: osrs.clock.random_sleep(2, 3),
    'logout': lambda: osrs.clock.random_sleep(2, 3),
}


def main():
    while True:
        osrs.game.break_manager_v4(script_config)
        start_game()
        handle_game()
        get_loot()

main()