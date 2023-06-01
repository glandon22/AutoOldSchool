import datetime

from pynput.keyboard import Key

from osrs_utils import general_utils

port = '56799'
waterbirth_portal_id = '29342'
attack_square_left = {
    'x': -2,
    'y': 1
}

attack_square_mid = {
    'x': 0,
    'y': 1
}

attack_square_right = {
    'x': 2,
    'y': 1
}

karambwan_id = 3144

ring_of_dueling_ids = [
    2552,
    2554,
    2556,
    2558,
    2560,
    2562,
    2564,
    2566
]

anti_venom_pots = [
    12913,
    12915,
    12917,
    12919
]

super_restore_ids = [
    3024,
    3026,
    3028,
    3030
]

divine_ranging_ids = [
    23733,
    23736,
    23739,
    23742
]

extended_super_anti_ids = [
    22209,
    22212,
    22215,
    22218
]

law_rune_id = 563
dust_rune_id = 4696
chaos_rune_id = 562
varrock_tele_tab = 8007
ruby_dragon_bolt_e = 21944
slay_staff_id = 4170
dhcb_id = 21012
diamond_dragon_bolts_e_id = 21946

required_multi_items = [
    anti_venom_pots[:3],
    divine_ranging_ids[:3],
    super_restore_ids[:3],
    extended_super_anti_ids[:3],
    ring_of_dueling_ids
]

required_items = [
    {'id': anti_venom_pots[:3], 'all': False},
    {'id': divine_ranging_ids[:3], 'all': False},
    # Get two super restores
    {'id': super_restore_ids[:3], 'all': False},
    {'id': super_restore_ids[:3], 'all': False},
    {'id': extended_super_anti_ids[:3], 'all': False},
    {'id': ring_of_dueling_ids, 'all': False},
    {'id': law_rune_id, 'all': True},
    {'id': chaos_rune_id, 'all': True},
    {'id': dust_rune_id, 'all': True},
    {'id': ruby_dragon_bolt_e, 'all': True},
    {'id': slay_staff_id, 'all': False},
    {'id': karambwan_id, 'all': True}
]

def anchor():
    loc = general_utils.get_world_location(port)
    return loc


def wake_vork():
    general_utils.toggle_run('on', port)
    while True:
        vork = general_utils.get_npc_by_id('8059', port)
        if vork:
            general_utils.move_and_click(vork['x'],vork['y'], 3, 3)
            break
    # once clicked, his ID changes as he wakes up, this is time to run to atk square
    while True:
        vork = general_utils.get_npc_by_id('8059', port)
        if not vork:
            break


def start_trip():
    anchor_tile = anchor()
    wake_vork()
    inv = general_utils.get_inv(port)
    divine_ranging = general_utils.are_items_in_inventory_v2(inv, divine_ranging_ids)
    if not divine_ranging:
        print('NO RANGING POTS!')
    general_utils.fast_move_and_click(divine_ranging['x'], divine_ranging['y'], 2, 2)
    general_utils.run_to_loc_v2(
        ['{},{},0'.format(
            anchor_tile['x'] + attack_square_mid['x'], anchor_tile['y'] + attack_square_mid['y']
        )],
        port)
    super_anti = general_utils.are_items_in_inventory_v2(inv, extended_super_anti_ids)
    if not super_anti:
        emergency_tele_out(inv)
    general_utils.fast_move_and_click(super_anti['x'], super_anti['y'], 3, 3)
    return anchor_tile


def begin_vork_fight(anchor_tile):
    wake_vork()
    general_utils.run_to_loc_v2(
        ['{},{},0'.format(
            anchor_tile['x'] + attack_square_mid['x'], anchor_tile['y'] + attack_square_mid['y']
        )],
        port)


def move_tiles_to_avoid_fireball_v2(anchor_tile):
    loc = general_utils.get_world_location(port)
    # I am standing on middle tile, so go right
    if loc and loc['x'] == anchor_tile['x'] and loc['y'] == anchor_tile['y'] + 1:
        general_utils.run_to_loc_v2(
            ['{},{},0'.format(
                anchor_tile['x'] + attack_square_right['x'], anchor_tile['y'] + attack_square_right['y']
            )],
            port)
    else:
        general_utils.run_to_loc_v2(
            ['{},{},0'.format(
                anchor_tile['x'], anchor_tile['y'] + 1
            )],
            port)
    vork = general_utils.get_npc_by_id('8061', port)
    if vork:
        general_utils.move_and_click(vork['x'], vork['y'], 3, 3)
    while True:
        fireball = general_utils.get_projectiles()
        if 1481 not in fireball:
            return


def drink_anti_venom(inv):
    ven_pots = general_utils.are_items_in_inventory_v2(inv, anti_venom_pots)
    if ven_pots:
        general_utils.fast_move_and_click(ven_pots['x'], ven_pots['y'], 3, 3)
    else:
        emergency_tele_out(inv)


def emergency_tele_out(inv):
    v_tab = general_utils.is_item_in_inventory_v2(inv, varrock_tele_tab)
    general_utils.fast_move_and_click(v_tab['x'], v_tab['y'], 3, 3)


def eat_manta(inv):
    manta = general_utils.is_item_in_inventory_v2(inv, karambwan_id)
    if manta:
        general_utils.fast_move_and_click(manta['x'], manta['y'], 3, 3)
    else:
        emergency_tele_out(inv)


# once the spawn is dead, i need to wait until it disappears otherwise this function is triggered again and breaks
def kill_spawn(inv, orb):
    general_utils.toggle_prayer('off', port)
    slay_staff = general_utils.is_item_in_inventory_v2(inv, slay_staff_id)
    if not slay_staff:
        emergency_tele_out(inv)
    print('found slay staff', slay_staff)
    general_utils.fast_move_and_click(slay_staff['x'], slay_staff['y'], 3, 3)
    # Wait to see the spawn once otherwise i could potentially exit loop while the spawn is sent out without killing
    start_time = datetime.datetime.now()
    while True:
        spawn = general_utils.get_npc_by_id('8063', port)
        if spawn or (datetime.datetime.now() - start_time).total_seconds() > 10:
            print('found the spawn!', spawn)
            break
    while True:
        spawn = general_utils.get_npc_by_id('8063', port)
        print('spawn to kill: ', spawn)
        if spawn and spawn['health'] != 0:
            general_utils.fast_move_and_click(spawn['x'], spawn['y'], 2, 2)
            print('attacking spawn')
        else:
            break
    general_utils.fast_move_and_click(orb['x'], orb['y'], 2, 2)
    curr_inv = general_utils.get_inv(port)
    dhcb = general_utils.is_item_in_inventory_v2(curr_inv, dhcb_id)
    print('re equiping bow', dhcb)
    general_utils.move_and_click(dhcb['x'], dhcb['y'], 3, 3)
    # the spawn may be killed but in the process of despawning, wait until that happens
    # so that this function is triggered again
    while True:
        spawn = general_utils.get_npc_by_id('8063', port)
        if not spawn:
            general_utils.toggle_prayer('on', port)
            break


def should_drink_super_restore(pd):
    if pd['boostedLevel'] + (pd['level'] * .25 + 8) <= pd['level']:
        return True
    else:
        return False


def avoid_acid_pools_v6(anchor_tile, inv, orb):
    # dont end this function until acid pools have landed - then gone away!
    acid_pools_seen = False
    # Step back to the anchor tile to ensure that i am going left to right on the safe tiles
    general_utils.spam_click('{},{},0'.format(anchor_tile['x'], anchor_tile['y']), 0.6, port)
    # consider not using the fast click function here if i have enough time
    general_utils.fast_move_and_click(orb['x'], orb['y'], 2, 2)
    general_utils.toggle_run('off', port)
    last_click = datetime.datetime.now() - datetime.timedelta(seconds=50)
    direction = 0
    # if i kill vork right as the spec attack starts,
    # i may get stuck in a loop walking back and forth never seeing pools
    spec_att_start_time = datetime.datetime.now()
    while True:
        loc = general_utils.get_world_location(port)
        if (datetime.datetime.now() - last_click).total_seconds() > .85:
            if direction == 1 and loc and loc['x'] < anchor_tile['x'] + 2:
                general_utils.spam_click('{},{},0'.format(anchor_tile['x'] + 3, anchor_tile['y']), 0.25, port)
                last_click = datetime.datetime.now()
                direction = 0
            elif direction == 0 and loc and loc['x'] > anchor_tile['x'] - 2:
                general_utils.spam_click('{},{},0'.format(anchor_tile['x'] - 3, anchor_tile['y']), 0.25, port)
                last_click = datetime.datetime.now()
                direction = 1

        acid_pools = general_utils.get_surrounding_game_objects(6, ['32000'], port)
        if not acid_pools and acid_pools_seen:
            break
        elif acid_pools:
            acid_pools_seen = True
        prayer_data = general_utils.get_skill_data('prayer', port)
        if prayer_data and should_drink_super_restore(prayer_data):
            inv = general_utils.get_inv(port)
            super_restore = general_utils.are_items_in_inventory_v2(inv, super_restore_ids)
            # just topping up, may not be necessary to tele out yet
            if not super_restore:
                continue
            general_utils.fast_move_and_click(super_restore['x'], super_restore['y'], 3, 3)
        hp_data = general_utils.get_skill_data('hitpoints', port)
        if hp_data and hp_data['level'] - hp_data['boostedLevel'] >= 21:
            inv = general_utils.get_inv(port)
            manta_ray = general_utils.is_item_in_inventory_v2(inv, karambwan_id)
            # just topping up, may not be necessary to tele out yet
            if not manta_ray:
                continue
            general_utils.fast_move_and_click(manta_ray['x'], manta_ray['y'], 3, 3)
        general_utils.toggle_run('off', port)
        general_utils.toggle_prayer('off', port)
        if (datetime.datetime.now() - spec_att_start_time).total_seconds() > 60:
            break
    general_utils.toggle_run('on', port)
    # go back to the middle attack square after the acid pools spec atk
    general_utils.spam_click('{},{},0'.format(anchor_tile['x'], anchor_tile['y'] + 1), 1, port)


def tele_to_ferox():
    while True:
        inv = general_utils.get_inv()
        duelings = general_utils.are_items_in_inventory_v2(inv, ring_of_dueling_ids)
        if not duelings:
            return print('no more rings of dueling')
        general_utils.right_click_menu_select(duelings, None, port, 'Ring', 'Rub')
        general_utils.sleep_one_tick()
        general_utils.keyboard.type('3')
        start_time = datetime.datetime.now()
        while True:
            loc = general_utils.get_world_location()
            if (datetime.datetime.now() - start_time).total_seconds() > 30:
                break
            elif loc and 3147 <= loc['x'] <= 3154 and 3630 <= loc['y'] <= 3638:
                return


def drink_from_pool_of_refreshment():
    while True:
        pool = general_utils.get_game_object('3129,3634,0', '39651', port)
        if not pool:
            general_utils.run_towards_square_v2('3137,3628,0', port)
            continue
        general_utils.move_and_click(pool['x'], pool['y'], 3, 3)
        start_time = datetime.datetime.now()
        while True:
            if (datetime.datetime.now() - start_time).total_seconds() > 15:
                break
            stats = general_utils.get_skill_data(['prayer', 'hitpoints'])
            if stats \
                and stats['hitpoints']['boostedLevel'] == stats['hitpoints']['level'] \
                and stats['prayer']['boostedLevel'] == stats['prayer']['level']:
                return


def kill_vork(anchor_tile, last_super_anti_dose, last_divine_range_dose):
    while True:
        q = {
            'npcsID': ['8061', '8063'],
            'projectiles': True,
            'interactingWith': True,
            # prayer orb, how to handle health orb?
            'widget': '160,21',
            'inv': True,
            'skills': ['hitpoints', 'prayer'],
            'gameObjects': []
        }

        tiles = general_utils.generate_surrounding_tiles(5, port)
        items = ['32000']
        for tile in tiles:
            item_to_find = '20997'
            if len(items) > 0:
                item_to_find = items[len(items) - 1]
                items.pop()
            q['gameObjects'].append({
                'tile': tile,
                'object': str(item_to_find)
            })
        data = general_utils.query_game_data(q, port)
        vork = list(filter(lambda npc: 'id' in npc and int(npc['id']) == 8061, data['npcs']))
        zombie_spawn = list(filter(lambda npc: 'id' in npc and int(npc['id']) == 8063, data['npcs']))
        projectiles = 'projectiles' in data and data['projectiles']
        interacting = 'interactingWith' in data and data['interactingWith']
        prayer_orb = 'widget' in data and data['widget']
        inv = 'inv' in data and data['inv']
        hp = 'skills' in data and 'hitpoints' in data['skills'] and data['skills']['hitpoints']
        prayer_skill_data = 'skills' in data and 'prayer' in data['skills'] and data['skills']['prayer']
        acid_pools = 'gameObjects' in data and data['gameObjects']
        health_orb = general_utils.get_widget('160,10', port)
        if 1481 in projectiles:
            move_tiles_to_avoid_fireball_v2(anchor_tile)
            continue
        if 395 in projectiles or len(zombie_spawn) > 0:
            kill_spawn(inv, prayer_orb)
            continue
            # vorkath is using the acid pools special attack
        if acid_pools or 1483 in projectiles:
            avoid_acid_pools_v6(anchor_tile, inv, prayer_orb)
            continue
        if 'boostedLevel' in hp and hp['boostedLevel'] < 50:
            eat_manta(inv)
            continue
        if prayer_skill_data and prayer_skill_data['boostedLevel'] < 20:
            super_restore = general_utils.are_items_in_inventory_v2(inv, super_restore_ids)
            # I am low on prayer with no restores - bail
            if not super_restore:
                emergency_tele_out(inv)
                return print('RAN OUT OF SUPER RESTORES')
            general_utils.fast_move_and_click(super_restore['x'], super_restore['y'], 3, 3)
            general_utils.sleep_one_tick()
        # prayer disabled
        if prayer_orb and prayer_orb['spriteID'] == 1063:
            general_utils.fast_move_and_click(prayer_orb['x'], prayer_orb['y'], 2, 2)
            # Wait for the click to register, otherwise it just clicks over and over again
            general_utils.sleep_one_tick()
            continue
        # I am venomed, drink antidote
        if health_orb and health_orb['spriteID'] == 1102:
            drink_anti_venom(inv)
            continue
        if not interacting and vork:
            if vork[0]['health'] == 0:
                print('killed vork')
                general_utils.toggle_prayer('off', port)
                return {'anti': last_super_anti_dose, 'divine': last_divine_range_dose}
            general_utils.move_and_click(vork[0]['x'], vork[0]['y'], 3, 3)
            continue
        if (datetime.datetime.now() - last_super_anti_dose).total_seconds() > 355:
            super_anti_fire = general_utils.are_items_in_inventory_v2(inv, extended_super_anti_ids)
            if not super_anti_fire:
                emergency_tele_out(inv)
            general_utils.fast_move_and_click(super_anti_fire['x'], super_anti_fire['y'], 3, 3)
            last_super_anti_dose = datetime.datetime.now()
            continue
        if (datetime.datetime.now() - last_divine_range_dose).total_seconds() > 295:
            divine_range = general_utils.are_items_in_inventory_v2(inv, divine_ranging_ids)
            if not divine_range:
                print('OUT OF RANGING POTS!')
            general_utils.fast_move_and_click(divine_range['x'], divine_range['y'], 3, 3)
            last_divine_range_dose = datetime.datetime.now()
            continue
        if vork and vork[0]['health'] / vork[0]['scale'] < .33:
            bolt_switch = general_utils.is_item_in_inventory_v2(inv, diamond_dragon_bolts_e_id)
            if bolt_switch:
                general_utils.fast_move_and_click(bolt_switch['x'], bolt_switch['y'], 3, 3)
                # have to sleep for a tick otherwise it just keeps switching back and forth
                general_utils.random_sleep(0.8, 0.9)
            continue
        if vork and vork[0]['health'] == 0:
            general_utils.toggle_prayer('off', port)
            return {'anti': last_super_anti_dose, 'divine': last_divine_range_dose}


def vork_handler_v2():
    anchor_tile = start_trip()
    last_super_anti_dose = datetime.datetime.now()
    last_divine_range_dose = datetime.datetime.now()
    for i in range(2):
        # first vork fight i drink pots, afterward just need to wake him up
        if i > 0:
            begin_vork_fight(anchor_tile)
        doses = kill_vork(anchor_tile, last_super_anti_dose, last_divine_range_dose)
        last_super_anti_dose = doses['anti']
        last_divine_range_dose = doses['divine']
        # switch back to ruby dragon bolts here TODO@@
        general_utils.random_sleep(2, 3)
    # turn off prayer
    # kill him again
    # loot the shit

def withdraw_item(item):
    bank = general_utils.get_bank_data()
    if type(item['id']) is list:
        item_loc = general_utils.are_items_in_inventory_v2(bank, item['id'])
        if not item_loc:
            exit('unable to find {}.'.format(item['id']))
        if item['all']:
            general_utils.right_click_menu_select(item_loc, False, port, '', 'Withdraw-All')
        else:
            general_utils.move_and_click(item_loc['x'], item_loc['y'], 3, 3)
    else:
        item_loc = general_utils.is_item_in_inventory_v2(bank, item['id'])
        if not item_loc:
            exit('unable to find {}.'.format(item['id']))
        if item['all']:
            general_utils.right_click_menu_select(item_loc, False, port, '', 'Withdraw-All')
        else:
            general_utils.move_and_click(item_loc['x'], item_loc['y'], 3, 3)


def bank_at_ferox():
    while True:
        chest = general_utils.get_game_object('3130,3632,0', '26711', port)
        if not chest:
            continue
        general_utils.move_and_click(chest['x'], chest['y'], 3, 3)
        start_time = datetime.datetime.now()
        while True:
            bank_tabs = general_utils.get_widget('12,11', port)
            if bank_tabs:
                general_utils.sleep_one_tick()
                general_utils.bank_dump_inv(port)
                # sometimes if the bank interface is just about to open, its position is wrong. so let the interace
                # fully open before doing any action
                bank_tabs = general_utils.get_widget('12,11', port)
                # click the third tab
                general_utils.move_and_click(bank_tabs['x'] - 100, bank_tabs['y'], 3, 3)
                general_utils.sleep_one_tick()
                for item in required_items:
                    withdraw_item(item)
                general_utils.keyboard.press(Key.esc)
                general_utils.keyboard.release(Key.esc)
                return
            elif (datetime.datetime.now() - start_time).total_seconds() > 10:
                break


def tele_home():
    while True:
        general_utils.keyboard.press(Key.f6)
        general_utils.keyboard.release(Key.f6)
        general_utils.random_sleep(0.2, 0.3)
        home_tele_button = general_utils.get_widget('218,29', port)
        if home_tele_button:
            general_utils.move_and_click(home_tele_button['x'], home_tele_button['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = general_utils.get_world_location(port)
                if loc and loc['x'] > 4000:
                    general_utils.random_sleep(2, 2.3)
                    general_utils.keyboard.press(Key.esc)
                    general_utils.keyboard.release(Key.esc)
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 15:
                    break


def enter_waterbirth_portal():
    while True:
        portal = general_utils.get_surrounding_game_objects(15, [waterbirth_portal_id], port)
        if portal and waterbirth_portal_id in portal:
            general_utils.move_and_click(portal[waterbirth_portal_id]['x'], portal[waterbirth_portal_id]['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = general_utils.get_world_location(port)
                if loc and loc['x'] < 3000:
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 15:
                    break


def travel_to_rellekka():
    while True:
        jarvald = general_utils.get_npc_by_id('10407', port)
        if jarvald:
            general_utils.move_and_click(jarvald['x'], jarvald['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = general_utils.get_world_location(port)
                if loc and loc['y'] < 3700:
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 9:
                    break


def take_boat_to_ungael():
    while True:
        general_utils.run_towards_square_v2({'x': 2641, 'y': 3695, 'z': 0}, port)
        # 10405 torfinn
        torfinn = general_utils.get_npc_by_id('10405', port)
        if torfinn:
            general_utils.move_and_click(torfinn['x'], torfinn['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = general_utils.get_world_location(port)
                if loc and loc['y'] > 4000:
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 9:
                    break


def enter_vorks_layer():
    while True:
        general_utils.run_towards_square_v2({'x': 2272, 'y': 4047, 'z': 0}, port)
        ice = general_utils.get_game_object('2272,4053,0', '31990', port)
        if ice:
            general_utils.move_and_click(ice['x'], ice['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = general_utils.get_world_location(port)
                if loc and loc['x'] > 5000:
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 9:
                    break

'''general_utils.random_sleep(1, 2)
tele_home()
enter_waterbirth_portal()
travel_to_rellekka()
take_boat_to_ungael()
enter_vorks_layer()'''
vork_handler_v2()