import datetime

import osrs

seers_bank_tile = '2724,3494,0'
seers_bank_id = '25808'
bandos_bank_tab = '12,10,3'  # spriteID -202 means it is highlighted
crystal_memories_id = '25104'
divine_pouch_id = '27281'
globetrotter_necklace_id = '28765'
bandos_full_helm_id = '12486'
pray_pot_id = '139'
karambwan_id = '3144'
pre_seers_altar_tile = '2724,3462,0'
seers_altar_tile = '2694,3462,0'
seers_altar_object_id = '409'
bandos_room_door_id = '26505'
bandos_room_door_tile = '2925,5332,2'
ice_barrage_id = '218,79'
graardor_id = '3129'
mager_id = '3130'
ranger_id = '3131'
meleer_id = '3132'

# Items to pick up
zammy_hilt = '11816'
staff_dead = '11791'

desert_am_4_id = '13136'

elidnis_stat_id = '10389'
elidnis_stat_tile = '3427,2930,0'

sage_axe = '28773'
ancient_staff = '4675'


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


def restore_at_nardah(qh: osrs.queryHelper.QueryHelper):
    curr_time = datetime.datetime.now()
    if curr_time.hour == 2:
        return print('its 2am')
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
        osrs.move.click(qh.get_inventory(crystal_memories_id))
        osrs.clock.random_sleep(3, 3.1)
        return


def find_next_npc(npcs, target):
    for npc in npcs:
        if int(npc['id']) == int(target):
            return npc


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
    start_mage_xp = 0
    last_freeze = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        start_mage_xp = qh.get_skills('magic')['xp']
        if qh.get_player_world_location() and qh.get_player_world_location()['x'] > 5000:
            anchor_point = qh.get_player_world_location()
            # 2925 5331 2 -> x - 7
            break
    # hit 2 max hits on zammy then freeze
    hits = 0
    while True:
        qh.query_backend()
        zammy = find_next_npc(qh.get_npcs(), graardor_id)
        if zammy:
            osrs.move.fast_click(zammy)
        if qh.get_skills('magic')['xp'] != start_mage_xp:
            hits += 1
            start_mage_xp = qh.get_skills('magic')['xp']
        if hits == 2:
            break
    barrage_bandos(qh)
    osrs.move.spam_click('{},{},2'.format(anchor_point['x'] - 7, anchor_point['y']), 1.1)
    # Monitor fight
    while True:
        qh.query_backend()
        graardor = find_next_npc(qh.get_npcs(), graardor_id)
        if qh.get_skills('hitpoints') and qh.get_skills('hitpoints')['boostedLevel'] < 42:
            return 'failed'
        elif not graardor or (graardor and graardor['health'] == 0):
            osrs.clock.random_sleep(5, 5.1)
            return 'success'
        elif graardor and qh.get_interating_with() and not 'K\'ril' in qh.get_interating_with():
            osrs.move.fast_click(graardor)


def loot_v2(qh: osrs.queryHelper.QueryHelper, result):
    if result == 'failed':
        return
    # Wait for arma loot to appear
    while True:
        loot_items = osrs.server.get_surrounding_ground_items_any_ids(15)
        print('waiting for loot.')
        if loot_items:
            print('found loot: ', loot_items)
            break
    while True:
        loot_items = osrs.server.get_surrounding_ground_items_any_ids(15)
        print('loot', loot_items)
        qh.query_backend()
        found_loot = False
        for item in [zammy_hilt, staff_dead]:
            print(item)
            if item in loot_items:
                print('picking up item: ', item)
                found_loot = True
                osrs.move.right_click_v3(loot_items[item][0], 'Take')
                osrs.clock.random_sleep(3, 3.1)
        if found_loot:
            continue
        else:
            print('no remaining loot to pick up: ', loot_items)
            return


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
    osrs.clock.random_sleep(0.8, 0.88)


script_config = {
    'intensity': 'high',
    'login': lambda: osrs.clock.random_sleep(4, 5),
    'logout': lambda: osrs.clock.random_sleep(11, 14),
}


def main():
    # in seers:
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_objects(
        {seers_bank_tile, seers_altar_tile, bandos_room_door_tile, elidnis_stat_tile},
        {seers_bank_id, seers_altar_object_id, bandos_room_door_id, elidnis_stat_id}
    )
    qh.set_widgets({bandos_bank_tab,ice_barrage_id})
    qh.set_bank()
    qh.set_interating_with()
    qh.set_inventory()
    qh.set_skills({'prayer', 'hitpoints', 'magic'})
    qh.set_npcs([graardor_id, mager_id, meleer_id, ranger_id])
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        # in Seer's Village
        if qh.get_player_world_location() \
                and 2685 < qh.get_player_world_location()['x'] < 2785 \
                and qh.get_player_world_location()['y'] < 3600:
            bank(qh)
            return_to_gwd(qh)
        elif qh.get_player_world_location() \
                and 2900 < qh.get_player_world_location()['x'] < 2932 \
                and qh.get_player_world_location()['y'] < 5350:
            enter_bandos_room(qh)
            result = kill_bandos(qh)
            loot_v2(qh, result)
            qh.query_backend()
            restore_at_nardah(qh)


