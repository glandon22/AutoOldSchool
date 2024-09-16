import datetime

import osrs

main_chat_widget = '162,34'


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
        elif qh.get_player_world_location('z') == 1 and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value,
                                                                       stairs2_id):
            osrs.move.right_click_v6(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs2_id)[0], 'Climb-up',
                                     qh.get_canvas())
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
    glories = [osrs.item_ids.AMULET_OF_GLORY6, osrs.item_ids.AMULET_OF_GLORY5,
               osrs.item_ids.AMULET_OF_GLORY4]
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
        elif qh.get_chat_options('Draynor Village') and (
                datetime.datetime.now() - last_d_vill_click).total_seconds() > 10:
            osrs.keeb.write(str(qh.get_chat_options('Draynor Village')))
            last_d_vill_click = datetime.datetime.now()
        elif qh.get_inventory(glories) and (
                datetime.datetime.now() - last_glory_click).total_seconds() > 4:
            res = osrs.move.right_click_v6(qh.get_inventory(glories),
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


def run_to_juliets_house():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if 3165 <= qh.get_player_world_location('x') <= 3174 and 3429 <= qh.get_player_world_location('y') <= 3438:
            break
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3169, 'y': 3433, 'z': 0})


def go_up_to_juliet():
    door_1_id = 11773
    stairs_1 = '11797'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    qh.set_player_world_location()
    qh.set_objects_v2(
        'wall',
        {door_1_id}
    )
    qh.set_objects_v2(
        'game',
        {stairs_1}
    )
    qh.set_npcs_by_name(['juliet'])
    qh.set_tiles({'3163,3434,0', '3157,3428,1'})
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            return
        door_1 = []
        door_2 = []
        door_3 = []
        if qh.get_objects_v2('wall', door_1_id):
            door_1 = list(filter(lambda door: door['x_coord'] == 3165 and door['y_coord'] == 3433,
                                 qh.get_objects_v2('wall', door_1_id)))
            door_2 = list(filter(lambda door: door['x_coord'] == 3157 and door['y_coord'] == 3430,
                                 qh.get_objects_v2('wall', door_1_id)))
            door_3 = list(filter(lambda door: door['x_coord'] == 3158 and door['y_coord'] == 3426,
                                 qh.get_objects_v2('wall', door_1_id)))

        if (3165 <= qh.get_player_world_location('x') <= 3174
            and 3429 <= qh.get_player_world_location('y') <= 3438) and door_1:
            osrs.move.fast_click(door_1[0])
        elif (3165 <= qh.get_player_world_location('x') <= 3174
              and 3429 <= qh.get_player_world_location('y') <= 3438) and qh.get_tiles('3163,3434,0'):
            osrs.move.fast_click(qh.get_tiles('3163,3434,0'))
        elif (3156 <= qh.get_player_world_location('x') <= 3164
              and 3432 <= qh.get_player_world_location('y') <= 3439) and qh.get_objects_v2('game', stairs_1):
            osrs.move.fast_click(qh.get_objects_v2('game', stairs_1)[0])
        elif (qh.get_player_world_location('z') == 1 and 3151 <= qh.get_player_world_location('x') <= 3158
              and 3431 <= qh.get_player_world_location('y') <= 3439) and door_2:
            osrs.move.fast_click(door_2[0])
        elif (qh.get_player_world_location('z') == 1 and 3151 <= qh.get_player_world_location('x') <= 3158
              and 3431 <= qh.get_player_world_location('y') <= 3439) and qh.get_tiles('3157,3428,1'):
            osrs.move.fast_click(qh.get_tiles('3157,3428,1'))
        elif (qh.get_player_world_location('z') == 1 and 3153 <= qh.get_player_world_location('x') <= 3159
              and 3427 <= qh.get_player_world_location('y') <= 3430) and door_3:
            osrs.move.fast_click(door_3[0])
        elif (qh.get_player_world_location('z') == 1 and 3153 <= qh.get_player_world_location('x') <= 3159
              and 3427 <= qh.get_player_world_location('y') <= 3430) and qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3167, 'y': 3433, 'z': 0})


def go_to_father_lawrence():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name(['father lawrence'])
    qh.set_widgets({main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            return
        elif qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3254, 'y': 3482, 'z': 0})


def go_to_apothecary():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name(['apothecary'])
    qh.set_widgets({main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            return
        elif qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3190, 'y': 3403, 'z': 0})


def find_and_talk_to_npc(npc, x, y):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name([npc])
    qh.set_widgets({main_chat_widget})
    time_with_chat_menu = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            if (datetime.datetime.now() - time_with_chat_menu).total_seconds() > 3:
                return
        else:
            time_with_chat_menu = datetime.datetime.now()

        if (qh.get_npcs_by_name()
                and not (qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden'])):
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif not qh.get_npcs_by_name():
            osrs.move.follow_path(qh.get_player_world_location(), {'x': x, 'y': y, 'z': 0}, right_click=True)


def enter_morgans_house():
    door_1_id = 1535
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    qh.set_player_world_location()
    qh.set_objects_v2(
        'wall',
        {door_1_id}
    )
    qh.set_npcs_by_name(['morgan'])
    qh.set_tiles({'3096,3269,0'})
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            return
        door_1 = []
        if qh.get_objects_v2('wall', door_1_id):
            door_1 = list(filter(lambda door: door['x_coord'] == 3098 and door['y_coord'] == 3270,
                                 qh.get_objects_v2('wall', door_1_id)))

        if (3090 <= qh.get_player_world_location('x') <= 3110 and 3267 <= qh.get_player_world_location(
                'y') <= 3280) and door_1:
            osrs.move.fast_click(door_1[0])
        elif (3096 <= qh.get_player_world_location('x') <= 3103 and 3271 <= qh.get_player_world_location(
                'y') <= 3273) and qh.get_tiles('3096,3269,0'):
            osrs.move.fast_click(qh.get_tiles('3096,3269,0'))
        elif (3096 <= qh.get_player_world_location('x') <= 3102
              and 3266 <= qh.get_player_world_location('y') <= 3270) and qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3100, 'y': 3273, 'z': 0})


def walk_to_draynor_manor():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if 3105 <= qh.get_player_world_location('x') <= 3110 and 3349 <= qh.get_player_world_location('y') <= 3353:
            break
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3108, 'y': 3352, 'z': 0})


def draynor_manor_basement():
    stairs_id = 2616
    door_1_id = 134
    inner_door_id = 11470
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    qh.set_player_world_location()
    qh.set_objects_v2(
        'wall',
        {door_1_id, inner_door_id}
    )
    qh.set_objects_v2(
        'game',
        {stairs_id}
    )
    qh.set_tiles({'3106,3361,0', '3116,3364,0'})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') > 5000:
            return
        inner_door_1 = list(filter(lambda door: door['x_coord'] == 3109 and door['y_coord'] == 3358,
                                   qh.get_objects_v2('wall', inner_door_id)))
        inner_door_2 = list(filter(lambda door: door['x_coord'] == 3106 and door['y_coord'] == 3368,
                                   qh.get_objects_v2('wall', inner_door_id)))

        if qh.get_player_world_location('y') <= 3353 and qh.get_objects_v2('wall', door_1_id):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_1_id)[0])
        elif 3105 <= qh.get_player_world_location('x') <= 3112 and 3354 <= qh.get_player_world_location('y') <= 3357:
            if inner_door_1:
                osrs.move.fast_click(inner_door_1[0])
            elif qh.get_tiles('3106,3361,0'):
                osrs.move.fast_click(qh.get_tiles('3106,3361,0'))
        elif 3105 <= qh.get_player_world_location('x') <= 3112 and 3358 <= qh.get_player_world_location('y') <= 3368:
            if inner_door_2:
                osrs.move.fast_click(inner_door_2[0])
            elif qh.get_tiles('3116,3364,0'):
                osrs.move.fast_click(qh.get_tiles('3116,3364,0'))
        elif qh.get_objects_v2('game', stairs_id):
            osrs.move.fast_click(qh.get_objects_v2('game', stairs_id)[0])


def walk_to_ge():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if 3155 <= qh.get_player_world_location('x') <= 3162 and 3485 <= qh.get_player_world_location('y') <= 3495:
            break
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3160, 'y': 3489, 'z': 0})


def tab_to_fally():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    last_tab = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        # in varrock center
        if 2958 <= qh.get_player_world_location('x') <= 2968 and 3370 <= qh.get_player_world_location(
                'y') <= 3390:
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            return
        elif qh.get_inventory(osrs.item_ids.FALADOR_TELEPORT) and (
                datetime.datetime.now() - last_tab).total_seconds() > 10:
            osrs.move.click(qh.get_inventory(osrs.item_ids.FALADOR_TELEPORT))
            last_tab = datetime.datetime.now()


def walk_to_loc(x_min, x_max, y_min, y_max, dest_x, dest_y, dest_z=0):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if x_min <= qh.get_player_world_location('x') <= x_max and y_min <= qh.get_player_world_location('y') <= y_max:
            break
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': dest_x, 'y': dest_y, 'z': dest_z})


def enter_dorics():
    door_1_id = 1535
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    qh.set_player_world_location()
    qh.set_objects_v2(
        'wall',
        {door_1_id}
    )
    qh.set_npcs_by_name(['doric'])
    qh.set_tiles({'2952,3450,0'})
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            return

        if (2944 <= qh.get_player_world_location('x') <= 2949 and 3449 <= qh.get_player_world_location(
                'y') <= 3454) and qh.get_objects_v2('wall', door_1_id):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_1_id)[0])
        elif (2944 <= qh.get_player_world_location('x') <= 2949 and 3449 <= qh.get_player_world_location(
                'y') <= 3454) and qh.get_tiles('2952,3450,0'):
            osrs.move.fast_click(qh.get_tiles('2952,3450,0'))
        elif (2950 <= qh.get_player_world_location('x') <= 2953
              and 3449 <= qh.get_player_world_location('y') <= 3452) and qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])


def leave_dorics():
    door_1_id = 1535
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    qh.set_player_world_location()
    qh.set_objects_v2(
        'wall',
        {door_1_id}
    )
    qh.set_npcs_by_name(['doric'])
    qh.set_tiles({'2946,3451,0'})
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            return

        if (2950 <= qh.get_player_world_location('x') <= 2953
            and 3449 <= qh.get_player_world_location('y') <= 3452) and qh.get_objects_v2('wall', door_1_id):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_1_id)[0])
        elif (2950 <= qh.get_player_world_location('x') <= 2953
              and 3449 <= qh.get_player_world_location('y') <= 3452) and qh.get_tiles('2946,3451,0'):
            osrs.move.fast_click(qh.get_tiles('2946,3451,0'))
        elif (2944 <= qh.get_player_world_location('x') <= 2949 and 3449 <= qh.get_player_world_location(
                'y') <= 3454):
            return


def enter_goblin_hall():
    door_1_id = 12446
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    qh.set_player_world_location()
    qh.set_objects_v2(
        'wall',
        {door_1_id}
    )
    qh.set_npcs_by_name(['general wartface'])
    qh.set_tiles({'2956,3512,0'})
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            return

        if (2954 <= qh.get_player_world_location('x') <= 2961 and 3500 <= qh.get_player_world_location(
                'y') <= 3509) and qh.get_objects_v2('wall', door_1_id):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_1_id)[0])
        elif (2954 <= qh.get_player_world_location('x') <= 2961 and 3500 <= qh.get_player_world_location(
                'y') <= 3509) and qh.get_tiles('2956,3512,0'):
            osrs.move.fast_click(qh.get_tiles('2956,3512,0'))
        elif (2954 <= qh.get_player_world_location('x') <= 2961
              and 3510 <= qh.get_player_world_location('y') <= 3514) and qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])


def fally_to_tav_gate():
    door_1_id = 1727
    intermediate_tile = '2932,3451,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    qh.set_player_world_location()
    qh.set_objects_v2(
        'wall',
        {door_1_id}
    )
    qh.set_tiles({intermediate_tile})
    while True:
        qh.query_backend()

        if (2936 <= qh.get_player_world_location('x') <= 2950
            and 3448 <= qh.get_player_world_location('y') <= 3454) and qh.get_objects_v2('wall', door_1_id):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_1_id)[0])
        elif (2936 <= qh.get_player_world_location('x') <= 2950
              and 3448 <= qh.get_player_world_location('y') <= 3454) and qh.get_tiles(intermediate_tile):
            osrs.move.fast_click(qh.get_tiles(intermediate_tile))
        elif qh.get_player_world_location('x') <= 2935:
            return


def tab_to_lumby():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    last_tab = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        # in lum center
        if 3207 <= qh.get_player_world_location('x') <= 3230 and 3204 <= qh.get_player_world_location(
                'y') <= 3232:
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            return
        elif qh.get_inventory(osrs.item_ids.LUMBRIDGE_TELEPORT) and (
                datetime.datetime.now() - last_tab).total_seconds() > 10:
            osrs.move.click(qh.get_inventory(osrs.item_ids.LUMBRIDGE_TELEPORT))
            last_tab = datetime.datetime.now()


def talk_to_lumby_duke():
    stairs_up_1_id = '16671'
    door = 1543
    lum_top_floor_bank_tile = '3208,3221,2'
    lum_top_floor_bank_id = '18491'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'3205,3208,0', '3205,3208,1', lum_top_floor_bank_tile},
        {stairs_up_1_id, lum_top_floor_bank_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_npcs_by_name(['duke horacio'])
    qh.set_objects_v2('wall', {door})
    qh.set_canvas()
    qh.set_widgets({main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget):
            return
        elif qh.get_objects_v2('wall', door, 3):
            osrs.move.fast_click(qh.get_objects_v2('wall', door, 3)[0])
        elif qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif qh.get_player_world_location('z') == 1:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 3207, 'y': 3222, 'z': 1})
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_1_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_up_1_id)[0])


def necklace_of_passage_tele_wiz_tower():
    necklace_ids = [
            osrs.item_ids.NECKLACE_OF_PASSAGE5,
            osrs.item_ids.NECKLACE_OF_PASSAGE4,
            osrs.item_ids.NECKLACE_OF_PASSAGE3,
            osrs.item_ids.NECKLACE_OF_PASSAGE2,
            osrs.item_ids.NECKLACE_OF_PASSAGE1,
        ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_chat_options()
    click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 3093 <= qh.get_player_world_location('x') <= 3124 and 3145 <= qh.get_player_world_location('y') <= 3190:
            return
        elif qh.get_chat_options("wizards' tower"):
            osrs.keeb.write(str(qh.get_chat_options("wizards' tower")))
        elif qh.get_inventory(necklace_ids) and (datetime.datetime.now() - click).total_seconds() > 10:
            osrs.move.right_click_v6(qh.get_inventory(necklace_ids), 'Rub', qh.get_canvas(), in_inv=True)
            click = datetime.datetime.now()


def necklace_of_passage_tele_outpost():
    necklace_ids = [
            osrs.item_ids.NECKLACE_OF_PASSAGE5,
            osrs.item_ids.NECKLACE_OF_PASSAGE4,
            osrs.item_ids.NECKLACE_OF_PASSAGE3,
            osrs.item_ids.NECKLACE_OF_PASSAGE2,
            osrs.item_ids.NECKLACE_OF_PASSAGE1,
        ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_chat_options()
    click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 2425 <= qh.get_player_world_location('x') <= 2450 and 3340 <= qh.get_player_world_location('y') <= 3350:
            return
        elif qh.get_chat_options("the outpost"):
            osrs.keeb.write(str(qh.get_chat_options("the outpost")))
        elif qh.get_inventory(necklace_ids) and (datetime.datetime.now() - click).total_seconds() > 10:
            osrs.move.right_click_v6(qh.get_inventory(necklace_ids), 'Rub', qh.get_canvas(), in_inv=True)
            click = datetime.datetime.now()


def games_neck_to_barb():
    necklace_ids = [
            osrs.item_ids.GAMES_NECKLACE8,
            osrs.item_ids.GAMES_NECKLACE7,
            osrs.item_ids.GAMES_NECKLACE6,
            osrs.item_ids.GAMES_NECKLACE5,
            osrs.item_ids.GAMES_NECKLACE4,
            osrs.item_ids.GAMES_NECKLACE3,
            osrs.item_ids.GAMES_NECKLACE2,
            osrs.item_ids.GAMES_NECKLACE1,
        ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_chat_options()
    click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 2516 <= qh.get_player_world_location('x') <= 2528 and 3563 <= qh.get_player_world_location('y') <= 3578:
            return
        elif qh.get_chat_options("barbarian outpost."):
            osrs.keeb.write(str(qh.get_chat_options("barbarian outpost.")))
        elif qh.get_inventory(necklace_ids) and (datetime.datetime.now() - click).total_seconds() > 10:
            osrs.move.right_click_v6(qh.get_inventory(necklace_ids), 'Rub', qh.get_canvas(), in_inv=True)
            click = datetime.datetime.now()


def games_neck_to_burthorpe():
    necklace_ids = [
            osrs.item_ids.GAMES_NECKLACE8,
            osrs.item_ids.GAMES_NECKLACE7,
            osrs.item_ids.GAMES_NECKLACE6,
            osrs.item_ids.GAMES_NECKLACE5,
            osrs.item_ids.GAMES_NECKLACE4,
            osrs.item_ids.GAMES_NECKLACE3,
            osrs.item_ids.GAMES_NECKLACE2,
            osrs.item_ids.GAMES_NECKLACE1,
        ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_chat_options()
    click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 2884 <= qh.get_player_world_location('x') <= 2913 and 3549 <= qh.get_player_world_location('y') <= 3578:
            return
        elif qh.get_chat_options("burth", fuzzy=True):
            osrs.keeb.write(str(qh.get_chat_options("burth", fuzzy=True)))
        elif qh.get_inventory(necklace_ids) and (datetime.datetime.now() - click).total_seconds() > 10:
            osrs.move.right_click_v6(qh.get_inventory(necklace_ids), 'Rub', qh.get_canvas(), in_inv=True)
            click = datetime.datetime.now()


def dueling_to_c_wars():
    necklace_ids = [
            osrs.item_ids.RING_OF_DUELING8,
            osrs.item_ids.RING_OF_DUELING7,
            osrs.item_ids.RING_OF_DUELING6,
            osrs.item_ids.RING_OF_DUELING5,
            osrs.item_ids.RING_OF_DUELING4,
            osrs.item_ids.RING_OF_DUELING3,
            osrs.item_ids.RING_OF_DUELING2,
            osrs.item_ids.RING_OF_DUELING1,
        ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_chat_options()
    click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 2434 <= qh.get_player_world_location('x') <= 2447 and 3081 <= qh.get_player_world_location('y') <= 3098:
            return
        elif qh.get_chat_options("castle wars", fuzzy=True):
            osrs.keeb.write(str(qh.get_chat_options("castle wars", fuzzy=True)))
        elif qh.get_inventory(necklace_ids) and (datetime.datetime.now() - click).total_seconds() > 10:
            osrs.move.right_click_v6(qh.get_inventory(necklace_ids), 'Rub', qh.get_canvas(), in_inv=True)
            click = datetime.datetime.now()


def walk_out_of_c_wars():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'2446,3090,0'})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2445:
            return
        elif qh.get_tiles('2446,3090,0'):
            osrs.move.fast_click(qh.get_tiles('2446,3090,0'))


def tab_to_ardy():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    last_tab = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        # in lum center
        if 2651 <= qh.get_player_world_location('x') <= 2672 and 3294 <= qh.get_player_world_location(
                'y') <= 3318:
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            return
        elif qh.get_inventory(osrs.item_ids.ARDOUGNE_TELEPORT) and (
                datetime.datetime.now() - last_tab).total_seconds() > 10:
            osrs.move.click(qh.get_inventory(osrs.item_ids.ARDOUGNE_TELEPORT))
            last_tab = datetime.datetime.now()