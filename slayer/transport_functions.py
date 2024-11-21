import datetime

import osrs
import osrs.move


def konar():
    osrs.game.tele_home_v2()
    osrs.game.tele_home_fairy_ring('cir')
    mount_karuulm('konar')
    osrs.move.interact_with_npc('8623', right_click_option='Assignment', exit_on_dialogue=True, timeout=7)
    osrs.dev.logger.debug("Successfully started talking to konar.")


def isle_of_souls_dungeon_v2(x, y):
    # dax doesnt work if i am standing on the fairy ring - just run off it
    osrs.move.go_to_loc(2280, 2967, skip_dax=True)
    osrs.move.go_to_loc(2306, 2962)
    osrs.move.go_to_loc(2310, 2918)
    osrs.move.interact_with_object_v3(
        40736, coord_type='y', coord_value=9000, greater_than=True
    )
    osrs.move.go_to_loc(x, y)


def kalphite_layer():
    osrs.move.go_to_loc(3263, 3096, skip_dax=True)
    osrs.move.go_to_loc(3320, 3121)
    osrs.move.interact_with_object_v3(30180, 'y', 5000)


def south_quidamortem_trolls():
    osrs.move.go_to_loc(1290, 3493, skip_dax=True)
    osrs.move.go_to_loc(1230, 3496)


def taverley_dungeon_black_dragons():
    osrs.dev.logger.debug('running to wall')
    osrs.move.go_to_loc(2936, 3355)
    osrs.move.interact_with_object_v3(
        24222, coord_type='x', coord_value=2935, greater_than=False
    )
    osrs.dev.logger.debug('running to ladder')
    osrs.move.go_to_loc(2885, 3393)
    osrs.move.interact_with_object_v3(
        16680, coord_type='y', coord_value=9000, greater_than=True, right_click_option='Climb-down', timeout=7
    )
    osrs.move.go_to_loc(2883, 9820)
    osrs.move.interact_with_object_v3(
        30189, coord_type='z', coord_value=1, greater_than=True
    )
    osrs.move.go_to_loc(2868, 9827, 1)


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
    osrs.dev.logger.debug('running to wall')
    osrs.move.go_to_loc(2936, 3355)
    osrs.move.interact_with_object_v3(
        24222, coord_type='x', coord_value=2935, greater_than=False
    )
    osrs.dev.logger.debug('running to ladder')
    osrs.move.go_to_loc(2885, 3393)
    osrs.move.interact_with_object_v3(
        16680, coord_type='y', coord_value=9000, greater_than=True, right_click_option='Climb-down', timeout=7
    )
    osrs.dev.logger.debug('running to steps')
    osrs.move.go_to_loc(2882, 9813)
    osrs.move.interact_with_object_v3(
        16510, coord_type='x', coord_value=2878, greater_than=False, timeout=2
    )


def taverley_dungeon_black_demons():
    osrs.dev.logger.debug('running to wall')
    osrs.move.go_to_loc(2936, 3355)
    osrs.move.interact_with_object_v3(
        24222, coord_type='x', coord_value=2935, greater_than=False
    )
    osrs.dev.logger.debug('running to ladder')
    osrs.move.go_to_loc(2885, 3393)
    osrs.move.interact_with_object_v3(
        16680, coord_type='y', coord_value=9000, greater_than=True, right_click_option='Climb-down', timeout=7
    )
    osrs.move.interact_with_object_v3(
        16509, coord_type='x', coord_value=2888, greater_than=True
    )
    osrs.move.go_to_loc(2878, 9768)


def stronghold_slayer_cave(x, y):
    osrs.game.standard_spells_tele('Varrock')
    osrs.move.go_to_loc(3180, 3504)
    osrs.game.sprit_tree('gnome stronghold')
    osrs.move.go_to_loc(2431, 3420)
    osrs.move.interact_with_object_v3(
        26709, 'y', 9000, right_click_option='Enter', timeout=7
    )
    osrs.move.go_to_loc(x, y)


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
    osrs.move.go_to_loc(3362, 2969)
    osrs.move.go_to_loc(3333, 2937)
    osrs.move.go_to_loc(3310, 2962)
    osrs.keeb.press_key('esc')
    osrs.move.interact_with_object_v3(
        int(dungeon_entrance_id), 'y', 9000
    )
    osrs.move.go_to_loc(3224, 9377)


def brimhaven_dungeon_dragons(x, y):
    osrs.move.go_to_loc(2791, 3001, skip_dax=True)
    osrs.move.go_to_loc(2762, 3059)
    osrs.move.interact_with_object_v3(66, 'y', 9000)
    osrs.move.go_to_loc(2711, 9482)
    osrs.move.go_to_loc(2700, 9436)
    osrs.move.interact_with_object_v3(30198, 'x', 2684, greater_than=False)
    osrs.move.go_to_loc(x, y)


def brimhaven_dungeon_south(monster):
    osrs.move.go_to_loc(2791, 3001, skip_dax=True)
    osrs.move.go_to_loc(2762, 3059)
    osrs.move.interact_with_object_v3(66, 'y', 9000)
    osrs.move.go_to_loc(2705, 9493)
    if monster == 'black demons':
        return
    osrs.move.interact_with_object_v3(21735, 'x', 2694, greater_than=False)
    osrs.move.go_to_loc(2676, 9479)
    osrs.move.interact_with_object_v3(21734, 'x', 2675, greater_than=False)
    osrs.move.go_to_loc(2665, 9482)
    if monster == 'fire giants':
        return
    osrs.move.go_to_loc(2635, 9521)
    osrs.move.interact_with_object_v3(21725, 'z', 2)
    if monster == 'greater demons':
        return


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


def frem_dungeon(monster):
    '''

    :param monster: cave crawler | rock slug | cockatrice | pyrefiend | basilisk | turoth | jellies | kurask
    :return:
    '''
    tele_to_frem_cave()
    if monster == 'cave crawler':
        return
    elif monster == 'rock slug':
        return osrs.move.go_to_loc(2796, 10018)
    elif monster == 'cockatrice':
        return osrs.move.go_to_loc(2790, 10035)
    osrs.move.go_to_loc(2776, 10003)
    osrs.move.interact_with_object_v3(
        16544, 'x', 2774, obj_tile={'x': 2774, 'y': 10003, 'z': 0}, greater_than=False
    )
    osrs.move.interact_with_object_v3(
        16544, 'x', 2769, obj_tile={'x': 2769, 'y': 10002, 'z': 0}, greater_than=False
    )
    if monster == 'pyrefiend':
        return
    osrs.move.go_to_loc(2744, 10009)
    if monster == 'basilisk':
        return
    osrs.move.interact_with_object_v3(
        16539, 'x', 2734,
        obj_tile={'x': 2734, 'y': 10008, 'z': 0}, greater_than=False, obj_type='wall'
    )

    if monster == 'turoth':
        return
    elif monster == 'jellies':
        return osrs.move.go_to_loc(2705, 10027)
    elif monster == 'kurask':
        osrs.move.go_to_loc(2702, 9994)
        osrs.move.interact_with_object_v3(
            29993, 'y', 9989, right_click_option='Climb', timeout=8, greater_than=False
        )
        return osrs.move.go_to_loc(2705, 9977)


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


def tele_to_frem_cave():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_player_world_location()
    qh.set_inventory()
    slayer_rings = [
        osrs.item_ids.SLAYER_RING_2,
        osrs.item_ids.SLAYER_RING_3,
        osrs.item_ids.SLAYER_RING_4,
        osrs.item_ids.SLAYER_RING_5,
        osrs.item_ids.SLAYER_RING_6,
        osrs.item_ids.SLAYER_RING_7,
        osrs.item_ids.SLAYER_RING_8,
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
        if qh.get_inventory() and qh.get_inventory(osrs.osrs.item_ids.KARAMJA_GLOVES_3) \
                and (datetime.datetime.now() - glove_click).total_seconds() > 10:
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.osrs.item_ids.KARAMJA_GLOVES_3),
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
        elif qh.get_inventory() and qh.get_inventory(osrs.osrs.item_ids.KARAMJA_GLOVES_3) \
                and (datetime.datetime.now() - glove_click).total_seconds() > 10:
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.osrs.item_ids.KARAMJA_GLOVES_3),
                'Slayer master',
                qh.get_canvas(),
                in_inv=True
            )
            glove_click = datetime.datetime.now()
        elif qh.get_npcs_by_name():
            closest = osrs.util.find_closest_target(qh.get_npcs_by_name())
            if closest:
                osrs.move.fast_click(closest)


def catacombs_v2(x, y):
    osrs.game.standard_spells_tele('Kourend')
    osrs.move.interact_with_object_v3(
        27785, 'y', 10000
    )
    osrs.move.go_to_loc(x, y)


def mount_karuulm(monster):
    osrs.move.go_to_loc(1321, 3763, skip_dax=True)
    osrs.move.go_to_loc(1323, 3775)
    osrs.move.interact_with_object_v3(34397, 'y', 3780)
    osrs.move.interact_with_object_v3(34396, 'y', 3790)
    if monster.lower() in ['konar', 'konar quo maten']:
        return osrs.move.go_to_loc(1308, 3788)

    osrs.move.interact_with_object_v3(
        34359, 'y', 10000, right_click_option='Activate',
        timeout=15, obj_type = 'ground'
    )
    osrs.move.go_to_loc(1311, 10205)
    ## First Floor
    if monster.lower() in ['wyrm', 'wyrms']:
        osrs.move.interact_with_object_v3(
            34544, 'x', 1302, greater_than=False, obj_tile={'x': 1302, 'y': 10205, 'z': 0}
        )
        osrs.move.go_to_loc(1271, 10178)
        osrs.move.interact_with_object_v3(34515, 'y', 10172, greater_than=False)
        osrs.move.go_to_loc(1263, 10158)
        return
    elif monster.lower() in ['hydras', 'hydra']:
        osrs.move.interact_with_object_v3(
            34544, 'y', 1312, obj_tile={'x': 1311, 'y': 10215, 'z': 0}
        )
        osrs.move.go_to_loc(1311, 10234)
        return

    osrs.move.interact_with_object_v3(
        34544, 'x', 1321, obj_tile={'x': 1321, 'y': 10205, 'z': 0}
    )
    osrs.move.interact_with_object_v3(
        34530, 'z', 1
    )

    ## Second Floor
    if monster.lower() in ['greater demon', 'greater demons']:
        osrs.move.go_to_loc(1284, 10206, 1)
        return
    elif monster.lower() in ['drake', 'drakes']:
        osrs.move.go_to_loc(1312, 10231, 1)
        return

    osrs.move.go_to_loc(1313, 10194, 1)
    osrs.move.interact_with_object_v3(34530, 'z', 2)

    ## Third Floor
    if monster.lower() in ['hellhound', 'hellhounds']:
        osrs.move.go_to_loc(1337, 10201, 2)
        return
    elif monster.lower() in ['fire giants', 'fire giant']:
        osrs.move.go_to_loc(1281, 10208, 2)
        return


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
        osrs.item_ids.SLAYER_RING_1,
        osrs.item_ids.SLAYER_RING_2,
        osrs.item_ids.SLAYER_RING_3,
        osrs.item_ids.SLAYER_RING_4,
        osrs.item_ids.SLAYER_RING_5,
        osrs.item_ids.SLAYER_RING_6,
        osrs.item_ids.SLAYER_RING_7,
        osrs.item_ids.SLAYER_RING_8,
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
        elif qh.get_inventory(osrs.osrs.item_ids.ETERNAL_TELEPORT_CRYSTAL) and (datetime.datetime.now() - last_crystal).total_seconds() > 7:
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.osrs.item_ids.ETERNAL_TELEPORT_CRYSTAL),
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
        elif qh.get_inventory(osrs.osrs.item_ids.ETERNAL_TELEPORT_CRYSTAL) and (datetime.datetime.now() - last_crystal).total_seconds() > 7:
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.osrs.item_ids.ETERNAL_TELEPORT_CRYSTAL),
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
        32113, 'y', 10469, True
    )
    osrs.move.interact_with_object(
        32117, 'y', 8000, False
    )
    osrs.move.interact_with_object(
        32153, 'x', 1574, True, obj_tile={'x': 1574, 'y': 5074, 'z': 0},
        right_click_option='Pass', timeout=10
    )


def fossil_island(monster='wyverns'):
    def in_house_on_hill():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_widgets({'187,3'})
        qh.query_backend()
        if 3758 <= qh.get_player_world_location('x') <= 3772 and 3864 <= qh.get_player_world_location('y') <= 3882:
            return True
        elif qh.get_widgets('187,3'):
            osrs.keeb.write('2')

    def in_meadow():
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_widgets({'608,15'})
        qh.query_backend()
        if 3669 <= qh.get_player_world_location('x') <= 3683 and 3865 <= qh.get_player_world_location('y') <= 3879:
            return True
        elif qh.get_widgets('608,15'):
            osrs.keeb.write('4')
    mounted_pendant_id = 33417
    osrs.move.interact_with_object(
        mounted_pendant_id, 'z', 3, True,
        obj_type='decorative', custom_exit_function=in_house_on_hill, right_click_option='Teleport menu',
        timeout=7
    )
    osrs.move.interact_with_object_v3(
        30920, custom_exit_function=in_meadow, timeout=7
    )
    if monster == 'mutated zygomites':
        return

    osrs.move.go_to_loc(3680, 3854)
    osrs.move.interact_with_object_v3(
        30842, coord_type='y', coord_value=10000
    )
    osrs.move.go_to_loc(3602, 10291)
    osrs.move.interact_with_object_v3(
        31485, coord_type='x', coord_value=3607, right_click_option='Climb', timeout=5
    )
    osrs.move.go_to_loc(3611, 10275)


def travel_to_priff():
    osrs.game.standard_spells_tele('Varrock')
    osrs.move.go_to_loc(3180, 3504)
    osrs.game.sprit_tree('prifddinas')


def iorworth_dungeon(x, y):
    osrs.move.go_to_loc(3229, 6049)
    osrs.move.interact_with_object(
        36690, 'y', 10000, True, right_click_option='Enter'
    )
    osrs.move.go_to_loc(x, y)


def run_to_safe_spot(x, y, z=0):
    osrs.player.turn_off_all_prayers()
    osrs.move.go_to_loc(x, y, z, exact_tile=True)
    return


def kelda_trolls():
    osrs.move.go_to_loc(2737, 3724, skip_dax=True)
    osrs.move.go_to_loc(2728, 3713)
    osrs.move.interact_with_object_v3(5008, 'y', 9000)
    osrs.move.go_to_loc(2781, 10144)


def mory_slayer_tower(monster):
    '''

    :param monster: 'aberrant spectres' | 'bloodvelds' | 'abby demons'| 'gargoyles' | 'nechs'
    :return:
    '''
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_canvas()
    qh.set_player_world_location()
    qh.set_inventory()
    slayer_rings = [
        osrs.item_ids.SLAYER_RING_1,
        osrs.item_ids.SLAYER_RING_2,
        osrs.item_ids.SLAYER_RING_3,
        osrs.item_ids.SLAYER_RING_4,
        osrs.item_ids.SLAYER_RING_5,
        osrs.item_ids.SLAYER_RING_6,
        osrs.item_ids.SLAYER_RING_7,
        osrs.item_ids.SLAYER_RING_8,
    ]
    last_ring_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 3405 <= qh.get_player_world_location('x') <= 3445 and 3532 <= qh.get_player_world_location('y') <= 3546:
            break
        elif qh.get_chat_options() and 'Teleport' in qh.get_chat_options():
            osrs.keeb.write('1')
        elif qh.get_chat_options() and 'Teleport to the Morytania Slayer Tower' in qh.get_chat_options():
            osrs.keeb.write('2')
        elif qh.get_inventory(slayer_rings) and (datetime.datetime.now() - last_ring_click).total_seconds() > 7.0:
            ring = qh.get_inventory(slayer_rings)
            osrs.move.right_click_v6(ring, 'Rub', qh.get_canvas(), in_inv=True)
            last_ring_click = datetime.datetime.now()
    if monster == 'aberrant spectres':
        osrs.move.interact_with_object_v3(
            16537, 'z', 1, True,
            right_click_option='Climb-up', timeout=9
        )
        return
    osrs.move.interact_with_object_v3(
        30191, 'z', 3, right_click_option='Climb-down', timeout=7
    )

    if monster == 'bloodvelds':
        return
    elif monster == 'nechs':
        osrs.move.go_to_loc(3413, 9965, 3)
    elif monster == 'abby demons':
        osrs.move.go_to_loc(3438, 9967, 3)
    elif monster == 'gargoyles':
        osrs.move.go_to_loc(3440, 9946, 3)


def skeletal_wyverns():
    osrs.move.go_to_loc(2998, 3120, skip_dax=True)
    osrs.move.go_to_loc(3010, 3149)
    osrs.move.interact_with_object_v3(
        1738, 'y', 9000, right_click_option='Climb-down', timeout=7
    )
    osrs.move.interact_with_object_v3(
        53250, 'x', 3014
    )
    # wait for the entrance animation to stop
    osrs.clock.random_sleep(7, 7.1)


def chasm_of_fire(monster):
    osrs.move.go_to_loc(1441, 3658, skip_dax=True)
    osrs.move.interact_with_object_v3(
        30236, 'y', 9000, right_click_option='Enter', timeout=10
    )
    if monster == 'lesser demons':
        return
    osrs.move.go_to_loc(1438, 10092, 3)
    osrs.move.interact_with_object_v3(
        30258, 'z', 2, greater_than=False, right_click_option='Enter', timeout=10
    )
    osrs.move.go_to_loc(1455, 10092, 2)
    if monster == 'greater demons':
        return
    osrs.move.interact_with_object_v3(
        30258, 'z', 1, greater_than=False, right_click_option='Enter', timeout=10
    )
    osrs.move.go_to_loc(1429, 10069, 1)


def lighthouse():
    osrs.game.tele_home_v2()
    osrs.game.tele_home_fairy_ring('alp')
    osrs.move.go_to_loc(2509, 3633, skip_dax=True)
    osrs.move.interact_with_object_v3(
        4577, 'y', 3636, greater_than=True, obj_type='wall', intermediate_tile='2509,3640,0'
    )
    osrs.move.interact_with_object_v3(4383, 'y', 9000)
    osrs.move.interact_with_object_v3(
        4545, 'y', 10003, obj_type='wall', right_click_option='Open', timeout=7
    )
    osrs.move.interact_with_object_v3(
        4485, 'y', 10008, right_click_option='Climb', timeout=7
    )
    osrs.move.go_to_loc(2526, 10033)


def fairy_ring_back_slay_area(qh, transport_func, weapon, fairy_ring, fn_arg=None):
    qh.set_equipment()
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.DRAMEN_STAFF):
            osrs.move.fast_click_v2(qh.get_inventory(osrs.item_ids.DRAMEN_STAFF))
            break
    osrs.game.tele_home_v2()
    osrs.game.click_restore_pool()
    osrs.game.tele_home_fairy_ring(fairy_ring)
    if fn_arg is None:
        transport_func()
    else:
        transport_func(fn_arg)
    qh.query_backend()
    osrs.move.fast_click_v2(qh.get_inventory(weapon))


def brine_cavern():
    qh = osrs.qh_v2.qh()
    qh.set_inventory()
    osrs.move.go_to_loc(2748, 3732, skip_dax=True, exact_tile=True)
    qh.query_backend()
    osrs.move.interact_with_object_v3(
        18137, 'y', 10000,
        pre_interact=lambda: osrs.move.fast_click_v2(qh.get_inventory(osrs.item_ids.SPADE)),
        right_click_option='Examine', timeout=99
    )
    osrs.move.go_to_loc(2706, 10132)

