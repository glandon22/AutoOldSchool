import datetime
import random

import osrs

wc_animations = [
    879, 877, 875, 873, 871, 869, 867, 8303, 2846, 24, 2117, 7264, 8324, 8778, 10071
]

equipment = [
    {'id': osrs.item_ids.EXPLORERS_RING_2, 'consume': 'Wear'},
    {'id': osrs.item_ids.HITPOINTS_CAPET, 'consume': 'Wear'},
    {'id': osrs.item_ids.REGEN_BRACELET, 'consume': 'Wear'},
    {'id': osrs.item_ids.HOLY_BLESSING, 'consume': 'Equip'},
    {'id': osrs.item_ids.HELM_OF_NEITIZNOT, 'consume': 'Wear'},
    {'id': osrs.item_ids.BOOTS_OF_BRIMSTONE, 'consume': 'Wear'},
    {'id': osrs.item_ids.DRAGON_FELLING_AXE, 'consume': 'Wield'},
    {'id': osrs.item_ids.AMULET_OF_FURY, 'consume': 'Wear'},
    {'id': osrs.item_ids.RUNE_PLATEBODY, 'consume': 'Wear'},
    {'id': osrs.item_ids.RUNE_PLATELEGS, 'consume': 'Wear'},
]

supplies = [
    osrs.item_ids.SARADOMIN_BREW4,
    osrs.item_ids.SARADOMIN_BREW4,
    osrs.item_ids.SUPERANTIPOISON2,
    osrs.item_ids.RAKE,
    osrs.item_ids.RUNE_POUCH,
]

bank_container_widget_id = '12,1'
bank_dump_widget_id = '12,42'

fancy_restore_pool_id = '29241'
varrock_tele_widget_id = '218,23'
sara_brew_ids = [6685, 6687, 6689, 6691]
mort_myre_fungus_id = 2970
super_antipoison_id = [
    osrs.item_ids.SUPERANTIPOISON1,
    osrs.item_ids.SUPERANTIPOISON2,
]
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

mushroom_to_drop_id = 6004

mushtree_ids = {mush_tree_id, sully_1_id, sully_2_id, sully_3_id, sully_4_id, sully_5_id, sully_6_id}
mushtree_tile_ids = {mush_tree_tile, sully_1_tile_id, sully_2_tile_id, sully_3_tile_id, sully_4_tile_id,
                     sully_5_tile_id, sully_6_tile_id}

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
    osrs.dev.logger.info('searching for mushtree to travel to sticky swamp.')
    last_mushtree_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_swamp_press = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets() and (datetime.datetime.now() - last_swamp_press).total_seconds() > 5:
            osrs.dev.logger.info('mushtree teleport menu open, selecting sticky swamp.')
            osrs.keeb.write('3')
            last_swamp_press = datetime.datetime.now()
        elif qh.get_player_world_location() and qh.get_player_world_location()['y'] < 3800:
            osrs.dev.logger.info('in sticky swamp.')
            return
        elif qh.get_game_objects(mush_tree_id) and (datetime.datetime.now() - last_mushtree_click).total_seconds() > 8:
            osrs.move.click(qh.get_game_objects(mush_tree_id)[0])
            last_mushtree_click = datetime.datetime.now()
            osrs.dev.logger.info('Clicked mushtree.')


def chop_sully(position):
    sully_to_chop = sully_tree_map[position]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {int(sully_to_chop)})
    qh.set_inventory()
    qh.set_skills({'hitpoints'})
    qh.set_widgets({health_orb_id})
    qh.set_canvas()
    qh.set_player_animation()
    last_chopping = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        # tree cut down
        if qh.get_objects_v2('game', int(sully_to_chop)) and qh.get_objects_v2('game', int(sully_to_chop))[0]['height'] < 65:
            return
        elif qh.get_inventory() and len(qh.get_inventory()) == 28:
            osrs.dev.logger.info('Full inventory.')
            osrs.inv.power_drop_v2(qh, [mushroom_to_drop_id, mort_myre_fungus_id])
        elif qh.get_widgets(health_orb_id) and qh.get_widgets(health_orb_id)['spriteID'] == 1061:
            anti = qh.get_inventory(super_antipoison_id)
            if not anti:
                osrs.dev.logger.error('No super anti poision in bag.')
                return
            osrs.move.click(anti)
        elif qh.get_skills('hitpoints')['boostedLevel'] < 30:
            s_brew = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), sara_brew_ids)
            if not s_brew:
                osrs.dev.logger.error('Low on health, out of sara brews.')
                return
            osrs.move.fast_click_v2(s_brew)
        elif qh.get_player_animation() and qh.get_player_animation() in wc_animations:
            osrs.dev.logger.info('Currently chopping.')
            last_chopping = datetime.datetime.now()
        elif (qh.get_objects_v2('game', int(sully_to_chop))
              and (datetime.datetime.now() - last_chopping).total_seconds() > 1.5):
            osrs.move.fast_click_v2(qh.get_objects_v2('game', int(sully_to_chop))[0])
            osrs.dev.logger.info(f'Clicked sully tree: {position}.')


def in_ge():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 3147 <= qh.get_player_world_location('x') <= 3182 and 3477 <= qh.get_player_world_location('y') <= 3499:
        return True


def pre():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({osrs.widget_ids.spells_inv_widget_id})
    qh.query_backend()
    if qh.get_widgets(osrs.widget_ids.spells_inv_widget_id) or qh.get_widgets(osrs.widget_ids.spells_inv_widget_id)['spriteID'] != 1027:
        osrs.keeb.press_key('f6')


def finish_trip(qh: osrs.queryHelper.QueryHelper):
    osrs.dev.logger.info('Trip complete, deciding whether or not to bank.')
    qh.query_backend()
    osrs.inv.power_drop_v2(qh, [mushroom_to_drop_id, mort_myre_fungus_id])
    osrs.clock.sleep_one_tick()
    qh.query_backend()
    if len(qh.get_inventory()) > 10 or not qh.get_inventory(super_antipoison_id) or not qh.get_inventory([
        osrs.item_ids.SARADOMIN_BREW2,
        osrs.item_ids.SARADOMIN_BREW3,
        osrs.item_ids.SARADOMIN_BREW4,
    ]):
        osrs.dev.logger.info(f'need to bank. inv length: {len(qh.get_inventory())}. super anti status: {bool(qh.get_inventory(super_antipoison_id))}')
        osrs.move.interact_with_widget_v3(
            osrs.widget_ids.varrock_tele_widget_id,
            right_click_option='Grand Exchange',
            timeout=7,
            custom_exit_function=in_ge,
            pre_interact=pre
        )
        osrs.bank.banking_handler({
            'dump_inv': True,
            'search': [{'query': 'sully', 'items': supplies}]
        })


script_config = {
    'intensity': 'high',
    'login': lambda: osrs.clock.random_sleep(2, 3),
    'logout': lambda: osrs.clock.random_sleep(2, 3),
}


def start():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    # also start the script in the GE
    if not (3147 <= qh.get_player_world_location('x') <= 3182 and 3477 <= qh.get_player_world_location('y') <= 3499):
        osrs.game.slow_lumb_tele()
        osrs.move.go_to_loc(3208, 3211)
        osrs.move.interact_with_object_v3(
            14880, obj_type='ground', coord_type='y', coord_value=9000,
            greater_than=True, right_click_option='Climb-down', timeout=8
        )
    osrs.bank.banking_handler({
        'dump_equipment': True,
        'dump_inv': True,
        'search': [{'query': 'sully', 'items': equipment + supplies}]
    })


def on_fossil_island():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_widgets({'187,3'})
    qh.query_backend()
    if 3634 <= qh.get_player_world_location('x') <= 3837 and 3701 <= qh.get_player_world_location('y') <= 3901:
        return True
    elif qh.get_widgets('187,3'):
        osrs.keeb.write('2')


def main(endless_loop=True):
    iter_count = 9999 if endless_loop else random.randint(3, 5)
    qh = osrs.queryHelper.QueryHelper()
    start()
    while True:
        qh.clear_query()
        qh.set_game_objects(
            {mush_tree_tile}.union(mushtree_tile_ids).union(var_west_bank_tile_ids),
            {mush_tree_id}.union(mushtree_ids).union({var_west_bank_id})
        )
        qh.set_widgets({sticky_swamp_button_id, health_orb_id, varrock_tele_widget_id, bank_dump_widget_id})
        qh.set_player_world_location()
        qh.set_player_animation()
        qh.set_inventory()
        qh.set_skills({'hitpoints'})
        qh.set_bank()
        qh.set_canvas()
        osrs.dev.logger.info('Teleing home.')
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.move.interact_with_object_v3(
            33417,
            obj_type='decorative', custom_exit_function=on_fossil_island, right_click_option='Teleport menu',
            timeout=7
        )
        break_info = osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False
        })
        if iter_count == 0:
            return
        elif 'took_break' in break_info and break_info['took_break']:
            iter_count -= 1
        mushtree_to_swamp(qh)
        osrs.player.toggle_run('on')
        chop_sully('1')
        osrs.move.go_to_loc(3682, 3743)
        osrs.move.interact_with_object_v3(
            30646, obj_tile={'x': 3678, 'y': 3743, 'z': 0}, intermediate_tile='3673,3743,0',
            coord_type='x', coord_value=3674, greater_than=False
        )
        osrs.move.go_to_loc(3679, 3732)
        chop_sully('2')
        osrs.move.go_to_loc(3670, 3744)
        osrs.move.interact_with_object_v3(
            30648, obj_tile={'x': 3669, 'y': 3747, 'z': 0}, intermediate_tile='3668,3754,0',
            coord_type='y', coord_value=3751, greater_than=True
        )
        osrs.move.interact_with_object_v3(
            30648, obj_tile={'x': 3672, 'y': 3760, 'z': 0}, intermediate_tile='3671,3763,0',
            coord_type='y', coord_value=3761, greater_than=True
        )
        osrs.move.interact_with_object_v3(
            30648, obj_tile={'x': 3672, 'y': 3764, 'z': 0}, intermediate_tile='3678,3766,0',
            coord_type='x', coord_value=3676, greater_than=True
        )
        osrs.move.go_to_loc(3684, 3774)
        chop_sully('3')
        osrs.move.go_to_loc(3675, 3769)
        osrs.move.interact_with_object_v3(
            30644, obj_tile={'x': 3674, 'y': 3771, 'z': 0}, intermediate_tile='3674,3774,0',
            coord_type='y', coord_value=3773, greater_than=True
        )
        osrs.move.go_to_loc(3665, 3781)
        chop_sully('4')
        osrs.move.interact_with_object_v3(
            30648, obj_tile={'x': 3667, 'y': 3789, 'z': 0}, intermediate_tile='3669,3792,0',
            coord_type='y', coord_value=3792, greater_than=True
        )
        osrs.move.interact_with_object_v3(
            30648, obj_tile={'x': 3671, 'y': 3792, 'z': 0}, intermediate_tile='3673,3796,0',
            coord_type='y', coord_value=3796, greater_than=True
        )
        osrs.move.interact_with_object_v3(
            30646, obj_tile={'x': 3672, 'y': 3802, 'z': 0}, intermediate_tile='3671,3805,0',
            coord_type='y', coord_value=3805, greater_than=True
        )
        osrs.move.go_to_loc(3665, 3803)
        osrs.clock.sleep_one_tick()
        chop_sully('5')
        osrs.move.go_to_loc(3680, 3806)
        chop_sully('6')
        finish_trip(qh)
