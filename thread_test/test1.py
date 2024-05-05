import osrs


def frem_dungeon_turoth():
    dungeon_entrance_id = '2123'
    shortcut_2_id = '16539'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'2797,3614,0'},
        {dungeon_entrance_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_objects(
        {'2734,10008,0'},
        {shortcut_2_id},
        osrs.queryHelper.ObjectTypes.WALL.value
    )
    qh.set_tiles({'2774,10003,0', '2769,10002,0'})
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('y') > 9000:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dungeon_entrance_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dungeon_entrance_id)[0])
            osrs.clock.random_sleep(1, 1.1)
    print('passing first stage of shortcut 1')
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') <= 2769:
            break
        elif qh.get_tiles('2774,10003,0') and qh.get_player_world_location('x') >= 2775:
            osrs.move.fast_click(qh.get_tiles('2774,10003,0'))
        elif qh.get_tiles('2769,10002,0') and 2773 >= qh.get_player_world_location('x') >= 2770:
            osrs.move.fast_click(qh.get_tiles('2769,10002,0'))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2775, 'y': 10003, 'z': 0})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') <= 2731:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, shortcut_2_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, shortcut_2_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2737, 'y': 10007, 'z': 0})

frem_dungeon_turoth()


