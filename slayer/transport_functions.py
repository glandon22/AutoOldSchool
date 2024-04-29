import osrs


def isle_of_souls_dungeon():
    dungeon_entrance_id = '40736'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'2309,2918,0'},
        {dungeon_entrance_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'2145,9296,0'})
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('y') > 5000:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dungeon_entrance_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dungeon_entrance_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2309, 'y': 2918, 'z': 0})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') == 2145 and qh.get_player_world_location('y') == 9296:
            return
        elif qh.get_tiles('2145,9296,0'):
            osrs.move.fast_click(qh.get_tiles('2145,9296,0'))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2145, 'y': 9296, 'z': 0})


def kalphite_layer():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'3320,3121,0'},
        {'30180'},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'3259,3096,0'})
    while True:
        qh.query_backend()
        while True:
            qh.query_backend()
            # I am in the dungeon
            if qh.get_player_world_location('y') > 5000:
                return
            elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, '30180'):
                osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, '30180')[0])
            else:
                if qh.get_tiles('3259,3096,0'):
                    osrs.move.fast_click(qh.get_tiles('3259,3096,0'))
                osrs.move.follow_path(qh.get_player_world_location(), {'x': 3320, 'y': 3121, 'z': 0})


def south_quidamortem_trolls():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_tiles({'1290,3493,0'})
    while True:
        qh.query_backend()
        while True:
            qh.query_backend()
            # I am in the dungeon
            if qh.get_player_world_location('x') < 1235:
                return
            else:
                if qh.get_tiles('1290,3493,0'):
                    osrs.move.fast_click(qh.get_tiles('1290,3493,0'))
                osrs.move.follow_path(qh.get_player_world_location(), {'x': 1230, 'y': 3496, 'z': 0})
