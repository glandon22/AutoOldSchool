import datetime

import osrs

seers_bank_tile = '2724,3494,0'
seers_bank_id = '25808'
bandos_bank_tab = '12,10,3'  # spriteID -202 means it is highlighted
ice_barrage_id = '218,79'
crystal_memories_id = '25104'
divine_pouch_id = '27281'
globetrotter_necklace_id = '28765'
bandos_full_helm_id = '12486'
pray_pot_id = '139'
karambwan_id = '3144'
pre_seers_altar_tile = '2724,3462,0'
seers_altar_tile = '2694,3462,0'
seers_altar_object_id = '409'
bandos_room_door_id = '26503'
bandos_room_door_tile = '2863,5354,2'

graardor_id = '2215'
mager_id = '2217'
ranger_id = '2218'
meleer_id = '2216'
void_mage_helm = '11663'

# Items to pick up
bcp_id = '11832'
b_tassys_id = '11834'
bandos_boots_id = '11836'
bandos_hilt_id = '11812'
shard_1_id = '11818'
shard_2_id = '11820'
shard_3_id = '11822'
noted_grimy_snap_id = '3052'
snap_seed_id = '5300'
noted_magic_logs_id = '1514'
super_restore_id = '3024'
scroll_box_hard_id = '24364'
scroll_box_elite_id = '24365'


def bank(qh: osrs.queryHelper.QueryHelper):
    last_bank_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    qh.query_backend()
    if osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), karambwan_id) >= 3 and \
            osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), pray_pot_id) >= 1 and \
            len(qh.get_inventory()) < 28:
        osrs.move.click(qh.get_inventory(bandos_full_helm_id))
        return
    while True:
        qh.query_backend()
        if qh.get_game_objects(seers_bank_id) and (datetime.datetime.now() - last_bank_click).total_seconds() > 5:
            osrs.move.click(qh.get_game_objects(seers_bank_id)[0])
            last_bank_click = datetime.datetime.now()
        elif qh.get_bank():
            break
    if qh.get_widgets(bandos_bank_tab) and qh.get_widgets(bandos_bank_tab)['spriteID'] == -201:
        osrs.move.click(qh.get_widgets(bandos_bank_tab))
    osrs.bank.dump_items()
    osrs.clock.sleep_one_tick()
    qh.query_backend()
    if qh.get_bank():
        for item in [
            crystal_memories_id, divine_pouch_id, globetrotter_necklace_id, bandos_full_helm_id, pray_pot_id,
            karambwan_id
        ]:
            bank_item = qh.get_bank(item)
            if bank_item:
                # withdraw 5 pray pots and karambwans
                if item == pray_pot_id or item == karambwan_id:
                    osrs.move.click(bank_item)
                    osrs.move.click(bank_item)
                    osrs.move.click(bank_item)
                    osrs.move.click(bank_item)
                    osrs.move.click(bank_item)
                else:
                    osrs.move.click(bank_item)
    osrs.keeb.press_key('esc')
    qh.query_backend()
    if qh.get_inventory(bandos_full_helm_id):
        osrs.move.click(qh.get_inventory(bandos_full_helm_id))


def pray_at_seers_altar(qh: osrs.queryHelper.QueryHelper):
    while True:
        qh.query_backend()
        if qh.get_skills('prayer')['boostedLevel'] > 25:
            break
        elif qh.get_game_objects(seers_altar_object_id):
            osrs.move.fast_click(qh.get_game_objects(seers_altar_object_id)[0])
            osrs.clock.sleep_one_tick()
        else:
            osrs.move.run_towards_square_v2({'x': 2724, 'y': 3462, 'z': 0})
            osrs.move.run_towards_square_v2({'x': 2715, 'y': 3462, 'z': 0})


def return_to_gwd(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    if qh.get_inventory(crystal_memories_id):
        osrs.move.click(qh.get_inventory(crystal_memories_id))
        osrs.clock.random_sleep(4, 4.2)


def enter_bandos_room(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    osrs.player.toggle_prayer('on')
    door = qh.get_game_objects(bandos_room_door_id)
    if door:
        osrs.move.right_click_v3(door[0], 'Open (private)')


def find_next_npc(npcs, target):
    for npc in npcs:
        if int(npc['id']) == int(target):
            return npc


def barrage_bandos(qh: osrs.queryHelper.QueryHelper):
    osrs.keeb.press_key('f6')
    while True:
        qh.query_backend()
        if qh.get_widgets(ice_barrage_id):
            break
    osrs.move.fast_click(qh.get_widgets(ice_barrage_id))
    qh.query_backend()
    graardoor = find_next_npc(qh.get_npcs(), graardor_id)
    if graardoor:
        osrs.move.click(graardoor)
    osrs.keeb.press_key('esc')


def find_next_target(npcs):
    res = False
    for npc in npcs:
        if npc['health'] != 0:
            if not res or npc['dist'] < res['dist']:
                res = npc
    return res


def world_points_equal(p1, p2):
    try:
        equal = int(p1['x']) == int(p2['x']) and int(p1['y']) == int(p2['y']) and int(p1['z']) == int(p2['z'])
        return equal
    except:
        return False


def kill_bandos(qh: osrs.queryHelper.QueryHelper):
    anchor_point = False
    last_freeze = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location() and qh.get_player_world_location()['x'] > 5000:
            anchor_point = qh.get_player_world_location()
            break
    # first barrage isnt working, also the dist check isnt working either
    barrage_bandos(qh)
    # Equip my void mage helm and blast him
    while True:
        qh.query_backend()
        if qh.get_inventory(void_mage_helm):
            osrs.move.click(qh.get_inventory(void_mage_helm))
            osrs.move.click(find_next_npc(qh.get_npcs(), graardor_id))
            break
    # Monitor fight
    while True:
        qh.query_backend()
        graardor = find_next_npc(qh.get_npcs(), graardor_id)
        if qh.get_skills('hitpoints') and qh.get_skills('hitpoints')['boostedLevel'] < 40:
            if qh.get_inventory(karambwan_id):
                osrs.move.fast_click(qh.get_inventory(karambwan_id))
            else:
                osrs.move.right_click_v3(qh.get_inventory(globetrotter_necklace_id), 'Last-destination')
                osrs.clock.sleep_one_tick()
                return 'failed'
        elif graardor and graardor['dist'] <= 2 and (datetime.datetime.now() - last_freeze).total_seconds() > 10:
            print('refreezing bandos', qh.get_player_world_location(), anchor_point)
            barrage_bandos(qh)
            last_freeze = datetime.datetime.now()
            if world_points_equal(qh.get_player_world_location(), anchor_point):
                print('time to move')
                curr_pt = qh.get_player_world_location()
                print('destination: ', {'x': curr_pt['x'], 'y': curr_pt['y'], 'z': curr_pt['z']})
                osrs.move.run_towards_square_v2({'x': curr_pt['x'] + 10, 'y': curr_pt['y'], 'z': curr_pt['z']})
            else:
                osrs.move.run_towards_square_v2(anchor_point)
        elif not graardor or (graardor and graardor['health'] == 0):
            osrs.player.toggle_prayer('off')
            # finish off the minions
            while True:
                qh.query_backend()
                if qh.get_npcs():
                    targ = find_next_target(qh.get_npcs())
                    if targ:
                        if not qh.get_interating_with():
                            osrs.move.fast_click(targ)
                    else:
                        break
            return
        elif graardor and not qh.get_interating_with() == 'General Graardor':
            osrs.move.fast_click(graardor)


def loot(qh: osrs.queryHelper.QueryHelper):
    while True:
        found_loot = False
        loot_items = osrs.server.get_surrounding_ground_items_any_ids(15)
        qh.query_backend()
        # sometimes a minion that i killed before i killed graardor will respawn after i kill graardor,
        # so make sure to kill them before looting
        if qh.get_npcs():
            targ = find_next_target(qh.get_npcs())
            if targ:
                if not qh.get_interating_with():
                    osrs.move.fast_click(targ)
                continue
        for item in [
            bcp_id,
            b_tassys_id,
            bandos_boots_id,
            bandos_hilt_id,
            shard_1_id, shard_2_id, shard_3_id,
            noted_grimy_snap_id, snap_seed_id, noted_magic_logs_id,
            super_restore_id, scroll_box_hard_id, scroll_box_elite_id
        ]:
            if item in loot_items:
                found_loot = True
                print('picking up item: ', item)
                osrs.move.right_click_v3(loot_items[item][0], 'Take')
                loot_click = datetime.datetime.now()
                prev_inv = qh.get_inventory()
                while True:
                    qh.query_backend()
                    if len(qh.get_inventory()) == 28:
                        return
                    elif qh.get_inventory() != prev_inv or (datetime.datetime.now() - loot_click).total_seconds() > 7:
                        osrs.clock.sleep_one_tick()
                        break
            # found loot, so break out of the search and look ago
            if found_loot:
                break
        # found no loot after cycling through all items, end search
        if not found_loot:
            break


script_config = {
    'intensity': 'high',
    'login': False,
    'logout': lambda: osrs.clock.random_sleep(11, 14),
}


def main():
    # in seers:
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_objects(
        {seers_bank_tile, seers_altar_tile, bandos_room_door_tile},
        {seers_bank_id, seers_altar_object_id, bandos_room_door_id}
    )
    qh.set_widgets({bandos_bank_tab, ice_barrage_id})
    qh.set_bank()
    qh.set_interating_with()
    qh.set_inventory()
    qh.set_skills({'prayer', 'hitpoints'})
    qh.set_npcs([graardor_id, mager_id, meleer_id, ranger_id])
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        # in Seer's Village
        if qh.get_player_world_location() \
                and 2685 < qh.get_player_world_location()['x'] < 2785 \
                and qh.get_player_world_location()['y'] < 3600:
            bank(qh)
            pray_at_seers_altar(qh)
            osrs.game.break_manager_v4(script_config)
            return_to_gwd(qh)
        elif qh.get_player_world_location() \
                and 2844 < qh.get_player_world_location()['x'] < 2863 \
                and qh.get_player_world_location()['y'] < 5400:
            enter_bandos_room(qh)
            result = kill_bandos(qh)
            loot(qh)
            qh.query_backend()
            if result != 'failed':
                osrs.move.right_click_v3(qh.get_inventory(globetrotter_necklace_id), 'Last-destination')


main()
