import osrs
from osrs.item_ids import ItemIDs


def nieve():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_tiles({'2868,9827,1'})
    qh.set_npcs_by_name(['nieve'])
    qh.set_slayer()
    print('running to wall')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_slayer():
            return
        elif qh.get_npcs_by_name():
            c = osrs.util.find_closest_target(qh.get_npcs_by_name())
            if c:
                osrs.move.fast_click(c)
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2435, 'y': 3423, 'z': 0})


def isle_of_souls_dungeon(x=2145, y=9296):
    dungeon_entrance_id = '40736'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'2309,2918,0'},
        {dungeon_entrance_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({f'{x},{y},0'})
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
        if qh.get_player_world_location('x') == x and qh.get_player_world_location('y') == y:
            return
        elif qh.get_tiles(f'{x},{y},0'):
            osrs.move.fast_click(qh.get_tiles(f'{x},{y},0'))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': x, 'y': y, 'z': 0})


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


def taverley_dungeon():
    rock_steps_id = '30189'
    rock_steps_tile = '2882,9825,0'
    crumbled_wall_id = '24222'
    crumbled_wall_tile = '2935,3355,0'
    ladder_id = '16680'
    ladder_tile = '2884,3397,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {crumbled_wall_tile, ladder_tile, rock_steps_tile},
        {crumbled_wall_id, ladder_id, rock_steps_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'2868,9827,1'})
    print('running to wall')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('x') <= 2935:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, crumbled_wall_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, crumbled_wall_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2936, 'y': 3355, 'z': 0})
    print('running to ladder')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('y') > 9000:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2884, 'y': 3396, 'z': 0})
    print('running to steps')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('z') == 1:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, rock_steps_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, rock_steps_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2884, 'y': 9825, 'z': 0})
    print('running to bridge')
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') == 2868 and qh.get_player_world_location('y') == 9827:
            return
        elif qh.get_tiles('2868,9827,1'):
            osrs.move.fast_click(qh.get_tiles('2868,9827,1'))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2868, 'y': 9827, 'z': 1})


def waterbirth_dungeon():
    cave_entrance_tile = '2522,3738,0'
    cave_entrance_id = '8929'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {cave_entrance_tile},
        {cave_entrance_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') > 9000:
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, cave_entrance_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, cave_entrance_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2526, 'y': 3739, 'z': 0})


def taverley_dungeon_hellhounds():
    shortcut_id = '16510'
    shortcut_tile = '2879,9813,0'
    crumbled_wall_id = '24222'
    crumbled_wall_tile = '2935,3355,0'
    ladder_id = '16680'
    ladder_tile = '2884,3397,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {crumbled_wall_tile, ladder_tile, shortcut_tile},
        {crumbled_wall_id, ladder_id, shortcut_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'2868,9827,1'})
    print('running to wall')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('x') <= 2935:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, crumbled_wall_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, crumbled_wall_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2936, 'y': 3355, 'z': 0})
    print('running to ladder')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('y') > 9000:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2884, 'y': 3396, 'z': 0})
    print('running to steps')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('x') < 2878:
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, shortcut_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, shortcut_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2882, 'y': 9813, 'z': 0})


def taverley_dungeon_black_demons():
    shortcut_id = '16509'
    shortcut_tile = '2887,9799,0'
    crumbled_wall_id = '24222'
    crumbled_wall_tile = '2935,3355,0'
    ladder_id = '16680'
    ladder_tile = '2884,3397,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {crumbled_wall_tile, ladder_tile, shortcut_tile},
        {crumbled_wall_id, ladder_id, shortcut_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'2868,9773,0'})
    print('running to wall')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('x') <= 2935:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, crumbled_wall_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, crumbled_wall_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2936, 'y': 3355, 'z': 0})
    print('running to ladder')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('y') > 9000:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2884, 'y': 3396, 'z': 0})
    print('running to pipe')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('x') >= 2892:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, shortcut_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, shortcut_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2890, 'y': 9799, 'z': 0})
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_tiles('2868,9773,0'):
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2868, 'y': 9773, 'z': 0})


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
        if qh.get_player_world_location('x') == 2730:
            # sleep for a second to finish shortcut animation
            osrs.clock.random_sleep(2, 2.1)
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, shortcut_2_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, shortcut_2_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2737, 'y': 10007, 'z': 0})


def stronghold_slayer_dungeon_bloodvelds():
    dungeon_entrance_id = '26709'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_slayer()
    qh.set_inventory()
    qh.set_chat_options()
    qh.set_player_world_location()
    qh.set_objects(
        {'2429,3425,0'},
        {dungeon_entrance_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    while True:
        qh.query_backend()
        slayer_ring = qh.get_inventory([
            ItemIDs.SLAYER_RING_1.value,
            ItemIDs.SLAYER_RING_2.value,
            ItemIDs.SLAYER_RING_3.value,
            ItemIDs.SLAYER_RING_4.value,
            ItemIDs.SLAYER_RING_5.value,
            ItemIDs.SLAYER_RING_6.value,
            ItemIDs.SLAYER_RING_7.value,
            ItemIDs.SLAYER_RING_8.value,
        ])
        if not slayer_ring:
            return print('need new task, no slayer ring in inv')
        if osrs.move.right_click_v3(slayer_ring, 'Rub'):
            osrs.clock.sleep_one_tick()
            osrs.keeb.write('1')
            osrs.clock.sleep_one_tick()
            osrs.keeb.write('1')
            break
    while True:
        qh.query_backend()
        dungeon = qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                dungeon_entrance_id
        )
        if dungeon:
            osrs.move.fast_click(dungeon[0])
            osrs.clock.sleep_one_tick()
        elif qh.get_player_world_location('y') > 8000:
            break
    while True:
        qh.query_backend()
        if 2481 <= qh.get_player_world_location('x') <= 2494 and 9814 <= qh.get_player_world_location('y') <= 9832:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2488, 'y': 9823, 'z': 0})


def stronghold_slayer_dungeon_ankou():
    dungeon_entrance_id = '26709'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_slayer()
    qh.set_inventory()
    qh.set_chat_options()
    qh.set_player_world_location()
    qh.set_objects(
        {'2429,3425,0'},
        {dungeon_entrance_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    while True:
        qh.query_backend()
        slayer_ring = qh.get_inventory([
            ItemIDs.SLAYER_RING_1.value,
            ItemIDs.SLAYER_RING_2.value,
            ItemIDs.SLAYER_RING_3.value,
            ItemIDs.SLAYER_RING_4.value,
            ItemIDs.SLAYER_RING_5.value,
            ItemIDs.SLAYER_RING_6.value,
            ItemIDs.SLAYER_RING_7.value,
            ItemIDs.SLAYER_RING_8.value,
        ])
        if not slayer_ring:
            return print('need new task, no slayer ring in inv')
        if osrs.move.right_click_v3(slayer_ring, 'Rub'):
            osrs.clock.sleep_one_tick()
            osrs.keeb.write('1')
            osrs.clock.sleep_one_tick()
            osrs.keeb.write('1')
            break
    while True:
        qh.query_backend()
        dungeon = qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                dungeon_entrance_id
        )
        if dungeon:
            osrs.move.fast_click(dungeon[0])
            osrs.clock.sleep_one_tick()
        elif qh.get_player_world_location('y') > 8000:
            break
    while True:
        qh.query_backend()
        if 2474 <= qh.get_player_world_location('x') <= 2484 and 9797 <= qh.get_player_world_location('y') <= 9802:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2478, 'y': 9800, 'z': 0})

