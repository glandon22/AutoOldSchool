import osrs


def start_game():
    boat_entry_ramp_id = '4977'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'2675,3170,0'},
        boat_entry_ramp_id,
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') < 2675 and qh.get_player_world_location('y') > 3165:
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, boat_entry_ramp_id):
            osrs.move.click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, boat_entry_ramp_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2676, 'y': 3167, 'z': 0})


def handle_game():
    ladder_to_deck_id = '4060'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name(['Enormous Tentacle'])
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
        if qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
            osrs.clock.sleep_one_tick()
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_to_deck_id):
            ladder = qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_to_deck_id)[0]
            if qh.get_player_world_location('x') > ladder['x_coord']:
                osrs.move.click(ladder)
                osrs.clock.sleep_one_tick()
        # games over
        elif qh.get_player_world_location('y') < 7500:
            return


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
    while True:
        qh.query_backend()
        if qh.get_widgets('367,19'):
            osrs.move.click(qh.get_widgets('367,19'))
            osrs.clock.sleep_one_tick()
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, net_id):
            osrs.move.click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, net_id)[0])


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
