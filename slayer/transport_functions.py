import datetime

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
    qh.set_tiles({f'{x},{y},0', '2268,2973,0'})
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('y') > 9300 and 2155 <= qh.get_player_world_location('x') <= 2174:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dungeon_entrance_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dungeon_entrance_id)[0])
        else:
            if qh.get_tiles('2268,2973,0'):
                osrs.move.fast_click(qh.get_tiles('2268,2973,0'))
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2310, 'y': 2918, 'z': 0})
    while True:
        qh.query_backend()
        if osrs.dev.point_dist(qh.get_player_world_location('x'), qh.get_player_world_location('y'), x, y) < 5:
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


def taverley_dungeon_black_dragons():
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
    print('running to steps')
    while True:
        qh.query_backend()
        # I am in the dungeon
        if qh.get_player_world_location('z') == 1:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, rock_steps_id) and qh.get_player_world_location(
                'y') > 9803:
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
            osrs.clock.sleep_one_tick()
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
            osrs.clock.sleep_one_tick()
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
        if 2468 <= qh.get_player_world_location('x') <= 2473 and 9776 <= qh.get_player_world_location('y') <= 9780:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2470, 'y': 9778, 'z': 0})


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
        if qh.get_player_world_location('x') <= 2655:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2650, 'y': 9425, 'z': 0})


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
    tele_to_frem_cave()
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


def morytania_gargoyles():
    basement_ladder_id = '30191'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_player_world_location()
    qh.set_objects(
        {'3417,3535,0'},
        {basement_ladder_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'3433,9937,3'})
    qh.set_npcs_by_name(['gargoyle'])
    qh.set_inventory()
    qh.set_canvas()
    slayer_rings = [
        ItemIDs.SLAYER_RING_1.value,
        ItemIDs.SLAYER_RING_2.value,
        ItemIDs.SLAYER_RING_3.value,
        ItemIDs.SLAYER_RING_4.value,
        ItemIDs.SLAYER_RING_5.value,
        ItemIDs.SLAYER_RING_6.value,
        ItemIDs.SLAYER_RING_7.value,
        ItemIDs.SLAYER_RING_8.value,
    ]
    last_ring_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_npcs_by_name() and qh.get_player_world_location('y') > 7500:
            return
        elif qh.get_chat_options() and 'Teleport' in qh.get_chat_options():
            osrs.keeb.write('1')
        elif qh.get_chat_options() and 'Teleport to the Morytania Slayer Tower' in qh.get_chat_options():
            osrs.keeb.write('2')
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, basement_ladder_id):
            osrs.move.right_click_v6(
                qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, basement_ladder_id)[0],
                 'Climb-down',
                 qh.get_canvas(),
                 in_inv=True
            )
            osrs.clock.sleep_one_tick()
        elif qh.get_tiles('3433,9937,3') and osrs.move.is_clickable(qh.get_tiles('3433,9937,3')):
            osrs.move.click(qh.get_tiles('3433,9937,3'))
        elif qh.get_inventory(slayer_rings) and (datetime.datetime.now() - last_ring_click).total_seconds() > 7:
            ring = qh.get_inventory(slayer_rings)
            osrs.move.right_click_v3(ring, 'Rub')
            last_ring_click = datetime.datetime.now()


def morytania_abby_demons():
    basement_ladder_id = '30191'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_player_world_location()
    qh.set_objects(
        {'3417,3535,0'},
        {basement_ladder_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'3433,9950,3', '3438,9967,3'})
    qh.set_npcs_by_name(['abyssal demon'])
    qh.set_canvas()
    qh.set_inventory()
    slayer_rings = [
        ItemIDs.SLAYER_RING_1.value,
        ItemIDs.SLAYER_RING_2.value,
        ItemIDs.SLAYER_RING_3.value,
        ItemIDs.SLAYER_RING_4.value,
        ItemIDs.SLAYER_RING_5.value,
        ItemIDs.SLAYER_RING_6.value,
        ItemIDs.SLAYER_RING_7.value,
        ItemIDs.SLAYER_RING_8.value,
    ]
    last_ring_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 3432 <= qh.get_player_world_location('x') <= 3443 and 9962 <= qh.get_player_world_location('y') <= 9973:
            return
        elif qh.get_chat_options() and 'Teleport' in qh.get_chat_options():
            osrs.keeb.write('1')
        elif qh.get_chat_options() and 'Teleport to the Morytania Slayer Tower' in qh.get_chat_options():
            osrs.keeb.write('2')
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, basement_ladder_id):
            osrs.move.right_click_v6(
                qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, basement_ladder_id)[0],
                'Climb-down',
                qh.get_canvas(),
                in_inv=True
            )
            osrs.clock.sleep_one_tick()
        elif qh.get_player_world_location('z') == 3:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3438, 'y': 9966, 'z': 3})
        elif qh.get_inventory(slayer_rings) and (datetime.datetime.now() - last_ring_click).total_seconds() > 7:
            ring = qh.get_inventory(slayer_rings)
            osrs.move.right_click_v3(ring, 'Rub')
            last_ring_click = datetime.datetime.now()


def tele_to_frem_cave():
    basement_ladder_id = '30191'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_player_world_location()
    qh.set_objects(
        {'3417,3535,0'},
        {basement_ladder_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'3433,9937,3'})
    qh.set_npcs_by_name(['gargoyle'])
    qh.set_inventory()
    slayer_rings = [
        ItemIDs.SLAYER_RING_2.value,
        ItemIDs.SLAYER_RING_3.value,
        ItemIDs.SLAYER_RING_4.value,
        ItemIDs.SLAYER_RING_5.value,
        ItemIDs.SLAYER_RING_6.value,
        ItemIDs.SLAYER_RING_7.value,
        ItemIDs.SLAYER_RING_8.value,
    ]
    last_ring_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') > 9000:
            return
        elif qh.get_chat_options() and 'Teleport' in qh.get_chat_options():
            osrs.keeb.write('1')
        elif qh.get_chat_options() and 'Teleport to the Fremennik Slayer Dungeon' in qh.get_chat_options():
            osrs.keeb.write('3')
        elif qh.get_inventory(slayer_rings) and (datetime.datetime.now() - last_ring_click).total_seconds() > 7:
            ring = qh.get_inventory(slayer_rings)
            osrs.move.right_click_v3(ring, 'Rub')
            last_ring_click = datetime.datetime.now()


def run_to_suqahs():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if 2090 <= qh.get_player_world_location('x') <= 2110 and 3860 <= qh.get_player_world_location('y') <= 3870:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2103, 'y': 3865, 'z': 0})


def duradel():
    gem_mine_ladder_id = '23584'
    duradel_ladder_id = '16683'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_objects(
        {'2838,9388,0', '2871,2971,0'},
        {duradel_ladder_id, gem_mine_ladder_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_npcs_by_name(['duradel'])
    qh.set_slayer()
    qh.set_canvas()
    glove_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_inventory() and qh.get_inventory(osrs.item_ids.ItemIDs.KARAMJA_GLOVES_3.value) \
                and (datetime.datetime.now() - glove_click).total_seconds() > 10:
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.item_ids.ItemIDs.KARAMJA_GLOVES_3.value),
                'Gem Mine',
                qh.get_canvas(),
                in_inv=True
            )
            glove_click = datetime.datetime.now()
        elif 2830 <= qh.get_player_world_location('x') <= 2845 and 9383 <= qh.get_player_world_location('y') <= 9394:
            break
    ladder_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, gem_mine_ladder_id) and (
                datetime.datetime.now() - ladder_click).total_seconds() > 6:
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, gem_mine_ladder_id)[0])
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, gem_mine_ladder_id)[0])
            ladder_click = datetime.datetime.now()
        elif 2819 <= qh.get_player_world_location('x') <= 2831 and 2994 <= qh.get_player_world_location('y') <= 3003:
            break
    while True:
        qh.query_backend()
        if 2863 <= qh.get_player_world_location('x') <= 2876 and 2963 <= qh.get_player_world_location('y') <= 2972:
            break
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2870, 'y': 2968, 'z': 0})
    ladder_click2 = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, duradel_ladder_id) and (
                datetime.datetime.now() - ladder_click2).total_seconds() > 6:
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, duradel_ladder_id)[0])
            ladder_click2 = datetime.datetime.now()
        elif qh.get_player_world_location('z') == 1:
            break
    while True:
        qh.query_backend()
        if qh.get_slayer() and qh.get_slayer()['monster']:
            print('got a new task')
            return True
        elif qh.get_npcs_by_name():
            closest = osrs.util.find_closest_target(qh.get_npcs_by_name())
            if closest:
                osrs.move.fast_click(closest)



def duradel_gloves_4():
    gem_mine_ladder_id = '23584'
    duradel_ladder_id = '16683'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_objects(
        {'2838,9388,0', '2871,2971,0'},
        {duradel_ladder_id, gem_mine_ladder_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_npcs_by_name(['duradel'])
    qh.set_slayer()
    qh.set_canvas()
    glove_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_slayer() and qh.get_slayer()['monster']:
            print('got a new task')
            return True
        elif qh.get_inventory() and qh.get_inventory(osrs.item_ids.ItemIDs.KARAMJA_GLOVES_4.value) \
                and (datetime.datetime.now() - glove_click).total_seconds() > 10:
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.item_ids.ItemIDs.KARAMJA_GLOVES_4.value),
                'Slayer master',
                qh.get_canvas(),
                in_inv=True
            )
            glove_click = datetime.datetime.now()
        elif qh.get_npcs_by_name():
            closest = osrs.util.find_closest_target(qh.get_npcs_by_name())
            if closest:
                osrs.move.fast_click(closest)


def morytania_nechs():
    basement_ladder_id = '30191'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_canvas()
    qh.set_player_world_location()
    qh.set_objects(
        {'3417,3535,0'},
        {basement_ladder_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'3412,9967,3'})
    qh.set_npcs_by_name(['Nechryael'])
    qh.set_inventory()
    slayer_rings = [
        ItemIDs.SLAYER_RING_1.value,
        ItemIDs.SLAYER_RING_2.value,
        ItemIDs.SLAYER_RING_3.value,
        ItemIDs.SLAYER_RING_4.value,
        ItemIDs.SLAYER_RING_5.value,
        ItemIDs.SLAYER_RING_6.value,
        ItemIDs.SLAYER_RING_7.value,
        ItemIDs.SLAYER_RING_8.value,
    ]
    last_ring_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_npcs_by_name():
            return
        elif qh.get_chat_options() and 'Teleport' in qh.get_chat_options():
            osrs.keeb.write('1')
        elif qh.get_chat_options() and 'Teleport to the Morytania Slayer Tower' in qh.get_chat_options():
            osrs.keeb.write('2')
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, basement_ladder_id):
            osrs.move.right_click_v6(
                qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, basement_ladder_id)[0],
                'Climb-down',
                qh.get_canvas(),
                in_inv=True
            )
            osrs.clock.sleep_one_tick()
        elif qh.get_tiles('3412,9967,3') and osrs.move.is_clickable(qh.get_tiles('3412,9967,3')):
            osrs.move.click(qh.get_tiles('3412,9967,3'))
        elif qh.get_inventory(slayer_rings) and (datetime.datetime.now() - last_ring_click).total_seconds() > 7:
            ring = qh.get_inventory(slayer_rings)
            osrs.move.right_click_v3(ring, 'Rub')
            last_ring_click = datetime.datetime.now()
        elif qh.get_player_world_location('z') == 3:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3412, 'y': 9967, 'z': 3})


def catacombs(x, y):
    dungeon_entrance_id = '27785'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects(
        {'1636,3673,0'},
        {dungeon_entrance_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_player_world_location()
    last_tele_cast = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 1623 <= qh.get_player_world_location('x') <= 1656 and 3664 <= qh.get_player_world_location('y') <= 3684:
            break
        elif (datetime.datetime.now() - last_tele_cast).total_seconds() > 10:
            osrs.game.cast_spell('218,36')
            last_tele_cast = datetime.datetime.now()
    while True:
        qh.query_backend()
        if 1658 <= qh.get_player_world_location('x') <= 1670 and qh.get_player_world_location('y') > 10000:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dungeon_entrance_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dungeon_entrance_id)[0])
    while True:
        qh.query_backend()
        if osrs.dev.point_dist(qh.get_player_world_location('x'), qh.get_player_world_location('y'), x, y) < 5:
            break
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': x, 'y': y, 'z': 0})


def mount_karuulm_drakes():
    shortcut_1_id = '34397'
    shortcut_2_id = '34396'
    obstacle_1_id = '34544'
    stairs_to_drakes_id = '34530'
    tunnel_to_final_room_id = '34516'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'1324,3778,0', '1324,3788,0', '1321,10205,0', '1272,10174,0', '1330,10206,0', '1332,10239,1'},
        {shortcut_1_id, shortcut_2_id, obstacle_1_id, stairs_to_drakes_id, tunnel_to_final_room_id},
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
        if qh.get_player_world_location('x') > 1321:
            break
        elif o1:
            osrs.move.fast_click(o1[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 1303, 'y': 10204, 'z': 0})
    while True:
        qh.query_backend()
        g1 = qh.get_objects(
            osrs.queryHelper.ObjectTypes.GAME.value,
            stairs_to_drakes_id
        )
        if qh.get_player_world_location('z') == 1:
            osrs.clock.sleep_one_tick()
            break
        elif g1:
            osrs.move.fast_click(g1[0])
    while True:
        qh.query_backend()
        if 1299 <= qh.get_player_world_location('x') <= 1325 and 10225 <= qh.get_player_world_location('y') <= 10251:
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 1311, 'y': 10239, 'z': 1})


def kraken_cove_private():
    cove_entrance = '30177'
    private_entrance = '537'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_canvas()
    qh.set_chat_options()
    qh.set_tiles({'2315,3613,0'})
    qh.set_objects(
        {'2278,3612,0'},
        {cove_entrance},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_objects(
        {'2280,10017,0'},
        {private_entrance},
        osrs.queryHelper.ObjectTypes.WALL.value
    )
    qh.set_player_world_location()
    qh.set_npcs(['496', '494'])
    last_successful_instance_entrance_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        # In my private instance
        if len(qh.get_npcs()) > 0:
            return
        # cave entrance visible
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, cove_entrance):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, cove_entrance)[0])
        # between fairy ring and cave entrance
        elif 2267 <= qh.get_player_world_location('x') <= 2334 and 3597 <= qh.get_player_world_location('y') <= 3640:
            # I'm on the fairy ring and the dax pathing always breaks
            if qh.get_player_world_location('x') == 2319 and qh.get_player_world_location('y') == 3619 and qh.get_tiles('2315,3613,0'):
                osrs.move.fast_click(qh.get_tiles('2315,3613,0'))
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2282, 'y': 3610, 'z': 0})
        # Chat option is up to go into the instance
        elif qh.get_chat_options('Yes, pay 25,000 x Coins.'):
            osrs.keeb.write(str(qh.get_chat_options('Yes, pay 25,000 x Coins.')))
        # Entrance to the private instance is in view
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, private_entrance) \
                and (datetime.datetime.now() - last_successful_instance_entrance_click).total_seconds() > 15:
            result = osrs.move.right_click_v6(
                qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, private_entrance)[0], 'Private', qh.get_canvas()
            )
            if result:
                last_successful_instance_entrance_click = datetime.datetime.now()
        # im in the cave but i cant see the instance entrance yet
        elif 2242 <= qh.get_player_world_location('x') <= 2300 and 9977 <= qh.get_player_world_location('y') <= 10015 \
                and (datetime.datetime.now() - last_successful_instance_entrance_click).total_seconds() > 15:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2270, 'y': 10003, 'z': 0})


def kraken_cove_waterfiends():
    cove_entrance = '30177'
    private_entrance = '537'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'2315,3613,0'})
    qh.set_objects(
        {'2278,3612,0'},
        {cove_entrance},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_player_world_location()
    qh.set_npcs_by_name(['waterfiend'])
    while True:
        qh.query_backend()
        # In cove
        if len(qh.get_npcs()) > 0:
            return
        # cave entrance visible
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, cove_entrance):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, cove_entrance)[0])
        # between fairy ring and cave entrance
        elif 2267 <= qh.get_player_world_location('x') <= 2334 and 3597 <= qh.get_player_world_location('y') <= 3640:
            # I'm on the fairy ring and the dax pathing always breaks
            if qh.get_player_world_location('x') == 2319 and qh.get_player_world_location('y') == 3619 and qh.get_tiles('2315,3613,0'):
                osrs.move.fast_click(qh.get_tiles('2315,3613,0'))
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2282, 'y': 3610, 'z': 0})


def morytania_spectres():
    basement_ladder_id = 16537
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_canvas()
    qh.set_player_world_location()
    qh.set_objects_v2('game', {basement_ladder_id})
    qh.set_inventory()
    slayer_rings = [
        ItemIDs.SLAYER_RING_1.value,
        ItemIDs.SLAYER_RING_2.value,
        ItemIDs.SLAYER_RING_3.value,
        ItemIDs.SLAYER_RING_4.value,
        ItemIDs.SLAYER_RING_5.value,
        ItemIDs.SLAYER_RING_6.value,
        ItemIDs.SLAYER_RING_7.value,
        ItemIDs.SLAYER_RING_8.value,
    ]
    last_ring_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('z') == 1 and 3405 <= qh.get_player_world_location('x') < 3450:
            return
        elif qh.get_chat_options() and 'Teleport' in qh.get_chat_options():
            osrs.keeb.write('1')
        elif qh.get_chat_options() and 'Teleport to the Morytania Slayer Tower' in qh.get_chat_options():
            osrs.keeb.write('2')
        elif qh.get_objects_v2('game', basement_ladder_id):
            osrs.move.interact_with_object(
                basement_ladder_id, 'z', 1, True,
                right_click_option='Climb-up', timeout=7
            )
        elif qh.get_inventory(slayer_rings) and (datetime.datetime.now() - last_ring_click).total_seconds() > 7:
            ring = qh.get_inventory(slayer_rings)
            osrs.move.right_click_v3(ring, 'Rub')
            last_ring_click = datetime.datetime.now()


def iorworth_dungeon_dark_beasts():
    entrance_id = 36690
    shortcut_id = 36692
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_canvas()
    last_crystal = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 3150 <= qh.get_player_world_location('x') <= 3300 and 6000 <= qh.get_player_world_location('y') <= 6100:
            break
        elif qh.get_inventory(osrs.item_ids.ItemIDs.ETERNAL_TELEPORT_CRYSTAL.value) and (datetime.datetime.now() - last_crystal).total_seconds() > 7:
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.item_ids.ItemIDs.ETERNAL_TELEPORT_CRYSTAL.value),
                'Prifddinas',
                qh.get_canvas(),
                in_inv=True
            )
            last_crystal = datetime.datetime.now()
    osrs.move.go_to_loc(3229, 6049)
    osrs.move.interact_with_object(
        entrance_id, 'y', 10000, True, right_click_option='Enter'
    )
    osrs.move.interact_with_object(
        shortcut_id, 'x', 3221, True
    )
    osrs.move.go_to_loc(3176, 12420)


def iorworth_dungeon_elves():
    entrance_id = 36690
    shortcut_id = 36692
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_canvas()
    last_crystal = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 3150 <= qh.get_player_world_location('x') <= 3300 and 6000 <= qh.get_player_world_location('y') <= 6100:
            break
        elif qh.get_inventory(osrs.item_ids.ItemIDs.ETERNAL_TELEPORT_CRYSTAL.value) and (datetime.datetime.now() - last_crystal).total_seconds() > 7:
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.item_ids.ItemIDs.ETERNAL_TELEPORT_CRYSTAL.value),
                'Prifddinas',
                qh.get_canvas(),
                in_inv=True
            )
            last_crystal = datetime.datetime.now()
    osrs.move.go_to_loc(3229, 6049)
    osrs.move.interact_with_object(
        entrance_id, 'y', 10000, True, right_click_option='Enter'
    )
    osrs.move.interact_with_object(
        shortcut_id, 'x', 3221, True
    )
    osrs.move.go_to_loc(3189, 12409)


def rune_dragons():
    '''
    3547,10455,0 in dungeon
click 32113 y< 10468
click 32117 y> 10000
click 32153 x < 1574
break
    '''
    def in_lithkren():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_widgets({'187,3'})
        qh.query_backend()
        if 3500 <= qh.get_player_world_location('x') <= 3600 and 10400 <= qh.get_player_world_location('y') <= 10500:
            return True
        elif qh.get_widgets('187,3'):
            osrs.keeb.write('3')
    mounted_pendant_id = 33417
    osrs.move.interact_with_object(
        mounted_pendant_id, 'z', 3, True,
        obj_type='decorative', custom_exit_function=in_lithkren, right_click_option='Teleport menu',
        timeout=7
    )
    osrs.move.interact_with_object(
        32113, 'y', 10468, True
    )
    osrs.move.interact_with_object(
        32117, 'y', 8000, False
    )
    osrs.move.interact_with_object(
        32153, 'x', 1574, True, obj_tile={'x': 1574, 'y': 5074, 'z': 0},
        right_click_option='Pass', timeout=10
    )