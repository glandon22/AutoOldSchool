import datetime

import osrs


# osrs.move.follow_path(qh.get_player_world_location(), osrs.models.tile(3182, 3434, 0).dict)
# Objects I click to start an herbi hunt
run_energy_widget_id = '160,28'
bank_dump_widget_id = '12,42'
fancy_restore_pool_id = '29241'
mounted_digsite_pendant_id = '33417'
mush_tree_tile = '3765,3880,1'
mush_meadow_button_id = '608,15'

stam_pot_ids = [
    12625,
    12627,
    12629,
    12631
]

trail_start_objects = [
    {
        'x': 3686,
        'y': 3870,
        'z': 0
    },
    {
        'x': 3695,
        'y': 3800,
        'z': 0
    },
    {
        'x': 3704,
        'y': 3810,
        'z': 0
    },
    {
        'x': 3705,
        'y': 3830,
        'z': 0
    },
    {
        'x': 3751,
        'y': 3850,
        'z': 0
    },
]
herbi_rock_1_id = '30519'
herbi_rock_1_tile = '3686,3870,0'

herbi_mushroom_1_id = '30520'
herbi_mushroom_1_tile = '3695,3800,0'

herbi_rock_2_id = '30521'
herbi_rock_2_tile = '3704,3810,0'

herbi_rock_3_id = '30522' ####################
herbi_rock_3_tile = '3705,3830,0'

herbi_wood_1_id = '30523'
herbi_wood_1_tile = '3751,3850,0'

herbi_caught_npc_id = '7785'
varrock_tele_widget_id = '218,23'
trail_start_ids = {herbi_rock_1_id, herbi_mushroom_1_id, herbi_rock_2_id, herbi_rock_3_id, herbi_wood_1_id}
trail_start_tiles = {herbi_rock_1_tile, herbi_mushroom_1_tile, herbi_rock_2_tile, herbi_rock_3_tile, herbi_wood_1_tile}

herb_sack_id = '13226'
mush_tree_id = '30920'

var_west_bank_id = '10583'
var_west_bank_tile_ids = {'3186,3438,0', '3186,3440,0', '3186,3442,0'}


def mushtree_to_swamp():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_objects(
        {mush_tree_tile},
        {mush_tree_id}
    )
    qh.set_widgets({mush_meadow_button_id, bank_dump_widget_id})
    qh.set_player_world_location()
    osrs.dev.logger.info('searching for mushtree to travel to sticky swamp.')
    last_mushtree_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_swamp_press = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets(mush_meadow_button_id) and (datetime.datetime.now() - last_swamp_press).total_seconds() > 5:
            osrs.dev.logger.info('mushtree teleport menu open, selecting sticky swamp.')
            osrs.keeb.write('4')
            last_swamp_press = datetime.datetime.now()
        elif qh.get_player_world_location() and qh.get_player_world_location()['x'] < 3700:
            osrs.dev.logger.info('in mushroom meadow.')
            return
        elif qh.get_game_objects(mush_tree_id) and (datetime.datetime.now() - last_mushtree_click).total_seconds() > 8:
            osrs.move.click(qh.get_game_objects(mush_tree_id)[0])
            last_mushtree_click = datetime.datetime.now()
            osrs.dev.logger.info('Clicked mushtree.')


def start_herbi():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_herbiboar()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_objects(
        trail_start_tiles,
        trail_start_ids,
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    # make this a loop that has ability to walk to a start if there isnt one on screen
    while True:
        qh.query_backend()
        all_starts = osrs.util.combine_objects(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value))

        closest_start = osrs.util.find_closest_target(all_starts)
        if 'nextStop' in qh.get_herbiboar():
            return
        elif closest_start:
            osrs.move.fast_click(closest_start)
        else:
            closest_start = {
                'dist': 999,
                'point': None
            }
            for start in trail_start_objects:
                if osrs.dev.point_dist(qh.get_player_world_location('x'), qh.get_player_world_location('y'), start['x'], start['y']) < closest_start['dist']:
                    closest_start['dist'] = osrs.dev.point_dist(qh.get_player_world_location('x'), qh.get_player_world_location('y'), start['x'], start['y'])
                    closest_start['point'] = start
            if closest_start:
                # If i am in the upper right corner peninsula by the boat, my path will lead me to take the boat back
                # to the museum camp then run north. i dont want to do that
                if closest_start['dist'] > 30:
                    osrs.move.follow_path(
                        qh.get_player_world_location(),
                        {'x': 3700, 'y': 3845, 'z': 0}
                    )
                else:
                    osrs.move.follow_path(
                        qh.get_player_world_location(),
                        closest_start['point']
                    )


def catch_herbi_v2():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_herbiboar()
    qh.set_player_world_location()
    qh.set_npcs([herbi_caught_npc_id])
    qh.set_inventory()
    qh.set_canvas()
    qh.set_game_objects({'2965,3381,0'}, {'9250'})
    qh.set_widgets({run_energy_widget_id})
    qh.query_backend()
    target_object = None
    last_seen_stop = None
    # there seems to be one combination of trails that the herbiboar runelite plugin cant handle, and it gets stuck
    # leading you in a loop, so in case i draw this one particular trail set, i need to log out and reset the herbiboar
    cached_step = {
        'x': 0,
        'y': 0,
        'time': datetime.datetime.now()
    }
    while True:
        # ensure I am always running
        osrs.player.toggle_run('on')
        qh.query_backend()
        # If Herbi is out, pick heerbs and exit loop
        if qh.get_npcs():
            while True:
                qh.query_backend()
                if not qh.get_npcs():
                    osrs.move.click(qh.get_inventory(herb_sack_id))
                    return
                osrs.move.fast_click(qh.get_npcs()[0])
        herbi_data = qh.get_herbiboar()
        # {'x': 9664, 'y': 7616, 'id': 30533, 'x_coord': 3699, 'y_coord': 3875}
        # Determine if I am at the end of a trail or still following it
        '''
        TODO: I have seen the plugin mess up and get stuck in a loop, if i have clicked
        the same spot for more than a minute or two just log out and reset    
        '''
        if 'nextStop' in herbi_data:
            if cached_step['x'] != herbi_data['nextStop']['x_coord'] and cached_step['y'] != herbi_data['nextStop']['y_coord']:
                cached_step['x'] = herbi_data['nextStop']['x_coord']
                cached_step['y'] = herbi_data['nextStop']['y_coord']
                cached_step['time'] = datetime.datetime.now()
            elif (datetime.datetime.now() - cached_step['time']).total_seconds() > 60:
                print('im stuck on a step, log out and reset')
                osrs.game.logout()
                osrs.clock.random_sleep(10, 11)
                osrs.game.login_v4()
                return

            target_object = herbi_data['nextStop']
            last_seen_stop = datetime.datetime.now()
        # sometimes you fail to catch the herbiboar, make sure i dont get trapped in this loop waiting to see him
        # when he actually got away
        elif last_seen_stop and (datetime.datetime.now() - last_seen_stop).total_seconds() > 20:
            print('failed to catch, exiting!')
            return
        else:
            continue

        # Drink stam if necessary
        if qh.get_widgets(run_energy_widget_id) and int(qh.get_widgets(run_energy_widget_id)['text']) < 40:
            stam = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), stam_pot_ids)
            if stam:
                osrs.move.click(stam)

        # the target object data comes from the herbiboar plugin, which doesnt seem to consistently update the x,y
        # location on screen regularly enough. so it will appear to be off screen when it is actually clickable
        # to get around that, we will just look for the tile that we know we need to click
        # in order to have the most up to date screen locations
        target_tile = f"{target_object['x_coord']},{target_object['y_coord']},0"
        qh.set_tiles({target_tile})
        qh.query_backend()

        # my target is on screen click it, otherwise follow a path to it
        if osrs.move.is_clickable(qh.get_tiles(target_tile)):
            osrs.move.fast_click(qh.get_tiles(target_tile))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': target_object['x_coord'], 'y': target_object['y_coord'], 'z': 0})


def click_mounted_digsite_pendant():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_objects(
        {mush_tree_tile},
        {mush_tree_id}
    )
    qh.set_widgets({mush_meadow_button_id, bank_dump_widget_id, run_energy_widget_id})
    qh.set_player_world_location()
    qh.set_script_stats({'Status': 'Returning to Fossil Island.'})
    osrs.dev.logger.info('Looking for digsite pendant')
    tile_map = None
    last_pendant_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_pool_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') > 4000 and not tile_map:
            osrs.dev.logger.info('in house, generating tile map.')
            tile_map = osrs.util.generate_game_tiles_in_coords(
                qh.get_player_world_location('x') - 15,
                qh.get_player_world_location('x') + 15,
                qh.get_player_world_location('y') - 15,
                qh.get_player_world_location('y') + 15,
                1
            )
            qh.set_objects(set(tile_map), set(), osrs.queryHelper.ObjectTypes.DECORATIVE.value)
            qh.set_objects(set(tile_map), {fancy_restore_pool_id}, osrs.queryHelper.ObjectTypes.GAME.value)
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, fancy_restore_pool_id) and \
                (datetime.datetime.now() - last_pool_click).total_seconds() > 12 \
                and (qh.get_widgets(run_energy_widget_id) and int(qh.get_widgets(run_energy_widget_id)['text']) < 95):

            osrs.dev.logger.info('Click on ornate rejuvenation pool.')
            osrs.move.click(
                qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value)[fancy_restore_pool_id][0]
            )
            last_pool_click = datetime.datetime.now()
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.DECORATIVE.value, mounted_digsite_pendant_id) and \
                (datetime.datetime.now() - last_pendant_click).total_seconds() > 7 \
                and (qh.get_widgets(run_energy_widget_id) and int(qh.get_widgets(run_energy_widget_id)['text']) == 100):
            osrs.dev.logger.info('clicking on digsite pendant')
            osrs.move.click(
                qh.get_objects(osrs.queryHelper.ObjectTypes.DECORATIVE.value)[mounted_digsite_pendant_id][0]
            )
            last_pendant_click = datetime.datetime.now()
        elif 3840 < qh.get_player_world_location('y') < 3900:
            osrs.dev.logger.info('successfully teleported to fossil island.')
            return


def bank_in_varrock():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_objects(
        var_west_bank_tile_ids,
        {var_west_bank_id}
    )
    qh.set_widgets({varrock_tele_widget_id, bank_dump_widget_id})
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_bank()
    qh.set_script_stats({'status': 'Banking.'})
    osrs.dev.logger.info('beginning banking sequence.')
    last_tele_attempt = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 3420 < qh.get_player_world_location('y') < 3440 and 3203 < qh.get_player_world_location('x') < 3222:
            osrs.dev.logger.info('arrived in varrock.')
            break
        elif (datetime.datetime.now() - last_tele_attempt).total_seconds() > 7:
            osrs.game.cast_spell(varrock_tele_widget_id)
            last_tele_attempt = datetime.datetime.now()
            osrs.dev.logger.info('teleported to varrock')
    last_bank_booth_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, var_west_bank_id) and (datetime.datetime.now() - last_bank_booth_click).total_seconds() > 15:
            closest = osrs.util.find_closest_target(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, var_west_bank_id))
            if closest:
                osrs.move.click(closest)
                last_bank_booth_click = datetime.datetime.now()
                osrs.dev.logger.info(f'clicked bank booth: {closest}')
        elif qh.get_widgets(bank_dump_widget_id):
            osrs.dev.logger.info('bank interface opened.')
            break
    while True:
        qh.query_backend()
        if qh.get_inventory(herb_sack_id):
            osrs.move.right_click_v3(qh.get_inventory(herb_sack_id), 'Empty')
            break
    qh.query_backend()
    osrs.move.click(qh.get_widgets(bank_dump_widget_id))
    while True:
        qh.query_backend()
        if len(qh.get_inventory()) == 0:
            osrs.dev.logger.info('inventory dumped in bank.')
            osrs.clock.sleep_one_tick()
            break
    while True:
        qh.query_backend()
        if qh.get_bank() and len(qh.get_bank()) > 0:
            osrs.dev.logger.info('withdrawing items for another sully trip.')
            osrs.move.click(qh.get_bank()[0])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[2])
            break
    osrs.keeb.press_key('esc')


def herbi_handler():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_script_stats({'status': 'Tracking Herbiboar.'})
    while True:
        osrs.game.break_manager_v4(script_config)
        qh.query_backend()
        # need at least three inv slots to pick herbi
        if (qh.get_inventory() and len(qh.get_inventory()) > 23) or not osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), stam_pot_ids):
            return
        start_herbi()
        catch_herbi_v2()


script_config = {
    'intensity': 'high',
    'login': lambda: osrs.clock.random_sleep(2, 3),
    'logout': lambda: osrs.clock.random_sleep(2, 3),
}


def main():
    while True:
        osrs.game.tele_home()
        click_mounted_digsite_pendant()
        mushtree_to_swamp()
        herbi_handler()
        bank_in_varrock()


main()
