import datetime

import osrs

north_totem_id = '41354'
left_mast_id = '41352'
south_totem_id = '41355'
right_mast_id = '41353'
ground_fire_id = '37582'

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
            logger.info('On ship, found buckets and ropes.')
            # there are multiple places to get buckets
            buckets = osrs.util.find_closest_target(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, bucket_bin_id))
            tap = qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, water_spout_id)[0]
            osrs.move.right_click_v4(buckets, 'Take-5')
            start_wait = datetime.datetime.now()
            while True:
                qh.query_backend()
                if qh.get_inventory('1925'):
                    break
                elif (datetime.datetime.now() - start_wait).total_seconds() > 7:
                    break
            if buckets['y_coord'] > tap['y_coord']:
                logger.info('Playing on left side.')
                return {'side': 'L', 'x': buckets['x_coord'], 'y': buckets['y_coord']}
            else:
                logger.info('Playing on right side.')
                return {'side': 'R', 'x': buckets['x_coord'], 'y': buckets['y_coord']}


def take_ropes():
    logger.info('Grabbing ropes.')
    ropes_id = '40965'
    rope = '954'
    while True:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_inventory()
        qh.query_backend()
        tiles = osrs.util.generate_surrounding_tiles_from_point(10, qh.get_player_world_location())
        qh.set_objects(
            set(tiles),
            {ropes_id},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ropes_id):
            while True:
                qh.query_backend()
                ropes = qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ropes_id)[0]
                if qh.get_inventory() and osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), rope) > 2:
                    return
                else:
                    osrs.move.fast_click(ropes)


def cast_humidify():
    logger.info('Casting humidify.')
    humidify_icon_id = '218,110'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({humidify_icon_id})
    osrs.keeb.press_key('f6')
    osrs.keeb.press_key('esc')
    qh.query_backend()
    osrs.keeb.press_key('f6')
    osrs.move.fast_click(qh.get_widgets(humidify_icon_id))
    osrs.keeb.press_key('esc')


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
        output['spots'] = f'{area_info["x"] + 13},{area_info["y"] + 18},0'
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


def tether_handler_v2():
    rope = '954'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['first mate deri', 'captain dudi', 'first mate peri', 'captain pudi'])
    qh.set_inventory()
    qh.set_spot_anims()
    qh.set_player_world_location()
    qh.query_backend()
    if not qh.get_inventory(rope):
        logger.info('no rope in inv, not trying to tether')
        return
    if qh.get_npcs_by_name():
        deri = qh.get_npcs_by_name()[0]
        if 'overheadText' in deri and 'drawing in water' in deri['overheadText']:
            logger.info('Tempoross is drawing in water.')
            wait_start = datetime.datetime.now()
            tethered = False
            while True:
                qh.clear_objects(osrs.queryHelper.ObjectTypes.GAME.value)
                nearby_tiles = osrs.util.generate_surrounding_tiles_from_point(10, qh.get_player_world_location())
                qh.set_objects(
                    set(nearby_tiles),
                    {north_totem_id, south_totem_id, left_mast_id, right_mast_id},
                    osrs.queryHelper.ObjectTypes.GAME.value
                )
                qh.query_backend()
                if (datetime.datetime.now() - wait_start).total_seconds() > 20:
                    logger.info('Timed out waiting for the the big wave.')
                    return
                if tethered and len(qh.get_spot_anims()) == 0:
                    logger.info('No longer tethered, ending function!')
                    return
                if 1845 in qh.get_spot_anims() or 1844 in qh.get_spot_anims():
                    logger.info('Successfully tethered for big wave.')
                    tethered = True
                    continue
                if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value) and not tethered:
                    logger.info('Not tethered - found a mast or totem.')
                    all_objs = osrs.util.combine_objects(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value))
                    closest = osrs.util.find_closest_target(all_objs)
                    if closest:
                        osrs.move.fast_click(closest)
                        logger.info('clicked tether point.')


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


def tempoross_handler():
    bucket_of_water_id = '1929'
    bucket_id = '1925'

    intensity_widget_id = '437,55'
    essence_widget_id = '437,45'
    energy_widget_id = '437,35'
    area_info = determine_side()
    take_ropes()
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
    qh.query_backend()
    last_humidify = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.clear_objects(osrs.queryHelper.ObjectTypes.GAME.value)
        nearby_tiles = osrs.util.generate_surrounding_tiles_from_point(10, qh.get_player_world_location())
        qh.set_objects(
            set(nearby_tiles),
            {ground_fire_id},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.query_backend()
        tempoross_state = tempoross_state_parser(qh)
        tether_handler_v2()
        if 3136 <= qh.get_player_world_location('x') <= 3163 and 2835 <= qh.get_player_world_location('y') <= 2845:
            return logger.info('game is over')
        # I am unexpectedly tethered to a mast or totem!
        if qh.get_spot_anims() and 1845 in qh.get_spot_anims():
            logger.info('unexpectedly tethered, calling untether logic!')
            untether()
            continue
        if tempoross_state['energy'] and tempoross_state['energy'] < 10:
            logger.info('Spirit pool is nearly active, heading there.')
            fish_spirit_pool(important_area_tiles)
            continue
        if not qh.get_inventory(bucket_of_water_id) and qh.get_inventory(bucket_id) and (datetime.datetime.now() - last_humidify).total_seconds() > 4:
            cast_humidify()
            last_humidify = datetime.datetime.now()
            continue
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ground_fire_id) and qh.get_inventory() and qh.get_inventory(bucket_of_water_id):
            logger.info('ground fire spotted, trying to put it out.')
            closest = osrs.util.find_closest_target(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ground_fire_id))
            if closest:
                osrs.move.fast_click(closest)
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
            shoot_fish(important_area_tiles)
            continue
        if (not qh.get_interating_with() or 'Fishing spot' not in qh.get_interating_with()) and (tempoross_state['essence'] and tempoross_state['essence'] != 0):
            logger.info('Need to fish - looking for spot')
            if qh.get_npcs_by_name():
                closest = osrs.util.find_closest_target(qh.get_npcs_by_name())
                # if the fish spot is not clickable, this will fall through and click a tile to get closer to the spots
                # otherwise, continue on from loop
                if closest and osrs.move.is_clickable(closest):
                    osrs.move.fast_click(closest)
                    have_fished = True
                    continue

            if qh.get_tiles(important_area_tiles['spots']) and osrs.move.is_clickable(qh.get_tiles(important_area_tiles['spots'])):
                osrs.move.fast_click(qh.get_tiles(important_area_tiles['spots']))
            elif qh.get_tiles(important_area_tiles['midway']) and osrs.move.is_clickable(qh.get_tiles(important_area_tiles['midway'])):
                osrs.move.fast_click(qh.get_tiles(important_area_tiles['midway']))
            continue


def shoot_fish(important_area_tiles):
    logger.info('shooting fish')
    bucket_of_water_id = '1929'
    fish_id = '25564'
    ammo_crates_ids = {'40968', '40969', '40970', '40971', ground_fire_id}
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
    while True:
        tether_handler_v2()
        qh.query_backend()
        if qh.get_npcs():
            logger.info('spirit pool came up while shooting fish, heading to spirit pool instead')
            # the spirit pool opened while i was doing this - fish that instead!!!
            return fish_spirit_pool(important_area_tiles)

        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ground_fire_id) and qh.get_inventory() and qh.get_inventory(bucket_of_water_id):
            closest = osrs.util.find_closest_target(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, ground_fire_id))
            if closest and 'dist' in closest and closest['dist'] <= 3:
                logger.info('fire on the ground close by, going to put it out.')
                osrs.move.fast_click(closest)
                continue

        if qh.get_interating_with() and 'Ammunition' in qh.get_interating_with():
            logger.info('still loading crate')
            continue
        elif not qh.get_inventory(fish_id):
            logger.info('inv is empty - done shooting fish')
            return
        qh.clear_objects(osrs.queryHelper.ObjectTypes.GAME.value)
        nearby_tiles = osrs.util.generate_surrounding_tiles_from_point(10, qh.get_player_world_location())
        qh.set_objects(
            set(nearby_tiles),
            ammo_crates_ids,
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value):
            crates = osrs.util.combine_objects(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value))
            closest = osrs.util.find_closest_target(crates)
            if closest:
                osrs.move.fast_click(closest)
                logger.info('found a crate to load my fish - clicking')
        elif qh.get_tiles(important_area_tiles['cannon']) and osrs.move.is_clickable(qh.get_tiles(important_area_tiles['cannon'])):
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['cannon']))
        elif qh.get_tiles(important_area_tiles['midway']) and osrs.move.is_clickable(qh.get_tiles(important_area_tiles['midway'])):
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['midway']))
        elif qh.get_tiles(important_area_tiles['spots']) and osrs.move.is_clickable(qh.get_tiles(important_area_tiles['spots'])):
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['spots']))


def fish_spirit_pool(important_area_tiles):
    logger.info('fishing spirit pool')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_is_fishing()
    qh.set_interating_with()
    qh.set_tiles({
        important_area_tiles['cannon'],
        important_area_tiles['spirit'],
        important_area_tiles['spots'],
        important_area_tiles['midway'],
    })
    qh.set_npcs(['10571'])
    have_fished = False
    parsed_spirit_tile = important_area_tiles['spirit'].split(',')
    while True:
        qh.query_backend()

        if 3136 <= qh.get_player_world_location('x') <= 3163 and 2835 <= qh.get_player_world_location('y') <= 2845:
            logger.info('game ended while at spirit pool. ending function')
            return

        if osrs.dev.point_dist(
                qh.get_player_world_location('x'), qh.get_player_world_location('y'), int(parsed_spirit_tile[0]), int(parsed_spirit_tile[1])
        ) < 3:
            logger.info('close to spirit pool - beginning to fish')
            break
        elif qh.get_tiles(important_area_tiles['spirit']) and osrs.move.is_clickable(
                qh.get_tiles(important_area_tiles['spirit'])):
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['spirit']))
        elif qh.get_tiles(important_area_tiles['midway']) and osrs.move.is_clickable(
                qh.get_tiles(important_area_tiles['midway'])):
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['midway']))
        elif qh.get_tiles(important_area_tiles['spots']) and osrs.move.is_clickable(
                qh.get_tiles(important_area_tiles['spots'])):
            osrs.move.fast_click(qh.get_tiles(important_area_tiles['spots']))
    last_pool_click = datetime.datetime.now() - datetime.timedelta(hours=12)
    while True:
        qh.query_backend()

        if 3136 <= qh.get_player_world_location('x') <= 3163 and 2835 <= qh.get_player_world_location('y') <= 2845:
            logger.info('game ended while at spirit pool - exiting')
            return

        if qh.get_interating_with():
            logger.info('fishing', qh.get_interating_with())
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


def empty_inv(qh):
    logger.info('cleaning up my inventory')
    bucket_of_water_id = '1929'
    bucket_id = '1925'
    rope_id = '954'
    if qh.get_inventory() and len(qh.get_inventory()) > 1:
        for item in qh.get_inventory():
            if str(item['id']) in [bucket_of_water_id, bucket_id, rope_id]:
                osrs.move.right_click_v5(item, 'Drop', in_inv=True)
        osrs.clock.sleep_one_tick()


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
            print('waiting for game')
            empty_inv(qh)
            continue
        elif qh.get_player_world_location('x') > 5000:
            tempoross_handler()
        else:
            empty_inv(qh)
            osrs.game.break_manager_v4(script_config)
            click_ladder()


main()
