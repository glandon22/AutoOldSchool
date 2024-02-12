import osrs
import datetime

ancient_staff = '4675'
desert_am_4_id = '13136'
elidnis_stat_id = '10389'
elidnis_stat_tile = '3427,2930,0'
ring_shadows_id = '28327'

# Start fight by clicking this
odd_figure_id = '12203'

# The Whisperer Boss
whisperer_id = '12204'
whisperer_melee_id = '12205'

# Tentacle Attack
tentacle_id = '12208'

# Freezing Melee Special
freezing_special_id = 2467

prayer_tab_widget = '161,63'
mage_prayer_widget = '541,21'
range_prayer_widget = '541,22'

ice_barrage_id = '218,79'

lost_soul_immune_id = '12211'
lost_soul_attackable_id = '12212'

ready_blackstone_id = '28356'
bad_orb = '47575'
good_orb = '47573'

floating_pillar_normal_id = '12210'
floating_pillar_shadow_id = '12209'

sage_axe = '28773'


# DROPS #
virtus_mask_id = '26241'
virtus_top_id = '26243'
virtus_bottom_id = '26245'

shadow_quartz_id = '28272'
ax_piece_1 = '28325'
ax_piece_2 = '28323'
ax_piece_3 = '28319'
ax_piece_4 = '28321'
# awakener_orb = '28334'

drag_jave_id = '19582'
r_bolts_unf_id = '9381'
pure_ess_id = '7937'

#2444 range
# 2445 mage


def pray_flick(projectile, phase, qh: osrs.queryHelper.QueryHelper, anchor_tile):
    osrs.keeb.press_key('f5')
    osrs.clock.random_sleep(0.1, 0.11)
    qh.query_backend()
    if projectile['id'] == 2444 and not (qh.get_active_prayers() and 4117 in qh.get_active_prayers()):
        osrs.move.instant_click(qh.get_widgets(range_prayer_widget)['x'], qh.get_widgets(range_prayer_widget)['y'])
    elif projectile['id'] == 2445 and not (qh.get_active_prayers() and 4116 in qh.get_active_prayers()):
        osrs.move.instant_click(qh.get_widgets(mage_prayer_widget)['x'], qh.get_widgets(mage_prayer_widget)['y'])
    if phase == 1:
        osrs.clock.random_sleep(1.5, 1.51)
        return avoid_tentacle(qh, anchor_tile)
    elif phase == 2 or phase == 3:
        osrs.clock.random_sleep(1.67, 1.68)
        if projectile['id'] == 2444:
            osrs.move.instant_click(qh.get_widgets(mage_prayer_widget)['x'], qh.get_widgets(mage_prayer_widget)['y'])
        else:
            osrs.move.instant_click(qh.get_widgets(range_prayer_widget)['x'], qh.get_widgets(range_prayer_widget)['y'])
        osrs.clock.random_sleep(0.2, 0.21)
        return avoid_tentacle(qh, anchor_tile)
    elif phase == 4:
        '''osrs.clock.random_sleep(0.84, 0.85)
        if projectile['id'] == 2444:
            osrs.move.instant_click(qh.get_widgets(mage_prayer_widget)['x'], qh.get_widgets(mage_prayer_widget)['y'])
        else:
            osrs.move.instant_click(qh.get_widgets(range_prayer_widget)['x'], qh.get_widgets(range_prayer_widget)['y'])
        osrs.clock.random_sleep(0.56, 0.57)
        if projectile['id'] == 2444:
            osrs.move.instant_click(qh.get_widgets(range_prayer_widget)['x'], qh.get_widgets(range_prayer_widget)['y'])
        else:
            osrs.move.instant_click(qh.get_widgets(mage_prayer_widget)['x'], qh.get_widgets(mage_prayer_widget)['y'])'''
        osrs.clock.random_sleep(1.4, 1.41)
        return avoid_tentacle(qh, anchor_tile)


def pray_range(qh: osrs.queryHelper.QueryHelper):
    while True:
        qh.query_backend()
        if qh.get_active_prayers() and 4117 in qh.get_active_prayers():
            return
        prayer_tab = qh.get_widgets(prayer_tab_widget)
        if prayer_tab:
            if prayer_tab['spriteID'] != 1030:
                osrs.keeb.press_key('f5')
            while True:
                qh.query_backend()
                if qh.get_widgets(range_prayer_widget) and qh.get_widgets(range_prayer_widget)['x'] > 250:
                    osrs.move.instant_click(qh.get_widgets(range_prayer_widget)['x'], qh.get_widgets(range_prayer_widget)['y'])
                    osrs.move.fast_move({'x': 900, 'y': 500})
                    return


def pray_mage(qh: osrs.queryHelper.QueryHelper):
    while True:
        qh.query_backend()
        if qh.get_active_prayers() and 4116 in qh.get_active_prayers():
            return
        prayer_tab = qh.get_widgets(prayer_tab_widget)
        if prayer_tab:
            if prayer_tab['spriteID'] != 1030:
                osrs.keeb.press_key('f5')
            while True:
                qh.query_backend()
                if qh.get_widgets(mage_prayer_widget) and qh.get_widgets(mage_prayer_widget)['x'] > 250:
                    osrs.move.instant_click(qh.get_widgets(mage_prayer_widget)['x'], qh.get_widgets(mage_prayer_widget)['y'])
                    osrs.move.fast_move({'x': 900, 'y': 500})
                    return


def find_next_npc(npcs, target):
    for npc in npcs:
        if int(npc['id']) == int(target):
            return npc


def wait_for_pillars(qh):
    while True:
        qh.query_backend()
        npcs = qh.get_npcs()
        for npc in npcs:
            if str(npc['compositionID']) == floating_pillar_shadow_id:
                osrs.clock.sleep_one_tick()
                return


def wait_for_pillar_projectile(qh: osrs.queryHelper.QueryHelper):
    while True:
        qh.query_backend()
        if qh.get_projectiles_v2():
            for projectile in qh.get_projectiles_v2():
                if projectile['id'] == 2471:
                    return


def calculate_second_pillar(first_pillar, third_pillar, npcs):
    second_pillar = False
    # there is at least one pillar layout where there is no second pillar between the first and third,
    # if that is that case, just select the pillar that is closest to me
    second_pillar_between_first_and_third = False
    for npc in npcs:
        if str(npc['compositionID']) == floating_pillar_shadow_id and npc['health'] == 27:
            print('++++++++++++++++')
            print(second_pillar)
            print('++++++++++++++++')
            distance_between_this_pillar_and_third_pillar = osrs.dev.point_dist(
                    npc['x_coord'],
                    npc['y_coord'],
                    third_pillar['x_coord'],
                    third_pillar['y_coord']
                )
            # If we don't have a second pillar saved yet, save the first one we see.
            if not second_pillar:
                if first_pillar['x_coord'] < npc['x_coord'] < third_pillar['x_coord'] \
                        or third_pillar['x_coord'] < npc['x_coord'] < first_pillar['x_coord']:
                    second_pillar_between_first_and_third = True
                npc['thid_pillar_dist'] = distance_between_this_pillar_and_third_pillar
                second_pillar = npc
            elif npc['dist'] <= second_pillar['dist']:
                if first_pillar['x_coord'] < npc['x_coord'] < third_pillar['x_coord'] \
                        or third_pillar['x_coord'] < npc['x_coord'] < first_pillar['x_coord']:
                    second_pillar_between_first_and_third = True
                    npc['thid_pillar_dist'] = distance_between_this_pillar_and_third_pillar
                    second_pillar = npc
            elif not second_pillar_between_first_and_third and first_pillar['x_coord'] < npc['x_coord'] < third_pillar['x_coord'] \
                        or third_pillar['x_coord'] < npc['x_coord'] < first_pillar['x_coord']:
                second_pillar_between_first_and_third = True
                npc['thid_pillar_dist'] = distance_between_this_pillar_and_third_pillar
                second_pillar = npc
            # If we never saw a second pillar between our first and third stages, just select the one
            # that is closest to me
    if not second_pillar_between_first_and_third:
        print('did not see a second pillar in between first and third')
        print(first_pillar, third_pillar, npcs)
        second_pillar = False
        print('++++++++++++++++')
        print(second_pillar)
        print('++++++++++++++++')
        for npc in npcs:
            if str(npc['compositionID']) == floating_pillar_shadow_id and npc['health'] == 27:
                distance_between_this_pillar_and_third_pillar = osrs.dev.point_dist(
                    npc['x_coord'],
                    npc['y_coord'],
                    third_pillar['x_coord'],
                    third_pillar['y_coord']
                )
                # If we don't have a second pillar saved yet, save the first one we see.
                if not second_pillar:
                    npc['thid_pillar_dist'] = distance_between_this_pillar_and_third_pillar
                    second_pillar = npc
                elif npc['dist'] <= second_pillar['dist']:
                    npc['thid_pillar_dist'] = distance_between_this_pillar_and_third_pillar
                    second_pillar = npc
    print('final second pillar: ', second_pillar)
    return second_pillar


def return_to_cathedral(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    print(qh.get_player_world_location())
    osrs.move.right_click_v3(qh.get_inventory(ring_shadows_id), 'Teleport')
    while True:
        qh.query_backend()
        if qh.get_chat_options():
            osrs.keeb.write('4')
            break
    while True:
        qh.query_backend()
        if qh.get_player_world_location() and qh.get_player_world_location()['x'] > 5500:
            # let the scene load in
            osrs.clock.sleep_one_tick()
            break
    while True:
        qh1 = osrs.queryHelper.QueryHelper()
        qh1.set_chat_options()
        tile_map = osrs.util.generate_game_tiles_in_coords(
            qh.get_player_world_location()['x'] - 15,
            qh.get_player_world_location()['x'] + 15,
            qh.get_player_world_location()['y'] - 15,
            qh.get_player_world_location()['y'] + 15,
            0
        )
        qh1.set_game_objects(
            set(tile_map),
            {'49479'}
        )
        qh1.query_backend()
        if qh1.get_game_objects('49479'):
            print(qh1.get_game_objects('49479'))
            osrs.move.click(qh1.get_game_objects('49479')[0])
            break
    while True:
        qh.query_backend()
        if qh.get_chat_options():
            osrs.keeb.write('2')
            osrs.clock.random_sleep(3, 3.1)
            break
    osrs.move.click({'x': 960, 'y': 75})
    while True:
        qh.query_backend()
        if qh.get_npcs():
            for npc in qh.get_npcs():
                if str(npc['id']) == odd_figure_id:
                    return


def restore_at_nardah(qh: osrs.queryHelper.QueryHelper):
    osrs.player.toggle_prayer('on')
    osrs.clock.sleep_one_tick()
    osrs.player.toggle_prayer('off')
    osrs.keeb.press_key('esc')
    curr_time = datetime.datetime.now()
    if curr_time.hour == 2:
        exit('its 2am')
    while True:
        qh.query_backend()
        if not qh.get_inventory(desert_am_4_id):
            exit('no ammy')
        osrs.move.right_click_v3(qh.get_inventory(desert_am_4_id), 'Nardah')
        while True:
            qh.query_backend()
            if 3420 < qh.get_player_world_location()['x'] < 3442 and 2918 < qh.get_player_world_location()['y'] < 2941:
                osrs.game.break_manager_v4(script_config)
                break
        while True:
            qh.query_backend()
            if qh.get_game_objects(elidnis_stat_id):
                osrs.move.click(osrs.util.find_closest_target(qh.get_game_objects(elidnis_stat_id)))
                osrs.clock.random_sleep(2, 2.5)
                qh.query_backend()
                if qh.get_skills('prayer')['boostedLevel'] > 95:
                    break
        osrs.keeb.press_key('esc')
        qh.query_backend()
        if qh.get_inventory(ancient_staff):
            osrs.move.click(qh.get_inventory(ancient_staff))
        return return_to_cathedral(qh)


def handle_screech_attack(qh: osrs.queryHelper.QueryHelper, anchor_tile):
    osrs.player.toggle_prayer('on')
    osrs.clock.random_sleep(0.2, 0.22)
    osrs.player.toggle_prayer('off')
    projectiles_seen = 0
    while True:
        qh.query_backend()
        if qh.get_inventory(ready_blackstone_id):
            osrs.keeb.press_key('esc')
            osrs.move.fast_click(qh.get_inventory(ready_blackstone_id))
            break
    # let the pillars load in correctly
    pillars_seen = False
    wait_for_pillars(qh)
    second_pillar = False
    third_pillar = False
    while True:
        qh.query_backend()
        npcs = qh.get_npcs()
        closest = False
        for npc in npcs:
            if str(npc['compositionID']) == floating_pillar_shadow_id and npc['health'] == 14:
                if not closest or npc['dist'] < closest['dist']:
                    closest = npc
            elif str(npc['compositionID']) == floating_pillar_shadow_id and npc['health'] == 40:
                third_pillar = npc
        osrs.move.spam_click('{},{},3'.format(closest['x_coord'], closest['y_coord'] + 2), 0.6)
        second_pillar = calculate_second_pillar(closest, third_pillar, qh.get_npcs())
        if closest:
            break
    wait_for_pillar_projectile(qh)
    osrs.move.spam_click('{},{},3'.format(second_pillar['x_coord'], second_pillar['y_coord'] + 2), 0.6)
    osrs.clock.sleep_one_tick()
    wait_for_pillar_projectile(qh)
    osrs.move.spam_click('{},{},3'.format(third_pillar['x_coord'], third_pillar['y_coord'] + 2), 0.6)
    osrs.clock.sleep_one_tick()
    wait_for_pillar_projectile(qh)
    osrs.move.spam_click('{},{},3'.format(anchor_tile['x'], anchor_tile['y']), 1.3)
    osrs.clock.random_sleep(1, 1.01)
    qh.query_backend()
    whisp = find_next_npc(qh.get_npcs(), whisperer_id)
    osrs.move.instant_click(whisp['x'], whisp['y'])


def handle_vita_souls(qh: osrs.queryHelper.QueryHelper, tile):
    vita_souls = []
    osrs.keeb.press_key('esc')
    osrs.move.spam_click('{},{},0'.format(qh.get_player_world_location()['x'], qh.get_player_world_location()['y'] + 2), 0.4)
    while True:
        qh.query_backend()
        if qh.get_inventory() and qh.get_inventory(ready_blackstone_id):
            print('clicking black stone in lost soul phase')
            osrs.move.fast_click(qh.get_inventory(ready_blackstone_id))
            break
    osrs.player.toggle_prayer('on')
    osrs.clock.random_sleep(0.1, 0.11)
    osrs.player.toggle_prayer('off')
    # wait for souls to appear
    while True:
        qh.query_backend()
        npcs = qh.get_npcs()
        for npc in npcs:
            if 'overheadText' in npc and npc['overheadText'] == 'Vita!':
                vita_souls.append(npc)
        if len(vita_souls) == 2:
            break
    vita_souls = sorted(vita_souls, key=lambda d: d['dist'])
    for vita_soul in vita_souls:
        osrs.move.instant_spam_click('{},{},3'.format(vita_soul['x_coord'], vita_soul['y_coord']), 1)
        osrs.clock.random_sleep(2, 2.1)
    osrs.move.spam_click('{},{},3'.format(tile['x'], tile['y'] + 8), 0.6)
    osrs.clock.random_sleep(2.9, 3)
    qh.query_backend()
    whispy = find_next_npc(qh.get_npcs(), whisperer_id)
    if whispy:
        osrs.move.instant_click(whispy['x'], whispy['y'])


def handle_enrage(curr_loc, prev_loc, qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    whispy = find_next_npc(qh.get_npcs(), whisperer_id)
    if whispy:
        osrs.move.instant_click(whispy['x'], whispy['y'])
        osrs.clock.random_sleep(0.2, 0.22)
    osrs.keeb.press_key('f5')
    osrs.clock.random_sleep(0.1, 0.11)
    qh.query_backend()
    if not (qh.get_active_prayers() and 4117 in qh.get_active_prayers()):
        osrs.move.instant_click(qh.get_widgets(range_prayer_widget)['x'], qh.get_widgets(range_prayer_widget)['y'])
    clicks = 0
    while True:
        qh.set_tiles({
            '{},{},{}'.format(prev_loc['x'] - 2, prev_loc['y'] + 1, 0),
            '{},{},{}'.format(prev_loc['x'] + 2, prev_loc['y'], 0)
        })
        qh.query_backend()
        if qh.get_tiles('{},{},{}'.format(prev_loc['x'] - 2, prev_loc['y'] + 1, 0)):
            osrs.move.fast_click(qh.get_tiles('{},{},{}'.format(prev_loc['x'] - 2, prev_loc['y'] + 1, 0)))
            osrs.clock.random_sleep(0.1, 0.11)
            clicks += 1
        else:
            break
        qh.query_backend()
        whispy = find_next_npc(qh.get_npcs(), whisperer_id)
        if whispy and clicks % 3 == 0:
            osrs.move.instant_click(whispy['x'], whispy['y'])
            osrs.clock.random_sleep(0.07, 0.08)
        qh.query_backend()
        if qh.get_tiles('{},{},{}'.format(prev_loc['x'] + 2, prev_loc['y'], 0)):
            osrs.move.fast_click(qh.get_tiles('{},{},{}'.format(prev_loc['x'] + 2, prev_loc['y'], 0)))
            osrs.clock.random_sleep(0.1, 0.11)
            clicks += 1
        else:
            break
    while True:
        print('in last phase')
        qh.set_tiles({
            '{},{},{}'.format(prev_loc['x'] - 2, prev_loc['y'] + 4, 3),
            '{},{},{}'.format(prev_loc['x'] + 2, prev_loc['y'] + 3, 3)
        })
        qh.set_surrounding_ground_items(10, qh.get_player_world_location())
        qh.query_backend()
        if qh.get_tiles('{},{},{}'.format(prev_loc['x'] - 2, prev_loc['y'] + 4, 3)):
            osrs.move.fast_click(qh.get_tiles('{},{},{}'.format(prev_loc['x'] - 2, prev_loc['y'] + 4, 3)))
            osrs.clock.random_sleep(0.1, 0.11)
        else:
            if qh.get_surrounding_ground_items():
                return 1
            print('couldnt find first lvl 3 tile but no loot')
        qh.query_backend()
        whispy = find_next_npc(qh.get_npcs(), whisperer_id)
        if whispy:
            osrs.move.instant_click(whispy['x'], whispy['y'])
            osrs.clock.random_sleep(0.2, 0.22)
        qh.query_backend()
        if qh.get_tiles('{},{},{}'.format(prev_loc['x'] + 2, prev_loc['y'] + 3, 3)):
            osrs.move.fast_click(qh.get_tiles('{},{},{}'.format(prev_loc['x'] + 2, prev_loc['y'] + 3, 3)))
            osrs.clock.random_sleep(0.1, 0.11)
        else:
            if qh.get_surrounding_ground_items():
                return 1
            print('couldnt find second lvl 3 tile but no loot')
            print(find_next_npc(qh.get_npcs(), whisperer_id))
            print('||||||||||||||||||||||||||||||||||||||||||||||')
        whispy = find_next_npc(qh.get_npcs(), whisperer_id)
        if whispy:
            osrs.move.instant_click(whispy['x'], whispy['y'])
            osrs.clock.random_sleep(0.2, 0.22)
        if qh.get_surrounding_ground_items():
            return 1




def avoid_tentacle(qh: osrs.queryHelper.QueryHelper, anchor_tile):
    loc = qh.get_player_world_location()
    whisp = find_next_npc(qh.get_npcs(), whisperer_id)
    centered_x = False
    destination_tile = False
    if loc['x'] >= anchor_tile['x']:
        centered_x = loc['x'] - 1
    else:
        centered_x = loc['x'] + 1

    if 6 <= osrs.dev.point_dist(centered_x, loc['y'] - 2, whisp['x_coord'], whisp['y_coord']) <= 9:
        destination_tile = '{},{},{}'.format(centered_x, loc['y'] - 2, loc['z'])
        osrs.move.instant_spam_click('{},{},{}'.format(centered_x, loc['y'] - 2, loc['z']), 0.6)
    else:
        destination_tile = '{},{},{}'.format(centered_x, loc['y'] + 2, loc['z'])
        osrs.move.instant_spam_click('{},{},{}'.format(centered_x, loc['y'] + 2, loc['z']), 0.6)
    last_tentacle_move = datetime.datetime.now()
    print('------------------------------------tentacle------------------------------------------')
    osrs.clock.random_sleep(0.2, 0.22)
    qh.query_backend()
    whispy = find_next_npc(qh.get_npcs(), whisperer_id)
    if whispy['health'] / whispy['scale'] < .19 and qh.get_inventory(sage_axe):
        print('++++++++++++++++++++++++++++++++++++')
        print(whispy)
        print('++++++++++++++++++++++++++++++++++++')
        osrs.keeb.press_key('esc')
        osrs.move.instant_click(qh.get_inventory(sage_axe)['x'], qh.get_inventory(sage_axe)['y'])
        return handle_enrage(destination_tile, loc, qh)
    osrs.move.instant_click(whispy['x'], whispy['y'])
    return last_tentacle_move


def collect_loot():
    while True:
        loot_items = osrs.server.get_surrounding_ground_items_any_ids(15)
        if loot_items:
            print('loot items: ', loot_items)
            break
    while True:
        loot_items = osrs.server.get_surrounding_ground_items_any_ids(15)
        found_loot = False
        if not loot_items:
            break
        for item in [
            virtus_mask_id,
            virtus_top_id,
            virtus_bottom_id,
            ax_piece_1,
            ax_piece_2,
            ax_piece_3,
            ax_piece_4,
            #awakener_orb,
            drag_jave_id,
            r_bolts_unf_id, pure_ess_id, shadow_quartz_id
        ]:
            if item in loot_items:
                found_loot = True
                osrs.move.spam_click('{},{},0'.format(loot_items[item][0]['x_coord'], loot_items[item][0]['y_coord']), 0.6)
                break
        if not found_loot:
            break


script_config = {
    'intensity': 'high',
    'login': lambda: osrs.clock.random_sleep(4, 5),
    'logout': lambda: osrs.clock.random_sleep(11, 14),
}


def main():
    phase = 1
    global ball_phase_complete
    global last_freeze_attack
    ball_phase_complete = False
    # Use this to track where I am in prayer cycle versus the projectiles
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([odd_figure_id, whisperer_id, tentacle_id, whisperer_melee_id, lost_soul_immune_id, lost_soul_attackable_id, floating_pillar_shadow_id, floating_pillar_normal_id])
    qh.set_projectiles_v2()
    qh.set_widgets({prayer_tab_widget, range_prayer_widget, mage_prayer_widget, ice_barrage_id})
    qh.set_active_prayers()
    qh.set_player_world_location()
    qh.set_game_cycle()
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_skills({'magic', 'prayer'})
    qh.clear_game_objects()
    qh.set_game_objects(
        {elidnis_stat_tile},
        {elidnis_stat_id}
    )
    qh.set_chat_options()
    moves = 0
    seen_screech = False
    last_tentacle_move = datetime.datetime.now() - datetime.timedelta(hours=1)
    # This is the anchor tile, where Odd Figure is located. Center of room
    anchor_tile = False
    tentacle_next = False
    last_freeze_attack = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        npcs = qh.get_npcs()
        for npc in npcs:
            if str(npc['id']) == odd_figure_id and not anchor_tile:
                anchor_tile = {
                    'x': npc['x_coord'],
                    'y': npc['y_coord'],
                    'z': 0
                }
                osrs.move.click(npc)
                # Don't set tiles to search for orbs and pillars until we know where our instance is located
                tile_map = osrs.util.generate_game_tiles_in_coords(
                    npc['x_coord'] - 15,
                    npc['x_coord'] + 15,
                    npc['y_coord'] - 15,
                    npc['y_coord'] + 15,
                    0
                )
                # during the orb phase, activating the blackstone
                # moves you to z 3
                tile_map_3 = osrs.util.generate_game_tiles_in_coords(
                    npc['x_coord'] - 15,
                    npc['x_coord'] + 15,
                    npc['y_coord'] - 15,
                    npc['y_coord'] + 15,
                    3
                )
                qh.set_game_objects(
                    set(tile_map + tile_map_3),
                    {good_orb, bad_orb}
                )
                while True:
                    qh.query_backend()
                    whisp = find_next_npc(qh.get_npcs(), whisperer_id)
                    if whisp:
                        osrs.move.click(whisp)
                        break
            elif str(npc['id']) == floating_pillar_normal_id and not seen_screech:
                phase += 1
                seen_screech = True
                handle_screech_attack(qh, anchor_tile)
            elif str(npc['id']) == whisperer_id and npc['health'] == 0:
                print('increment phase! old phase: ', phase)
        if qh.get_projectiles_v2():
            closest_projectile = {
                'id': 0,
                'startCycle': 9999991
            }
            for projectile in qh.get_projectiles_v2():
                if projectile['startCycle'] < closest_projectile['startCycle']:
                    closest_projectile = projectile
            if closest_projectile['id'] == 2444 or closest_projectile['id'] == 2445:
                tentacle_next = True
                print('range')
                res = pray_flick(closest_projectile, phase, qh, anchor_tile)
                if res == 1:
                    return qh
            # freeze and melee attack - i need to barrage her
            elif closest_projectile['id'] == 2467 and (datetime.datetime.now() - last_freeze_attack).total_seconds() > 20:
                # may need to set a skip here if she is already below 20% health to just equip my sage ax and kill her
                # click the ice barrage spell to manually cast
                osrs.keeb.press_key('f6')
                while True:
                    print('waiting for ice barrage to open')
                    qh.query_backend()
                    if qh.get_widgets(ice_barrage_id) and qh.get_widgets(ice_barrage_id)['x'] > 250:
                        break
                osrs.move.fast_click(qh.get_widgets(ice_barrage_id))
                whisp = find_next_npc(qh.get_npcs(), whisperer_melee_id)
                osrs.move.fast_move(whisp)
                osrs.clock.sleep_one_tick()
                osrs.move.fast_click(whisp)
                last_freeze_attack = datetime.datetime.now()
                continue
            # tortured souls special attack, kill the ones saying vita!
            elif closest_projectile['id'] == 668:
                phase += 1
                handle_vita_souls(qh, anchor_tile)
            else:
                continue
        elif qh.get_game_objects(bad_orb) and not ball_phase_complete:
            phase += 1
            osrs.player.toggle_prayer('on')
            osrs.clock.random_sleep(0.1, 0.2)
            osrs.player.toggle_prayer('off')
            # We are in the orb special, I step on one then continue attacking
            # I tank 30 damage for not completing all orbs
            # switch to inventory tab
            osrs.keeb.press_key('esc')
            while True:
                qh.query_backend()
                if qh.get_inventory(ready_blackstone_id):
                    print('world loc before click frag: ', qh.get_player_world_location())
                    osrs.move.click(qh.get_inventory(ready_blackstone_id))
                    break
            while True:
                qh.query_backend()
                if qh.get_game_objects(good_orb):
                    osrs.clock.random_sleep(1, 1.1)
                    break
            closest = False
            while True:
                qh.query_backend()
                if qh.get_game_objects(good_orb):
                    closest = osrs.util.find_closest_npc(qh.get_game_objects(good_orb))
                    break
            # need to finish this
            while True:
                qh.query_backend()
                if qh.get_game_objects(good_orb):
                    consumed_ball = True
                    for ball in qh.get_game_objects(good_orb):
                        # We have not consumed the orb yet
                        if ball['x_coord'] == closest['x_coord'] and ball['y_coord'] == closest['y_coord']:
                            consumed_ball = False
                    if consumed_ball:
                        osrs.move.click(qh.get_inventory(ready_blackstone_id))
                        osrs.clock.sleep_one_tick()
                        osrs.move.run_to_loc_v2(['{},{},0'.format(anchor_tile['x'], anchor_tile['y'] + 9)])
                        ball_phase_complete = True
                        qh.query_backend()
                        whisp = find_next_npc(qh.get_npcs(), whisperer_id)
                        osrs.move.click(whisp)
                        break
                    else:
                        osrs.move.spam_click('{},{},3'.format(closest['x_coord'], closest['y_coord']), .3)


while True:
    qh = main()
    collect_loot()
    restore_at_nardah(qh)


'''calculate_second_pillar(
    {'x': 819, 'y': 451, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 4, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 9604, 'y_coord': 2611, 'compositionID': 12209},
    {'x': 726, 'y': 394, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 7, 'graphic': -1, 'health': 40, 'scale': 40, 'x_coord': 9607, 'y_coord': 2609, 'compositionID': 12209},
    [{'x': 1280, 'y': 505, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 10, 'graphic': -1, 'health': 27, 'scale': 40, 'x_coord': 9590, 'y_coord': 2613, 'compositionID': 12209}, {'x': 960, 'y': 261, 'name': 'The Whisperer', 'id': 12204, 'dist': 10, 'graphic': 377, 'health': 44, 'scale': 80, 'x_coord': 9599, 'y_coord': 2604, 'compositionID': 12204}, {'x': 1182, 'y': 399, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 8, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 9592, 'y_coord': 2609, 'compositionID': 12209}, {'x': 1097, 'y': 451, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 5, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 9595, 'y_coord': 2611, 'compositionID': 12209}, {'x': 1010, 'y': 475, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 2, 'graphic': -1, 'health': 27, 'scale': 40, 'x_coord': 9598, 'y_coord': 2612, 'compositionID': 12209}, {'x': 913, 'y': 475, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 2, 'graphic': -1, 'health': 27, 'scale': 40, 'x_coord': 9601, 'y_coord': 2612, 'compositionID': 12209}, {'x': 819, 'y': 451, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 4, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 9604, 'y_coord': 2611, 'compositionID': 12209}, {'x': 726, 'y': 394, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 7, 'graphic': -1, 'health': 40, 'scale': 40, 'x_coord': 9607, 'y_coord': 2609, 'compositionID': 12209}, {'x': 654, 'y': 509, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 9, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 9609, 'y_coord': 2613, 'compositionID': 12209}]
)'''

#calculate_second_pillar({'x': 906, 'y': 537, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 1, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 11326, 'y_coord': 3188, 'compositionID': 12209}, {'x': 620, 'y': 445, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 10, 'graphic': -1, 'health': 40, 'scale': 40, 'x_coord': 11335, 'y_coord': 3185, 'compositionID': 12209}, [{'x': 1180, 'y': 569, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 7, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 11318, 'y_coord': 3189, 'compositionID': 12209}, {'x': 868, 'y': 307, 'name': 'The Whisperer', 'id': 12204, 'dist': 8, 'graphic': 377, 'health': 44, 'scale': 80, 'x_coord': 11327, 'y_coord': 3180, 'compositionID': 12204}, {'x': 1097, 'y': 449, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 5, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 11320, 'y_coord': 3185, 'compositionID': 12209}, {'x': 1005, 'y': 506, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 2, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 11323, 'y_coord': 3187, 'compositionID': 12209}, {'x': 906, 'y': 537, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 1, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 11326, 'y_coord': 3188, 'compositionID': 12209}, {'x': 816, 'y': 534, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 4, 'graphic': -1, 'health': 27, 'scale': 40, 'x_coord': 11329, 'y_coord': 3188, 'compositionID': 12209, 'thid_pillar_dist': 6.708203932499369}, {'x': 719, 'y': 506, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 7, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 11332, 'y_coord': 3187, 'compositionID': 12209}, {'x': 620, 'y': 445, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 10, 'graphic': -1, 'health': 40, 'scale': 40, 'x_coord': 11335, 'y_coord': 3185, 'compositionID': 12209}, {'x': 537, 'y': 569, 'name': '<col=00ffff>Floating Column</col>', 'id': 12209, 'dist': 12, 'graphic': -1, 'health': 14, 'scale': 40, 'x_coord': 11337, 'y_coord': 3189, 'compositionID': 12209}])