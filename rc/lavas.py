import datetime

import osrs

fire_altar_entrance_tile = '3313,3256,0'
fire_altar_tile = '2584,4839,0'
bank_tile = '2444,3083,0'
altar_id = '34764'
bank_id = '4483'
altar_entrance_id = '34817'
ring_of_dueling_ids = [
    2552,
    2554,
    2556,
    2558,
    2560,
    2562,
    2564
]
single_charge_dueling_id = 2566
binding_id = 5521
earth_talisman_id = 1440
pure_ess_id = 7936
earth_rune_id = 557


def find_equipment(equipment, ids):
    if not equipment or len(equipment) == 0:
        return False
    for item in equipment:
        if item['id'] in ids:
            return True
    return False


def withdraw_and_equip_items(qh, need_ring, need_binding):
    if need_ring or need_binding:
        if need_ring:
            ring = qh.get_bank(ring_of_dueling_ids)
            if not ring:
                exit('out of rings of dueling')
            osrs.move.click(ring)
        if need_binding:
            binding = qh.get_bank(binding_id)
            if not binding:
                exit('out of binding necklaces')
            osrs.move.click(binding)
        osrs.keeb.keyboard.press(osrs.keeb.key.esc)
        osrs.keeb.keyboard.release(osrs.keeb.key.esc)
        osrs.clock.sleep_one_tick()
        qh.query_backend()
        dueling = qh.get_inventory(ring_of_dueling_ids)
        if dueling:
            osrs.move.click(dueling)
        binding = qh.get_inventory(binding_id)
        if binding:
            osrs.move.click(binding)
        open_bank_interface(qh)


def dump_items(qh):
    qh.query_backend()
    if qh.get_inventory() and len(qh.get_inventory()) != 0:
        dump_inv = qh.get_widgets('12,42')
        if dump_inv:
            osrs.move.click(dump_inv)


def withdraw_materials(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    for item in [earth_talisman_id, earth_rune_id, pure_ess_id]:
        found_item = qh.get_bank(item)
        if not found_item:
            exit('out of {}'.format(found_item))
        if item == earth_talisman_id:
            osrs.move.click(found_item)
        else:
            osrs.move.right_click_v3(found_item, 'Withdraw-All')


def bank(qh):
    need_ring = not find_equipment(qh.get_equipment(), ring_of_dueling_ids)
    need_binding = not find_equipment(qh.get_equipment(), [binding_id])
    banking = open_bank_interface(qh)
    if not banking:
        return False
    osrs.clock.sleep_one_tick()
    dump_items(qh)
    withdraw_and_equip_items(qh, need_ring, need_binding)
    dump_items(qh)
    withdraw_materials(qh)
    osrs.keeb.keyboard.press(osrs.keeb.key.esc)
    osrs.keeb.keyboard.release(osrs.keeb.key.esc)
    osrs.clock.sleep_one_tick()


def open_bank_interface(qh):
    started_banking = datetime.datetime.now()
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        bank_chest = qh.get_game_objects(bank_id)
        if qh.get_bank():
            return True
        elif (datetime.datetime.now() - started_banking).total_seconds() > 30:
            return False
        elif bank_chest and len(bank_chest) > 0 and (datetime.datetime.now() - last_click).total_seconds() > 6:
            osrs.move.click(bank_chest[0])
            last_click = datetime.datetime.now()


def tele(qh, dest):
    while True:
        qh.query_backend()
        valid_rings = ring_of_dueling_ids if dest == 'pvp arena' else [] + ring_of_dueling_ids + [single_charge_dueling_id]
        have_ring = find_equipment(qh.get_equipment(), valid_rings)
        if not have_ring:
            return print('did not have a valid ring!!!')
        osrs.keeb.keyboard.press(osrs.keeb.key.f4)
        osrs.keeb.keyboard.release(osrs.keeb.key.f4)
        osrs.clock.sleep_one_tick()
        ring_slot = qh.get_widgets('387,24')
        if ring_slot:
            osrs.move.right_click_v3(ring_slot, dest)
            osrs.keeb.keyboard.press(osrs.keeb.key.esc)
            osrs.keeb.keyboard.release(osrs.keeb.key.esc)
            osrs.clock.random_sleep(3, 3.2)
            return


def run_to_altar(qh: osrs.queryHelper.QueryHelper()):
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    start = datetime.datetime.now()
    while True:
        qh.query_backend()
        curr_loc = qh.get_player_world_location()
        entrance = qh.get_game_objects(altar_entrance_id)
        if entrance and len(entrance) > 0 and (datetime.datetime.now() - last_click).total_seconds() > 6:
            osrs.move.click(entrance[0])
            last_click = datetime.datetime.now()
        elif (datetime.datetime.now() - start).total_seconds() > 30:
            return
        elif curr_loc and 2566 <= curr_loc['x'] <= 2599 and \
                4837 <= curr_loc['y'] <= 4853:
            return


def make_runes(qh: osrs.queryHelper.QueryHelper()):
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    start = datetime.datetime.now()
    while True:
        qh.query_backend()
        altar = qh.get_game_objects(altar_id)
        if altar and len(altar) > 0 and (datetime.datetime.now() - last_click).total_seconds() > 6:
            earth_rune = qh.get_inventory(earth_rune_id)
            if not earth_rune:
                print('DID NOT HAVE EARTH RUNES IN ALTAR. MAKIKNG FIRES.')
            else:
                osrs.move.click(earth_rune)
            osrs.move.click(altar[0])
            last_click = datetime.datetime.now()
        elif not altar:
            osrs.move.run_towards_square_v2({'x': 2584, 'y': 4839, 'z': 0})
        elif (datetime.datetime.now() - start).total_seconds() > 30:
            return
        elif not qh.get_inventory(pure_ess_id):
            return


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'387,24', '387,17', '12,42'})
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_game_objects({fire_altar_entrance_tile, fire_altar_tile, bank_tile}, {altar_id, bank_id, altar_entrance_id})
    qh.set_equipment()
    qh.set_bank()
    # got stuck at altar w no dueling, need to see why
    while True:
        qh.query_backend()
        curr_loc = qh.get_player_world_location()
        if curr_loc and 2435 <= curr_loc['x'] <= 2445 and \
                3082 <= curr_loc['y'] <= 3098:
            if len(qh.get_inventory()) == 28:
                tele(qh, 'pvp arena')
            else:
                bank(qh)
        elif curr_loc and 3300 <= curr_loc['x'] <= 3328 and \
                3224 <= curr_loc['y'] <= 3259:
            run_to_altar(qh)
        elif curr_loc and 2566 <= curr_loc['x'] <= 2599 and \
                4837 <= curr_loc['y'] <= 4853:
            if qh.get_inventory(pure_ess_id):
                make_runes(qh)
            else:
                tele(qh, 'castle wars')

main()
