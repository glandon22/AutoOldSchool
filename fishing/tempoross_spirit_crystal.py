import datetime

import osrs

north_totem_id = 41354
left_mast_id = 41352
south_totem_id = 41355
right_mast_id = 41353
ground_fire_id = 37582
intensity_widget_id = '437,55'
essence_widget_id = '437,45'
energy_widget_id = '437,35'

logger = osrs.dev.instantiate_logger()


def click_ladder():
    logger.info('Clicking ladder to board ship.')
    ladder_id = '41305'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects(
        {'3135,2840,0'},
        {ladder_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_id):
        osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ladder_id)[0])
    else:
        osrs.move.follow_path(qh.get_player_world_location(), {'x': 3135, 'y': 2840, 'z': 0})


def determine_side():
    logger.info('Determining which ship we are on.')
    bucket_bin_id = '40966'
    water_spout_id = '41000'
    while True:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_inventory()
        qh.query_backend()
        tiles = osrs.util.generate_surrounding_tiles_from_point(10, qh.get_player_world_location())
        qh.set_objects(
            set(tiles),
            {bucket_bin_id, water_spout_id},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, bucket_bin_id) and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, water_spout_id):
            logger.info('On ship, found buckets.')
            # there are multiple places to get buckets
            buckets = osrs.util.find_closest_target(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, bucket_bin_id))
            tap = qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, water_spout_id)[0]
            osrs.move.interact_with_object(
                40966, 'x', 1, False, custom_exit_function=have_buckets,
                obj_dist=9, right_click_option='Take'
            )
            if buckets['y_coord'] > tap['y_coord']:
                logger.info('Playing on left side.')
                return {'side': 'L', 'x': buckets['x_coord'], 'y': buckets['y_coord']}
            else:
                logger.info('Playing on right side.')
                return {'side': 'R', 'x': buckets['x_coord'], 'y': buckets['y_coord']}


def have_buckets():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if (
            osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.ItemIDs.BUCKET.value) +
            osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.ItemIDs.BUCKET_OF_WATER.value) >= 2
    ):
        return True


def cast_humidify():
    logger.info('Casting humidify.')
    humidify_icon_id = '218,110'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({humidify_icon_id})
    osrs.keeb.press_key('f6')
    osrs.keeb.press_key('esc')
    while True:
        qh.query_backend()
        osrs.keeb.press_key('f6')
        if qh.get_widgets(humidify_icon_id):
            osrs.move.fast_click(qh.get_widgets(humidify_icon_id))
            osrs.keeb.press_key('esc')
            return


def build_tiles(area_info):
    logger.info('Building reference tile strings.')
    output = {
        'cannon': None,
        'spirit': None,
        'spots': None,
        'midway': None
    }
    if area_info['side'] == 'L':
        output['cannon'] = f'{area_info["x"] + 3},{area_info["y"] - 1},0'
        output['spirit'] = f'{area_info["x"] + 14},{area_info["y"] + 5},0'
        output['spots'] = f'{area_info["x"] + 13},{area_info["y"] + 16},0'
        output['midway'] = f'{area_info["x"] + 9},{area_info["y"] + 7},0'
    else:
        output['cannon'] = f'{area_info["x"] - 3},{area_info["y"] + 1},0'
        output['spirit'] = f'{area_info["x"] - 14},{area_info["y"] - 5},0'
        output['spots'] = f'{area_info["x"] - 18},{area_info["y"] - 16},0'
        output['midway'] = f'{area_info["x"] - 8},{area_info["y"] - 6},0'
    return output


def untether():
    logger.info('Unexpectedly tethered, untethering!')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_spot_anims()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        qh.clear_objects(osrs.queryHelper.ObjectTypes.GAME.value)
        nearby_tiles = osrs.util.generate_surrounding_tiles_from_point(10, qh.get_player_world_location())
        qh.set_objects(
            set(nearby_tiles),
            {north_totem_id, south_totem_id, left_mast_id, right_mast_id},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.query_backend()
        if 1846 in qh.get_spot_anims() or len(qh.get_spot_anims()) == 0:
            return
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value):
            all_objs = osrs.util.combine_objects(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value))
            closest = osrs.util.find_closest_target(all_objs)
            if closest:
                osrs.move.fast_click(closest)


def have_tethered():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_spot_anims()
    qh.set_inventory()
    qh.query_backend()
    if 1845 in qh.get_spot_anims() or 1844 in qh.get_spot_anims():
        logger.info('Successfully tethered for big wave.')
        return True
    elif 7211 in qh.get_spot_anims() or 534 in qh.get_spot_anims():
        logger.warn('failed to tether, washed.')
        return True


def have_untethered():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_spot_anims()
    qh.query_backend()
    if len(qh.get_spot_anims()) == 0:
        logger.info('Successfully untethered after timeout for big wave.')
        return True


def tether_handler_v2(area_info):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['first mate deri', 'captain dudi', 'first mate peri', 'captain pudi'])
    qh.set_inventory()
    qh.set_spot_anims()
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_npcs_by_name():
        deri = qh.get_npcs_by_name()[0]
        if 'overheadText' in deri and 'drawing in water' in deri['overheadText']:
            logger.info('Tempoross is drawing in water.')
            osrs.move.interact_with_multiple_objects(
                {north_totem_id, south_totem_id, left_mast_id, right_mast_id}, 'x', 1, False,
                custom_exit_function=have_tethered, right_click_option='Tether'
            )
            wait_start = datetime.datetime.now()
            while True:
                qh.query_backend()
                if len(qh.get_spot_anims()) == 0:
                    logger.info('successfully handled wave, exiting.')
                    return
                elif (datetime.datetime.now() - wait_start).total_seconds() > 10:
                    logger.warn('failed to handle a colossal wave, timed out.')
                    break
            osrs.move.interact_with_multiple_objects(
                {north_totem_id, south_totem_id, left_mast_id, right_mast_id}, 'x',
                1, False,
                custom_exit_function=have_untethered, right_click_option='Untether', timeout=5
            )


def tempoross_state_parser(qh: osrs.queryHelper.QueryHelper):
    logger.info('parsing tempoross energy, essence, and storm intensity.')
    try:
        intensity_widget_id = '437,55'
        essence_widget_id = '437,45'
        energy_widget_id = '437,35'
        output = []
        for stat in [intensity_widget_id, essence_widget_id, energy_widget_id]:
            stat = qh.get_widgets(stat)
            if not stat:
                stat = None
            else:
                stat = int(stat['text'].split(': ')[1][:-1])
            output.append(stat)
        return {
            'intensity': output[0],
            'essence': output[1],
            'energy': output[2],
        }
    except Exception as e:
        print('couldnt parse the tempoross state', e)
        return {
            'energy': None,
            'intensity': None,
            'essence': None
        }


def ground_fire_handler(qh: osrs.queryHelper.QueryHelper):
    if qh.get_objects_v2('game', ground_fire_id, dist=5):
        if not qh.get_inventory(osrs.item_ids.ItemIDs.BUCKET_OF_WATER.value):
            logger.warn('fire on the ground but dont have any buckets of water.')
            return
        c = osrs.util.find_closest_target(qh.get_objects_v2('game', ground_fire_id, dist=5))
        if c:
            osrs.move.fast_click(c)
            qh.query_backend()
            return True


def fish_catching_handler(qh, important_area_tiles, area_info):
    while True:
        tether_handler_v2(area_info)
        qh.query_backend()
        found_fire = ground_fire_handler(qh)
        if found_fire:
            continue
        if qh.get_interating_with():
            return
        if 3136 <= qh.get_player_world_location('x') <= 3163 and 2835 <= qh.get_player_world_location('y') <= 2845:
            return logger.info('game is over')
        if qh.get_npcs_by_name():
            closest = osrs.util.find_closest_target(qh.get_npcs_by_name())
            # if the fish spot is not clickable, this will fall through and click a tile to get closer to the spots
            # otherwise, continue on from loop
            if closest and osrs.move.is_clickable(closest):
                osrs.move.fast_click(closest)
                continue

        if qh.get_tiles(important_area_tiles['spots']) and osrs.move.is_clickable(
                qh.get_tiles(important_area_tiles['spots'])):
            osrs.keeb.press_key('space')
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['spots']))
        elif qh.get_tiles(important_area_tiles['midway']) and osrs.move.is_clickable(
                qh.get_tiles(important_area_tiles['midway'])):
            osrs.keeb.press_key('space')
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['midway']))


def game_over(state):
    return ('intensity' in state and state['intensity'] is None and
        'essence' in state and state['essence'] is None and
            'energy' in state and state['energy'] is None)


def leave_game():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['first mate deri', 'first mate peri'])
    qh.set_player_world_location()
    qh.set_canvas()
    while True:
        qh.query_backend()
        if 3136 <= qh.get_player_world_location('x') <= 3163 and 2835 <= qh.get_player_world_location('y') <= 2845:
            return
        elif qh.get_npcs_by_name():
            osrs.move.right_click_v6(
                qh.get_npcs_by_name()[0],
                'Leave',
                qh.get_canvas(),
                in_inv=True
            )


def tempoross_handler():
    bucket_of_water_id = '1929'
    bucket_id = '1925'
    area_info = determine_side()
    important_area_tiles = build_tiles(area_info)
    qh = osrs.queryHelper.QueryHelper()
    qh.set_is_fishing()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_spot_anims()
    qh.set_widgets({intensity_widget_id, essence_widget_id, energy_widget_id})
    qh.set_npcs_by_name(['fishing spot'])
    qh.set_tiles({
        important_area_tiles['cannon'],
        important_area_tiles['spirit'],
        important_area_tiles['spots'],
        important_area_tiles['midway'],
    })
    qh.set_interating_with()
    qh.set_objects_v2('game', {ground_fire_id})
    qh.query_backend()
    last_humidify = datetime.datetime.now() - datetime.timedelta(hours=1)
    game_start = datetime.datetime.now()
    osrs.keeb.press_key('esc')
    while True:
        qh.query_backend()
        tempoross_state = tempoross_state_parser(qh)
        ground_fire_handler(qh)
        tether_handler_v2(area_info)
        if 3136 <= qh.get_player_world_location('x') <= 3163 and 2835 <= qh.get_player_world_location('y') <= 2845:
            return logger.info('game is over')
        elif game_over(tempoross_state) and (datetime.datetime.now() - game_start).total_seconds() > 30:
            logger.info('tempoross down, game is over')
            return leave_game()

        if 'energy' in tempoross_state and type(tempoross_state['energy']) is int and tempoross_state['energy'] < 7:
            logger.info('Spirit pool is nearly active, heading there.')
            fish_spirit_pool(important_area_tiles)
            continue
        if not qh.get_inventory(bucket_of_water_id) and qh.get_inventory(bucket_id) and (datetime.datetime.now() - last_humidify).total_seconds() > 4:
            cast_humidify()
            last_humidify = datetime.datetime.now()
            continue
        # tempoross is injured and energy is low - about to have spirit pool open for the last time - dump bag
        if (
                tempoross_state['energy']
                and tempoross_state['essence']
                and tempoross_state['energy'] <= 29
                and tempoross_state['essence'] != 100
        ) \
                or (qh.get_inventory() and len(qh.get_inventory()) == 28):
            logger.info('Heading to ship to shoot fish at tempoross')
            shoot_fish(important_area_tiles, area_info)
            continue
        if (not qh.get_interating_with() or 'Fishing spot' not in qh.get_interating_with()) and (tempoross_state['essence'] and tempoross_state['essence'] != 0):
            fish_catching_handler(qh, important_area_tiles, area_info)

# 7211 534


def shoot_fish(important_area_tiles, area_info):
    logger.info('shooting fish')
    fish_ids = [25564, 25566]
    ammo_crates_ids = {40968, 40969, 40970, 40971, ground_fire_id}
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_interating_with()
    qh.set_tiles({
        important_area_tiles['cannon'],
        important_area_tiles['spirit'],
        important_area_tiles['spots'],
        important_area_tiles['midway'],
    })
    qh.set_npcs(['10571'])
    qh.set_inventory()
    qh.set_objects_v2('game', ammo_crates_ids)
    while True:
        qh.query_backend()
        ground_fire_handler(qh)
        tether_handler_v2(area_info)
        if qh.get_npcs():
            logger.info('spirit pool came up while shooting fish, heading to spirit pool instead')
            # the spirit pool opened while i was doing this - fish that instead!!!
            return fish_spirit_pool(important_area_tiles)

        if qh.get_interating_with() and 'Ammunition' in qh.get_interating_with():
            logger.info('still loading crate')
            continue
        elif not qh.get_inventory(fish_ids):
            logger.info('inv is empty - done shooting fish')
            return
        if qh.get_objects_v2('game'):
            closest = osrs.util.find_closest_target(qh.get_objects_v2('game'))
            if closest and closest['dist'] < 5:
                osrs.move.fast_click(closest)
                logger.info('found a crate to load my fish - clicking')
                continue

        if qh.get_tiles(important_area_tiles['cannon']) and osrs.move.is_clickable(qh.get_tiles(important_area_tiles['cannon'])):
            osrs.keeb.press_key('space')
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['cannon']))
        elif qh.get_tiles(important_area_tiles['midway']) and osrs.move.is_clickable(qh.get_tiles(important_area_tiles['midway'])):
            osrs.keeb.press_key('space')
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['midway']))
        elif qh.get_tiles(important_area_tiles['spots']) and osrs.move.is_clickable(qh.get_tiles(important_area_tiles['spots'])):
            osrs.keeb.press_key('space')
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['spots']))


def fish_spirit_pool(important_area_tiles):
    logger.info('fishing spirit pool')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_is_fishing()
    qh.set_widgets({intensity_widget_id, essence_widget_id, energy_widget_id})
    qh.set_interating_with()
    qh.set_tiles({
        important_area_tiles['cannon'],
        important_area_tiles['spirit'],
        important_area_tiles['spots'],
        important_area_tiles['midway'],
    })
    qh.set_objects_v2('game', {ground_fire_id})
    qh.set_npcs(['10571'])
    have_fished = False
    last_pool_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    parsed_spirit_tile = important_area_tiles['spirit'].split(',')
    while True:
        qh.query_backend()
        tempoross_state = tempoross_state_parser(qh)
        ground_fire_handler(qh)
        if 3136 <= qh.get_player_world_location('x') <= 3163 and 2835 <= qh.get_player_world_location('y') <= 2845:
            logger.info('game ended while at spirit pool. ending function')
            return

        elif game_over(tempoross_state):
            logger.info('tempoross down, game is over')
            return

        if qh.get_interating_with() and 'Spirit pool' in qh.get_interating_with():
            print('qh', qh.get_interating_with())
            logger.info('fishing')
            have_fished = True
            continue
        elif not qh.get_interating_with() and have_fished and not len(qh.get_npcs()):
            logger.info('spirit pool closed')
            return
        elif qh.get_npcs() and (datetime.datetime.now() - last_pool_click).total_seconds() > 3:
            closest = osrs.util.find_closest_target(qh.get_npcs())
            if closest:
                osrs.move.fast_click(closest)
                logger.info('clicking spirit pool')
                last_pool_click = datetime.datetime.now()
        elif osrs.dev.point_dist(
                qh.get_player_world_location('x'), qh.get_player_world_location('y'), int(parsed_spirit_tile[0]), int(parsed_spirit_tile[1])
        ) > 3:
            if qh.get_tiles(important_area_tiles['spirit']) and osrs.move.is_clickable(
                    qh.get_tiles(important_area_tiles['spirit'])):
                osrs.move.fast_click(qh.get_tiles(important_area_tiles['spirit']))
            elif qh.get_tiles(important_area_tiles['midway']) and osrs.move.is_clickable(
                    qh.get_tiles(important_area_tiles['midway'])):
                osrs.move.fast_click(qh.get_tiles(important_area_tiles['midway']))
            elif qh.get_tiles(important_area_tiles['spots']) and osrs.move.is_clickable(
                    qh.get_tiles(important_area_tiles['spots'])):
                osrs.move.fast_click(qh.get_tiles(important_area_tiles['spots']))





script_config = {
    'intensity': 'high',
    'login': False,
    'logout': False
}


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    while True:
        qh.query_backend()
        if 3125 <= qh.get_player_world_location('x') <= 3135:
            logger.info('waiting for game')
            continue
        elif qh.get_player_world_location('x') > 5000:
            tempoross_handler()
        else:
            osrs.game.break_manager_v4(script_config)
            click_ladder()


main()

#I'm ready to leave.