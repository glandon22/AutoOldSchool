import datetime
import osrs

logger = osrs.dev.instantiate_logger()

wc_animations = [
    879, 877, 875, 873, 871, 869, 867, 8303, 2846, 24, 2117, 7264, 8324, 8778
]

bank_container_widget_id = '12,1'
bank_dump_widget_id = '12,42'

fancy_restore_pool_id = '29241'
varrock_tele_widget_id = '218,23'
sara_brew_ids = [6685, 6687, 6689, 6691]
mort_myre_fungus_id = 2970
super_antipoison_id = '185'
health_orb_id = '160,10'
mounted_digsite_pendant_id = '33417'
mush_tree_id = '30920'
mush_tree_tile = '3765,3880,1'
sticky_swamp_button_id = '608,11'

sully_1_id = '31420'
sully_1_tile_id = '3683,3758,0'

sully_2_id = '31421'
sully_2_tile_id = '3678,3733,0'

sully_3_id = '31422'
sully_3_tile_id = '3683,3775,0'

sully_4_id = '31423'
sully_4_tile_id = '3664,3781,0'

sully_5_id = '31424'
sully_5_tile_id = '3664,3802,0'

sully_6_id = '31425'
sully_6_tile_id = '3678,3806,0'

floor_vines_1_id = '30644'
floor_vines_1_tile_id = '3675,3771,0'

thick_vine_1_id = '30646'
thick_vine_1_tile_id = '3679,3743,0'

thick_vine_2_id = '30648'
thick_vine_2_tile_id = '3670,3747,0'

thick_vine_3_tile_id = '3671,3760,0'
thick_vine_4_tile_id = '3672,3764,0'
thick_vine_5_tile_id = '3666,3789,0'
thick_vine_6_tile_id = '3670,3792,0'
thick_vine_7_tile_id = '3672,3802,0'

mushroom_to_drop_id = 6004

mushtree_ids = {mush_tree_id, sully_1_id, sully_2_id, sully_3_id, sully_4_id, sully_5_id, sully_6_id}
mushtree_tile_ids = {mush_tree_tile, sully_1_tile_id, sully_2_tile_id, sully_3_tile_id, sully_4_tile_id,
                     sully_5_tile_id, sully_6_tile_id}

vine_ids = {thick_vine_1_id, thick_vine_2_id, floor_vines_1_id}
vine_tile_ids = {thick_vine_1_tile_id, thick_vine_2_tile_id, thick_vine_3_tile_id, thick_vine_4_tile_id,
                 floor_vines_1_tile_id, thick_vine_5_tile_id, thick_vine_6_tile_id, thick_vine_7_tile_id}

var_west_bank_id = '10583'
var_west_bank_tile_ids = {'3186,3438,0', '3186,3440,0', '3186,3442,0'}

sully_tree_map = {
    '1': sully_1_id,
    '2': sully_2_id,
    '3': sully_3_id,
    '4': sully_4_id,
    '5': sully_5_id,
    '6': sully_6_id
}


def mushtree_to_swamp(qh: osrs.queryHelper.QueryHelper):
    logger.info('searching for mushtree to travel to sticky swamp.')
    last_mushtree_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_swamp_press = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets() and (datetime.datetime.now() - last_swamp_press).total_seconds() > 5:
            logger.info('mushtree teleport menu open, selecting sticky swamp.')
            osrs.keeb.write('3')
            last_swamp_press = datetime.datetime.now()
        elif qh.get_player_world_location() and qh.get_player_world_location()['y'] < 3800:
            logger.info('in sticky swamp.')
            return
        elif qh.get_game_objects(mush_tree_id) and (datetime.datetime.now() - last_mushtree_click).total_seconds() > 8:
            osrs.move.click(qh.get_game_objects(mush_tree_id)[0])
            last_mushtree_click = datetime.datetime.now()
            logger.info('Clicked mushtree.')


def chop_sully(qh: osrs.queryHelper.QueryHelper, position):
    last_sully_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    sully_to_chop = sully_tree_map[position]
    while True:
        qh.query_backend()
        if qh.get_inventory() and len(qh.get_inventory()) == 28:
            logger.info('Full inventory chopping.')
            osrs.inv.power_drop(qh.get_inventory(), [], [mushroom_to_drop_id, mort_myre_fungus_id])
        elif qh.get_widgets(health_orb_id) and qh.get_widgets(health_orb_id)['spriteID'] == 1061:
            anti = qh.get_inventory(super_antipoison_id)
            if not anti:
                logger.error('No super anti poision in bag.')
                osrs.game.logout()
                exit(1)
            osrs.move.click(anti)
        elif qh.get_skills('hitpoints')['boostedLevel'] < 30:
            s_brew = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), sara_brew_ids)
            if not s_brew:
                logger.error('Low on health, out of sara brews.')
                osrs.game.tele_home()
                osrs.game.logout()
                exit(1)
            osrs.move.click(s_brew)
        elif qh.get_player_animation() and qh.get_player_animation() in wc_animations:
            logger.info('Currently chopping.')
        elif qh.get_game_objects(sully_to_chop) and (datetime.datetime.now() - last_sully_click).total_seconds() > 7:
            found_option = osrs.move.right_click_menu_select(
                qh.get_game_objects(sully_to_chop)[0], None, '56799', 'Sulliuscep', 'Cut'
            )
            if not found_option:
                logger.info('sully tree has been cut down.')
                return
            last_sully_click = datetime.datetime.now()
            logger.info(f'Clicked sully tree: {position}.')


def run_to_sully2(qh: osrs.queryHelper.QueryHelper):
    logger.info('running to second sully tree.')
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') > 3752:
            osrs.move.spam_click('3681,3747,0', 0.9)
        elif qh.get_game_objects(thick_vine_1_id):
            osrs.move.fast_click(qh.get_game_objects(thick_vine_1_id)[0])
        elif qh.get_player_world_location('y') < 3747 and qh.get_player_world_location('x') > 3678:
            osrs.move.spam_click('3673,3743,0', 0.9)
        elif qh.get_player_world_location('x') < 3677 and qh.get_player_world_location('y') > 3736:
            osrs.move.spam_click('3673,3735,0', 0.9)
        elif qh.get_player_world_location('x') == 3673 and qh.get_player_world_location('y') == 3735:
            return


def run_to_sully3(qh: osrs.queryHelper.QueryHelper):
    logger.info('running to third sully tree.')
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') == 3684 and qh.get_player_world_location('y') == 3768:
            return
        elif qh.get_game_objects(thick_vine_2_id) \
                and osrs.util.find_closest_target(qh.get_game_objects(thick_vine_2_id)) \
                and osrs.util.find_closest_target(qh.get_game_objects(thick_vine_2_id))['y_coord'] < 3780:
            closest_vine = osrs.util.find_closest_target(qh.get_game_objects(thick_vine_2_id))
            if closest_vine:
                osrs.move.fast_click(closest_vine)
        elif qh.get_player_world_location('y') < 3748:
            osrs.move.spam_click('3670,3758,0', 0.9)
        elif qh.get_player_world_location('y') > 3758:
            osrs.move.spam_click('3684,3768,0', 0.9)


def run_to_sully4(qh: osrs.queryHelper.QueryHelper):
    logger.info('running to fourth sully tree.')
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') == 3665 and qh.get_player_world_location('y') == 3780:
            return
        elif qh.get_game_objects(floor_vines_1_id):
            osrs.move.fast_click(qh.get_game_objects(floor_vines_1_id)[0])
        else:
            osrs.move.spam_click('3665,3780,0', 0.9)


def run_to_sully5(qh: osrs.queryHelper.QueryHelper):
    logger.info('running to fifth sully tree.')
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') == 3667 and qh.get_player_world_location('y') == 3804:
            return
        elif qh.get_game_objects(thick_vine_2_id):
            closest_vine = osrs.util.find_closest_target(qh.get_game_objects(thick_vine_2_id))
            if closest_vine:
                osrs.move.fast_click(closest_vine)
        elif qh.get_game_objects(thick_vine_1_id):
            osrs.move.fast_click(qh.get_game_objects(thick_vine_1_id)[0])
        else:
            osrs.move.spam_click('3667,3804,0', 0.9)


def click_mounted_digsite_pendant(qh: osrs.queryHelper.QueryHelper):
    logger.info('Looking for digsite pendant')
    tile_map = None
    last_pendant_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_pool_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') > 4000 and not tile_map:
            logger.info('in house, generating tile map.')
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
                (datetime.datetime.now() - last_pool_click).total_seconds() > 7 \
                and qh.get_skills('hitpoints')['boostedLevel'] != qh.get_skills('hitpoints')['level']:
            logger.info('Click on ornate rejuvenation pool.')
            osrs.move.click(
                qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value)[fancy_restore_pool_id][0]
            )
            last_pool_click = datetime.datetime.now()
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.DECORATIVE.value, mounted_digsite_pendant_id) and \
                (datetime.datetime.now() - last_pendant_click).total_seconds() > 7 \
                and qh.get_skills('hitpoints')['boostedLevel'] == qh.get_skills('hitpoints')['level']:
            logger.info('clicking on digsite pendant')
            osrs.move.click(
                qh.get_objects(osrs.queryHelper.ObjectTypes.DECORATIVE.value)[mounted_digsite_pendant_id][0]
            )
            last_pendant_click = datetime.datetime.now()
        elif 3840 < qh.get_player_world_location('y') < 3900:
            logger.info('successfully teleported to fossil island.')
            return


def bank_in_varrock(qh: osrs.queryHelper.QueryHelper):
    logger.info('beginning banking sequence.')
    last_tele_attempt = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 3420 < qh.get_player_world_location('y') < 3440 and 3203 < qh.get_player_world_location('x') < 3222:
            logger.info('arrived in varrock.')
            break
        elif (datetime.datetime.now() - last_tele_attempt).total_seconds() > 7:
            osrs.game.cast_spell(varrock_tele_widget_id)
            last_tele_attempt = datetime.datetime.now()
            logger.info('teleported to varrock')
    last_bank_booth_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, var_west_bank_id) and (datetime.datetime.now() - last_bank_booth_click).total_seconds() > 15:
            closest = osrs.util.find_closest_target(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, var_west_bank_id))
            if closest:
                osrs.move.click(closest)
                last_bank_booth_click = datetime.datetime.now()
                logger.info(f'clicked bank booth: {closest}')
        elif qh.get_widgets(bank_dump_widget_id):
            logger.info('bank interface opened.')
            break
    qh.query_backend()
    osrs.move.click(qh.get_widgets(bank_dump_widget_id))
    while True:
        qh.query_backend()
        if len(qh.get_inventory()) == 0:
            logger.info('inventory dumped in bank.')
            osrs.clock.sleep_one_tick()
            break
    while True:
        qh.query_backend()
        if qh.get_bank() and len(qh.get_bank()) > 0:
            logger.info('withdrawing items for another sully trip.')
            osrs.move.click(qh.get_bank()[0])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[1])
            osrs.move.click(qh.get_bank()[2])
            osrs.move.click(qh.get_bank()[3])
            break
    osrs.keeb.press_key('esc')


def finish_trip(qh: osrs.queryHelper.QueryHelper):
    logger.info('Trip complete, deciding whether or not to bank.')
    qh.query_backend()
    osrs.inv.power_drop(qh.get_inventory(), [], [mushroom_to_drop_id, mort_myre_fungus_id])
    osrs.clock.sleep_one_tick()
    qh.query_backend()
    if len(qh.get_inventory()) > 10 or not qh.get_inventory(super_antipoison_id):
        logger.info(f'need to bank. inv length: {len(qh.get_inventory())}. super anti status: {bool(qh.get_inventory(super_antipoison_id))}')
        bank_in_varrock(qh)


script_config = {
    'intensity': 'high',
    'login': lambda: osrs.clock.random_sleep(2, 3),
    'logout': lambda: osrs.clock.random_sleep(2, 3),
}


def main():
    qh = osrs.queryHelper.QueryHelper()
    while True:
        qh.clear_query()
        qh.set_game_objects(
            {mush_tree_tile}.union(mushtree_tile_ids).union(vine_tile_ids).union(var_west_bank_tile_ids),
            {mush_tree_id}.union(mushtree_ids).union(vine_ids).union({var_west_bank_id})
        )
        qh.set_widgets({sticky_swamp_button_id, health_orb_id, varrock_tele_widget_id, bank_dump_widget_id})
        qh.set_player_world_location()
        qh.set_player_animation()
        qh.set_inventory()
        qh.set_skills({'hitpoints'})
        qh.set_bank()

        logger.info('Teleing home.')
        osrs.game.tele_home()
        click_mounted_digsite_pendant(qh)
        mushtree_to_swamp(qh)
        osrs.game.break_manager_v4(script_config)
        chop_sully(qh, '1')
        run_to_sully2(qh)
        chop_sully(qh, '2')
        run_to_sully3(qh)
        chop_sully(qh, '3')
        run_to_sully4(qh)
        chop_sully(qh, '4')
        run_to_sully5(qh)
        chop_sully(qh, '5')
        osrs.clock.sleep_one_tick()
        chop_sully(qh, '6')
        finish_trip(qh)


main()
