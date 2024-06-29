import datetime

import osrs


def bank_in_lumby():
    stairs_up_1_id = '16671'
    stairs_up_2_id = '16672'
    lum_top_floor_bank_tile = '3208,3221,2'
    lum_top_floor_bank_id = '18491'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'3205,3208,0', '3205,3208,1', lum_top_floor_bank_tile},
        {stairs_up_1_id, stairs_up_2_id, lum_top_floor_bank_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_canvas()
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, lum_top_floor_bank_id):
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_2_id):
            osrs.move.right_click_v6(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_2_id)[0],
                                     'Climb-up', qh.get_canvas())
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_1_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_1_id)[0])


def bank_to_lumby_ground():
    stairs_up_1_id = '16673'
    stairs_up_2_id = '16672'
    lum_top_floor_bank_tile = '3208,3221,2'
    lum_top_floor_bank_id = '18491'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'3205,3208,2', '3205,3208,1', lum_top_floor_bank_tile},
        {stairs_up_1_id, stairs_up_2_id, lum_top_floor_bank_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_canvas()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('z') == 0:
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_2_id):
            osrs.move.right_click_v6(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_2_id)[0],
                                     'Climb-down', qh.get_canvas())
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_1_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_1_id)[0])


def walk_to_sheep_shearer():
    chat_holder_widget = '231,0'
    gate_id = '12986'
    door_id = '13001'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_widgets({chat_holder_widget})
    qh.set_objects(
        {'3188,3279,0', '3189,3275,0'},
        {gate_id, door_id},
        osrs.queryHelper.ObjectTypes.WALL.value
    )
    qh.set_npcs_by_name(['fred the farmer'])
    # run to farmers house
    while True:
        qh.query_backend()
        if 3182 <= qh.get_player_world_location('x') <= 3190 and 3279 <= qh.get_player_world_location('y') <= 3289:
            break
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3188, 'y': 3283, 'z': 0})
    # enter the farmers house
    last_gate_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_door_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets(chat_holder_widget):
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, gate_id) \
                and (datetime.datetime.now() - last_gate_click).total_seconds() > 5:
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, gate_id)[0])
            last_gate_click = datetime.datetime.now()
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door_id) \
                and not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, gate_id) \
                and (datetime.datetime.now() - last_door_click).total_seconds() > 5:
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door_id)[0])
            last_door_click = datetime.datetime.now()
        elif (not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door_id)
              and not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, gate_id)
              and len(qh.get_npcs_by_name()) > 0):
            osrs.move.fast_click(qh.get_npcs_by_name()[0])


def leave_farmer_freds_house():
    chat_holder_widget = '231,0'
    gate_id = '12986'
    door_id = '13001'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_tiles({'3188,3283,0'})
    qh.set_widgets({chat_holder_widget})
    qh.set_objects(
        {'3188,3279,0', '3189,3275,0'},
        {gate_id, door_id},
        osrs.queryHelper.ObjectTypes.WALL.value
    )
    qh.set_npcs_by_name(['fred the farmer'])
    # enter the farmers house
    last_gate_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_door_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') >= 3281:
            return
        elif (qh.get_tiles('3188,3283,0') and not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door_id)
              and not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, gate_id)):
            osrs.move.fast_click(qh.get_tiles('3188,3283,0'))
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door_id) \
                and (datetime.datetime.now() - last_door_click).total_seconds() > 5:
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door_id)[0])
            last_door_click = datetime.datetime.now()
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, gate_id) \
            and not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door_id) \
                and (datetime.datetime.now() - last_gate_click).total_seconds() > 5:
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, gate_id)[0])
            last_gate_click = datetime.datetime.now()


def walk_to_wizards_tower():
    door1_id = '23972'
    door2_id = '23972'
    stairs1_id = '12536'
    stairs2_id = '12537'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'3109,3167,0'},
        {door1_id},
        osrs.queryHelper.ObjectTypes.WALL.value
    )
    qh.set_objects(
        {'3107,3162,0', '3104,3160,0', '3104,3160,1'},
        {door2_id, stairs1_id, stairs2_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_canvas()
    # walk to entrance
    while True:
        qh.query_backend()
        if 3106 <= qh.get_player_world_location('x') <= 3116 and 3167 <= qh.get_player_world_location('y') <= 3172:
            break
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3111, 'y': 3169, 'z': 0})
    # go to top floor
    while True:
        qh.query_backend()
        if qh.get_player_world_location('z') == 2:
            break
        elif qh.get_player_world_location('z') == 1 and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs2_id):
            osrs.move.right_click_v6(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs2_id)[0], 'Climb-up', qh.get_canvas())
        elif (not qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, door2_id)
              and not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id)
              and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs1_id)):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs1_id)[0])
        elif (not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id)
              and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, door2_id)):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, door2_id)[0])
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id)[0])


def glory_to_draynor():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_chat_options()
    qh.set_canvas()
    last_glory_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_d_vill_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 3070 <= qh.get_player_world_location('x') < 3110 and 3234 <= qh.get_player_world_location('y') <= 3280:
            return
        elif qh.get_chat_options('Draynor Village') and (datetime.datetime.now() - last_d_vill_click).total_seconds() > 10:
            osrs.keeb.write(str(qh.get_chat_options('Draynor Village')))
            last_d_vill_click = datetime.datetime.now()
        elif qh.get_inventory(osrs.item_ids.ItemIDs.AMULET_OF_GLORY6.value) and (datetime.datetime.now() - last_glory_click).total_seconds() > 4:
            res = osrs.move.right_click_v6(qh.get_inventory(
                [osrs.item_ids.ItemIDs.AMULET_OF_GLORY6.value, osrs.item_ids.ItemIDs.AMULET_OF_GLORY5.value, osrs.item_ids.ItemIDs.AMULET_OF_GLORY4.value]),
                'Rub',
                qh.get_canvas(),
                in_inv=True
            )
            if res:
                last_glory_click = datetime.datetime.now()


def walk_to_rimmington():
    chat_holder_widget = '217,1'
    door1_id = '1535'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_objects(
        {'2964,3206,0'},
        {door1_id},
        osrs.queryHelper.ObjectTypes.WALL.value
    )
    qh.set_npcs_by_name(['hetty'])
    qh.set_widgets({chat_holder_widget})
    # walk to entrance
    while True:
        qh.query_backend()
        if 2950 <= qh.get_player_world_location('x') <= 2960 and 3200 <= qh.get_player_world_location('y') <= 3220:
            break
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2956, 'y': 3209, 'z': 0})
    # open door and talk to witch
    last_door_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets(chat_holder_widget):
            return
        elif len(qh.get_npcs_by_name()) > 0 and not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id):
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif (qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id)
              and (datetime.datetime.now() - last_door_click).total_seconds() > 7):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id)[0])
            last_door_click = datetime.datetime.now()


def leave_hettys_house():
    door1_id = '1535'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_objects(
        {'2964,3206,0'},
        {door1_id},
        osrs.queryHelper.ObjectTypes.WALL.value
    )
    qh.set_tiles({'2956,3207,0'})
    # open door and talk to witch
    last_door_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') <= 2964:
            return
        elif (qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id)
              and (datetime.datetime.now() - last_door_click).total_seconds() > 7):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id)[0])
            last_door_click = datetime.datetime.now()
        elif qh.get_tiles('2956,3207,0') and not qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value, door1_id):
            osrs.move.fast_click(qh.get_tiles('2956,3207,0'))
