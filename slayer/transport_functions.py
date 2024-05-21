import osrs
import osrs.move
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
            if qh.get_player_world_location('y') > 5000 and 3268 <= qh.get_player_world_location('x') <= 3348:
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
            osrs.clock.sleep_one_tick()
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
            osrs.clock.sleep_one_tick()
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


def mount_karuulm_wyrms():
    shortcut_1_id = '34397'
    shortcut_2_id = '34396'
    obstacle_1_id = '34544'
    gap_1_id = '34515'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'1324,3778,0', '1324,3788,0', '1302,10205,0', '1272,10174,0'},
        {shortcut_1_id, shortcut_2_id, obstacle_1_id, gap_1_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'1311,3807,0'})
    while True:
        qh.query_backend()
        s1 = qh.get_objects(
            osrs.queryHelper.ObjectTypes.GAME.value,
            shortcut_1_id
        )
        if qh.get_player_world_location('y') > 3778 and 1275 <= qh.get_player_world_location('x') <= 1350:
            break
        elif s1:
            osrs.move.fast_click(s1[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 1324, 'y': 3776, 'z': 0})
    while True:
        qh.query_backend()
        s2 = qh.get_objects(
            osrs.queryHelper.ObjectTypes.GAME.value,
            shortcut_2_id
        )
        if qh.get_player_world_location('y') > 3788 and 1275 <= qh.get_player_world_location('x') <= 1350:
            break
        elif s2:
            osrs.move.fast_click(s2[0])
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') > 9000:
            break
        elif qh.get_tiles('1311,3807,0'):
            # clicking this constantly stalls the animation
            # so i have to cool down after a click
            osrs.move.fast_click(qh.get_tiles('1311,3807,0'))
            osrs.clock.sleep_one_tick()
    while True:
        qh.query_backend()
        o1 = qh.get_objects(
            osrs.queryHelper.ObjectTypes.GAME.value,
            obstacle_1_id
        )
        if qh.get_player_world_location('x') < 1302:
            break
        elif o1:
            osrs.move.fast_click(o1[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 1303, 'y': 10204, 'z': 0})
    while True:
        qh.query_backend()
        g1 = qh.get_objects(
            osrs.queryHelper.ObjectTypes.GAME.value,
            gap_1_id
        )
        if qh.get_player_world_location('y') <= 10170:
            osrs.clock.sleep_one_tick()
            break
        elif g1:
            osrs.move.fast_click(g1[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 1271, 'y': 10176, 'z': 0})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') <= 10161:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 1264, 'y': 10156, 'z': 0})


def stronghold_slayer_dungeon_spectres():
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
        if 2441 <= qh.get_player_world_location('x') <= 2447 and 9773 <= qh.get_player_world_location('y') <= 9787:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2444, 'y': 9780, 'z': 0})


'''
click esc key
run to 3310,2959,0
find obj 6279 on tile 3310,2962,0
i dungeon when y greater than 9k
end func
'''


def smoke_dungeon():
    carpet_guy_id = 'Rug Merchant'
    dungeon_entrance_id = '6279'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([carpet_guy_id])
    qh.set_chat_options()
    qh.set_tiles({'3259,3096,0', '3310,2959,0'})
    qh.set_objects(
        {'3310,2962,0'},
        {dungeon_entrance_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_player_world_location()
    print('running to rug merchant')
    while True:
        qh.query_backend()
        if qh.get_chat_options():
            osrs.clock.sleep_one_tick()
            osrs.keeb.write('3')
            break
        elif qh.get_npcs_by_name():
            c = osrs.util.find_closest_target(qh.get_npcs_by_name())
            if c:
                osrs.move.fast_click(c)
                osrs.clock.sleep_one_tick()
        else:
            if qh.get_tiles('3259,3096,0'):
                osrs.move.fast_click(qh.get_tiles('3259,3096,0'))
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3309, 'y': 3105, 'z': 0})
    print('on carpet to polli')
    while True:
        qh.query_backend()
        if 3334 <= qh.get_player_world_location('x') <= 3366 and 2994 <= qh.get_player_world_location('y') <= 3012:
            break
    print('in polli')
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') > 9000:
            break
        elif qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                dungeon_entrance_id
        ):
            osrs.move.fast_click(qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                dungeon_entrance_id
            )[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': '3310', 'y': 2962, 'z': 0})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 3222:
            osrs.keeb.press_key('esc')
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3224, 'y': 9377, 'z': 0})


def brimhaven_dungeon_steels():
    dungeon_entrance_id = '66'
    crevice_id = '30198'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'2759,3062,0', '2696,9436,0'},
        {dungeon_entrance_id, crevice_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'2796,3003,0'})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') > 9200 and 2722 <= qh.get_player_world_location('x') <= 2746:
            break
        elif qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                dungeon_entrance_id
        ):
            osrs.move.fast_click(qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                dungeon_entrance_id
            )[0])
        else:
            if qh.get_tiles('2796,3003,0'):
                osrs.move.fast_click(qh.get_tiles('2796,3003,0'))
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2763, 'y': 3062, 'z': 0})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') <= 2688:
            break
        elif qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                crevice_id
        ):
            osrs.move.fast_click(qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                crevice_id
            )[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2699, 'y': 9436, 'z': 0})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') <= 2667:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2662, 'y': 9425, 'z': 0})


def godwars_main_room():
    mountain_shortcut_1 = '16524'
    mountain_shortcut_2 = '16523'
    mountain_shortcut_3 = '3748'
    boulder_id = '26415'
    gwd_entrance_id = '26419'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'2901,3680,0', '2908,3682,0'},
        {mountain_shortcut_1, mountain_shortcut_2},
        osrs.queryHelper.ObjectTypes.GROUND.value
    )
    qh.set_objects(
        {'2910,3686,0', '2899,3717,0', '2917,3745,0'},
        {mountain_shortcut_3, boulder_id, gwd_entrance_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    # wait until i am actually in trollheim to do anything
    while True:
        qh.query_backend()
        if 3667 <= qh.get_player_world_location('y') <= 3700 and 2887 <= qh.get_player_world_location('x') <= 2896:
            break
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2901:
            break
        elif qh.get_player_world_location('x') <= 2900 and qh.get_objects(
                osrs.queryHelper.ObjectTypes.GROUND.value,
                mountain_shortcut_1
        ):
            osrs.move.fast_click(qh.get_objects(
                osrs.queryHelper.ObjectTypes.GROUND.value,
                mountain_shortcut_1
            )[0])
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2909:
            break
        elif qh.get_player_world_location('x') <= 2907 and qh.get_objects(
                osrs.queryHelper.ObjectTypes.GROUND.value,
                mountain_shortcut_2
        ):
            osrs.move.fast_click(qh.get_objects(
                osrs.queryHelper.ObjectTypes.GROUND.value,
                mountain_shortcut_2
            )[0])
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2911:
            break
        elif qh.get_player_world_location('x') <= 2909 and qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                mountain_shortcut_3
        ):
            osrs.move.fast_click(qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                mountain_shortcut_3
            )[0])
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') >= 3717:
            break
        elif qh.get_objects(
            osrs.queryHelper.ObjectTypes.GAME.value,
            boulder_id
        ) and qh.get_player_world_location('y') > 3700:
            osrs.move.fast_click(qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                boulder_id
            )[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2899, 'y': 3710, 'z': 0})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') >= 5200:
            break
        elif qh.get_objects(
            osrs.queryHelper.ObjectTypes.GAME.value,
            gwd_entrance_id
        ):
            osrs.move.fast_click(qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                gwd_entrance_id
            )[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2914, 'y': 3742, 'z': 0})


def frem_dungeon_kurask():
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
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, shortcut_2_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, shortcut_2_id)[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2737, 'y': 10007, 'z': 0})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') <= 2700:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2697, 'y': 9997, 'z': 0})


def zanaris_zygomites():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_tiles({'2412,4436,0'})
    while True:
        qh.query_backend()
        if 2409 <= qh.get_player_world_location('x') <= 2420 and 4467 <= qh.get_player_world_location('y') <= 4476:
            return
        else:
            if qh.get_tiles('2412,4436,0'):
                osrs.move.click(qh.get_tiles('2412,4436,0'))
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2416, 'y': 4471, 'z': 0})