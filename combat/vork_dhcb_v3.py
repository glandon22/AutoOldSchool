# TODO
'''
emergency tele gets stuck teleing over and over again
loot a until gone or inv full after each kill
eat and sip restore to full after each kill (other than final kill)
'''
import datetime
from pynput.keyboard import Key

import osrs

port = '56799'
waterbirth_portal_id = '29342'
rejuv_pool_id = '29241'
portal_nex_id = '33366' # this obj id changes based on which tele is left click FYI
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
rune_pouch_id = 12791
dust_rune_id = 4696
chaos_rune_id = 562
varrock_tele_tab = 8007
ruby_dragon_bolt_e = 21944
slay_staff_id = 4170
dhcb_id = 21012
diamond_dragon_bolts_e_id = 21946

required_items = [
    {'id': super_restore_ids[:2], 'all': False},
    {'id': anti_venom_pots[:3], 'all': False},
    {'id': divine_ranging_ids[:3], 'all': False},
    # Get two super restores
    # Note: It's hacky, but if there is 1 4 dose super restore left it will click it twice if they are back to back,
    # so breaking it up to ensure i have two restores. Can probably find a more elegant solution.
    {'id': super_restore_ids[:2], 'all': False},
    {'id': extended_super_anti_ids[:3], 'all': False},
    {'id': super_restore_ids[:2], 'all': False},
    {'id': rune_pouch_id, 'all': False},
    {'id': ruby_dragon_bolt_e, 'all': True},
    {'id': diamond_dragon_bolts_e_id, 'all': True},
    {'id': slay_staff_id, 'all': False},
    {'id': karambwan_id, 'all': True}
]


def anchor():
    loc = osrs.server.get_world_location(port)
    return loc


def wake_vork():
    osrs.player.toggle_run('on', port)
    while True:
        vork = osrs.server.get_npc_by_id('8059', port)
        if vork:
            osrs.move.move_and_click(vork['x'], vork['y'], 3, 3)
            break
    # once clicked, his ID changes as he wakes up, this is time to run to atk square
    while True:
        vork = osrs.server.get_npc_by_id('8059', port)
        if not vork:
            break


def start_trip():
    anchor_tile = anchor()
    wake_vork()
    inv = osrs.inv.get_inv(port)
    divine_ranging = osrs.inv.are_items_in_inventory_v2(inv, divine_ranging_ids)
    if not divine_ranging:
        print('NO RANGING POTS!')
    osrs.move.fast_move_and_click(divine_ranging['x'], divine_ranging['y'], 2, 2)
    osrs.move.run_to_loc_v2(
        ['{},{},0'.format(
            anchor_tile['x'] + attack_square_mid['x'], anchor_tile['y'] + attack_square_mid['y']
        )],
        port)
    super_anti = osrs.inv.are_items_in_inventory_v2(inv, extended_super_anti_ids)
    if not super_anti:
        tele_home()
    osrs.move.fast_move_and_click(super_anti['x'], super_anti['y'], 3, 3)
    return anchor_tile


def begin_vork_fight(anchor_tile):
    wake_vork()
    osrs.move.run_to_loc_v2(
        ['{},{},0'.format(
            anchor_tile['x'] + attack_square_mid['x'], anchor_tile['y'] + attack_square_mid['y']
        )],
        port)


def move_tiles_to_avoid_fireball_v3(anchor_tile, loc):
    # make sure i am going to a sq that is at least two tiles away!!!
    for sq in [attack_square_mid, attack_square_right, attack_square_left]:
        dist = osrs.dev.point_dist(loc['x'], loc['y'], anchor_tile['x'] + sq['x'], anchor_tile['y'] + sq['y'])
        if dist >= 2:
            osrs.move.spam_click('{},{},0'.format(anchor_tile['x'] + sq['x'], anchor_tile['y'] + sq['y']), 1, port)
            break
    vork = osrs.server.get_npc_by_id('8061', port)
    if vork:
        osrs.move.move_and_click(vork['x'], vork['y'], 3, 3)
    while True:
        fireball = osrs.server.get_projectiles()
        if 1481 not in fireball:
            return


def drink_anti_venom(inv):
    ven_pots = osrs.inv.are_items_in_inventory_v2(inv, anti_venom_pots)
    if ven_pots:
        osrs.move.fast_move_and_click(ven_pots['x'], ven_pots['y'], 3, 3)
    else:
        tele_home()


def eat_manta(inv):
    manta = osrs.inv.is_item_in_inventory_v2(inv, karambwan_id)
    if manta:
        osrs.move.fast_move_and_click(manta['x'], manta['y'], 3, 3)
    else:
        tele_home()


# once the spawn is dead, i need to wait until it disappears otherwise this function is triggered again and breaks
def kill_spawn(inv, orb):
    osrs.player.toggle_prayer('off', port)
    slay_staff = osrs.inv.is_item_in_inventory_v2(inv, slay_staff_id)
    if not slay_staff:
        tele_home()
    print('found slay staff', slay_staff)
    osrs.move.fast_move_and_click(slay_staff['x'], slay_staff['y'], 3, 3)
    # Wait to see the spawn once otherwise i could potentially exit loop while the spawn is sent out without killing
    start_time = datetime.datetime.now()
    while True:
        spawn = osrs.server.get_npc_by_id('8063', port)
        if spawn or (datetime.datetime.now() - start_time).total_seconds() > 10:
            print('found the spawn!', spawn)
            break
        osrs.player.toggle_prayer('off', port)
        food_handler(False, None)
        super_restore_handler(False, None)
    while True:
        spawn = osrs.server.get_npc_by_id('8063', port)
        print('spawn to kill: ', spawn)
        if spawn and spawn['health'] != 0:
            osrs.move.fast_move_and_click(spawn['x'], spawn['y'], 2, 2)
            print('attacking spawn')
        else:
            break
    osrs.move.fast_move_and_click(orb['x'], orb['y'], 2, 2)
    curr_inv = osrs.inv.get_inv(port)
    dhcb = osrs.inv.is_item_in_inventory_v2(curr_inv, dhcb_id)
    print('re equiping bow', dhcb)
    osrs.move.move_and_click(dhcb['x'], dhcb['y'], 3, 3)
    # the spawn may be killed but in the process of despawning, wait until that happens
    # so that this function is triggered again
    while True:
        spawn = osrs.server.get_npc_by_id('8063', port)
        if not spawn:
            osrs.player.toggle_prayer('on', port)
            break


def should_drink_super_restore(pd):
    if pd['boostedLevel'] + (pd['level'] * .25 + 8) <= pd['level']:
        return True
    else:
        return False


def super_restore_handler(required, emergency_handler):
    prayer_data = osrs.server.get_skill_data('prayer', port)
    if prayer_data and should_drink_super_restore(prayer_data):
        inv = osrs.inv.get_inv(port)
        super_restore = osrs.inv.are_items_in_inventory_v2(inv, super_restore_ids)
        if not super_restore and required:
            emergency_handler()
        elif super_restore:
            osrs.move.fast_move_and_click(super_restore['x'], super_restore['y'], 3, 3)
            osrs.clock.random_sleep(0.2, 0.3)


def food_handler(required, emergency_handler):
    hp_data = osrs.server.get_skill_data('hitpoints', port)
    if hp_data and hp_data['level'] - hp_data['boostedLevel'] >= 21:
        inv = osrs.inv.get_inv(port)
        food = osrs.inv.is_item_in_inventory_v2(inv, karambwan_id)
        # just topping up, may not be necessary to tele out yet
        if not food and required:
            emergency_handler()
        elif food:
            osrs.move.fast_move_and_click(food['x'], food['y'], 3, 3)
            osrs.clock.random_sleep(0.2, 0.3)


def avoid_acid_pools_v7(anchor_tile, inv, orb):
    # dont end this function until acid pools have landed - then gone away!
    acid_pools_seen = False
    # Step back to the anchor tile to ensure that i am going left to right on the safe tiles
    osrs.move.spam_click('{},{},0'.format(anchor_tile['x'], anchor_tile['y']), 0.6, port)
    # consider not using the fast click function here if i have enough time
    osrs.move.fast_move_and_click(orb['x'], orb['y'], 2, 2)
    osrs.player.toggle_run('off', port)
    last_click = datetime.datetime.now() - datetime.timedelta(seconds=50)
    direction = 0
    # if i kill vork right as the spec attack starts,
    # i may get stuck in a loop walking back and forth never seeing pools
    spec_att_start_time = datetime.datetime.now()
    while True:
        loc = osrs.server.get_world_location(port)
        if (datetime.datetime.now() - last_click).total_seconds() > .85:
            if direction == 1 and loc and loc['x'] < anchor_tile['x'] + 2:
                osrs.move.spam_click('{},{},0'.format(anchor_tile['x'] + 5, anchor_tile['y']), 0.25, port)
                last_click = datetime.datetime.now()
                direction = 0
            elif direction == 0 and loc and loc['x'] > anchor_tile['x'] - 2:
                osrs.move.spam_click('{},{},0'.format(anchor_tile['x'] - 5, anchor_tile['y']), 0.25, port)
                last_click = datetime.datetime.now()
                direction = 1

        acid_pools = osrs.server.get_surrounding_game_objects(6, ['32000'], port)
        if not acid_pools:
            if acid_pools_seen:
                break
            # only call to check if vork is still alive to decrease latency
            vork = osrs.server.get_npc_by_id('8061')
            if not vork:
                break
        elif acid_pools:
            acid_pools_seen = True
        super_restore_handler(False, None)
        food_handler(False, None)
        osrs.player.toggle_run('off', port)
        osrs.player.toggle_prayer('off', port)
        if (datetime.datetime.now() - spec_att_start_time).total_seconds() > 60:
            break
    osrs.player.toggle_run('on', port)
    # go back to the middle attack square after the acid pools spec atk
    osrs.move.spam_click('{},{},0'.format(anchor_tile['x'], anchor_tile['y'] + 1), 1, port)


# should add check to see if i am back in lumby and tele
def kill_vork(anchor_tile, last_super_anti_dose, last_divine_range_dose):
    # Store a variable to indicate if vorkath has gotten below 1/3 health
    # I use this in the instance that I kill vorkath right as the ice spawn
    # is thrown out to be able to break from the loop
    vork_low_health = False
    while True:
        q = {
            'npcsID': ['8061', '8063'],
            'projectiles': True,
            'interactingWith': True,
            # prayer orb, how to handle health orb?
            'widget': '160,21',
            'inv': True,
            'skills': ['hitpoints', 'prayer', 'ranged'],
            'gameObjects': [],
            'playerWorldPoint': True,
            'varBit': '6101'
        }

        tiles = osrs.util.generate_surrounding_tiles(5, port)
        items = ['32000', '4525']
        for tile in tiles:
            item_to_find = '20997'
            if len(items) > 0:
                item_to_find = items[len(items) - 1]
                items.pop()
            q['gameObjects'].append({
                'tile': tile,
                'object': str(item_to_find)
            })
        data = osrs.server.query_game_data(q, port)
        vork = list(filter(lambda npc: 'id' in npc and int(npc['id']) == 8061, data['npcs']))
        zombie_spawn = list(filter(lambda npc: 'id' in npc and int(npc['id']) == 8063, data['npcs']))
        projectiles = 'projectiles' in data and data['projectiles']
        interacting = 'interactingWith' in data and data['interactingWith']
        prayer_orb = 'widget' in data and data['widget']
        inv = 'inv' in data and data['inv']
        hp = 'skills' in data and 'hitpoints' in data['skills'] and data['skills']['hitpoints']
        prayer_skill_data = 'skills' in data and 'prayer' in data['skills'] and data['skills']['prayer']
        ranged_skill_data = 'skills' in data and 'prayer' in data['skills'] and data['skills']['ranged']
        acid_pools = 'gameObjects' in data and '32000' in data['gameObjects'] and data['gameObjects']['32000']
        # look for this to see if i had to emergency tele out
        house_portal = 'gameObjects' in data and '4525' in data['gameObjects'] and data['gameObjects']['4525']
        health_orb = osrs.server.get_widget('160,10', port)
        world_point = data['playerWorldPoint']
        super_antifire_status = 'varBit' in data and data['varBit']

        if 1481 in projectiles:
            print('fire ball incoming.')
            move_tiles_to_avoid_fireball_v3(anchor_tile, world_point)
            continue
        if 395 in projectiles or len(zombie_spawn) > 0:
            print('zombie spawn special.')
            kill_spawn(inv, prayer_orb)
            continue
            # vorkath is using the acid pools special attack
        if acid_pools or 1483 in projectiles:
            print('acid pools spec starting.')
            avoid_acid_pools_v7(anchor_tile, inv, prayer_orb)
            continue
        # i teled out
        if house_portal:
            return {}
        if 'boostedLevel' in hp and hp['boostedLevel'] < 50:
            print('hp under 50 - eating')
            eat_manta(inv)
            continue
        if prayer_skill_data and prayer_skill_data['boostedLevel'] < 20:
            print('prayer under 20 - sipping restore.')
            super_restore = osrs.inv.are_items_in_inventory_v2(inv, super_restore_ids)
            # I am low on prayer with no restores - bail
            if not super_restore:
                print('out of super restores')
            else:
                osrs.move.fast_move_and_click(super_restore['x'], super_restore['y'], 3, 3)
                osrs.clock.sleep_one_tick()
        # prayer disabled
        if prayer_orb and prayer_orb['spriteID'] == 1063:
            print('re enabling prayer')
            osrs.move.fast_move_and_click(prayer_orb['x'], prayer_orb['y'], 2, 2)
            # Wait for the click to register, otherwise it just clicks over and over again
            osrs.clock.sleep_one_tick()
            continue
        # I am venomed, drink antidote
        if health_orb and health_orb['spriteID'] == 1102:
            print('drinking anti venom')
            drink_anti_venom(inv)
            continue
        if not interacting and vork:
            if vork[0]['health'] == 0:
                print('killed vork')
                osrs.player.toggle_prayer('off', port)
                return {'anti': last_super_anti_dose, 'divine': last_divine_range_dose}
            print('attacking vork')
            osrs.move.move_and_click(vork[0]['x'], vork[0]['y'], 3, 3)
            continue
        if int(super_antifire_status) == 0:
            print('drinking super anti fire')
            super_anti_fire = osrs.inv.are_items_in_inventory_v2(inv, extended_super_anti_ids)
            if not super_anti_fire:
                tele_home()
            osrs.move.fast_move_and_click(super_anti_fire['x'], super_anti_fire['y'], 3, 3)
            continue
        if ranged_skill_data and ranged_skill_data['level'] == ranged_skill_data['boostedLevel']:
            print('repotting divine range')
            divine_range = osrs.inv.are_items_in_inventory_v2(inv, divine_ranging_ids)
            if not divine_range:
                print('OUT OF RANGING POTS!')
                continue
            osrs.move.fast_move_and_click(divine_range['x'], divine_range['y'], 3, 3)
            continue
        if vork and vork[0]['health'] / vork[0]['scale'] < .35 and not vork_low_health:
            print('vork below 30% health - switching bolts')
            vork_low_health = True
            bolt_switch = osrs.inv.is_item_in_inventory_v2(inv, diamond_dragon_bolts_e_id)
            if bolt_switch:
                osrs.move.fast_move_and_click(bolt_switch['x'], bolt_switch['y'], 3, 3)
                # have to sleep for a tick otherwise it just keeps switching back and forth
            continue
        if (vork and vork[0]['health'] == 0) or (not vork and vork_low_health):
            print('killed vork')
            osrs.player.toggle_prayer('off', port)
            return {'anti': last_super_anti_dose, 'divine': last_divine_range_dose}
        #  ensure i am always on one of the three attack tiles
        if world_point \
                and not (
                (world_point['x'] == anchor_tile['x'] + attack_square_mid['x']
                 and world_point['y'] == anchor_tile['y'] + attack_square_mid['y']) or
                (world_point['x'] == anchor_tile['x'] + attack_square_right['x']
                 and world_point['y'] == anchor_tile['y'] + attack_square_right['y']) or
                (world_point['x'] == anchor_tile['x'] + attack_square_left['x']
                 and world_point['y'] == anchor_tile['y'] + attack_square_left['y'])
        ):
            osrs.move.spam_click(
                '{},{},0'.format
                    (
                    anchor_tile['x'] + attack_square_mid['x'], anchor_tile['y'] + attack_square_mid['y']
                ),
                0.6,
                port
            )


def pickup_loot_v2():
    global loot
    global parsed_loot
    global loot_tile_list
    start_time = datetime.datetime.now()
    loot = None
    parsed_loot = []
    loot_tile_list = set()
    while True:
        loot = osrs.server.get_surrounding_ground_items_any_ids(15, port)
        # couldnt find loot in 30 seconds - bail
        if (datetime.datetime.now() - start_time).total_seconds() > 30:
            return
        elif loot:
            for _, value in loot.items():
                parsed_loot += value
            break
    for item in parsed_loot:
        print('lll', item)
        loot_tile_list.add('{},{},0'.format(item['x_coord'], item['y_coord']))
    start_time = datetime.datetime.now()
    while True:
        # bail after 30s
        if (datetime.datetime.now() - start_time).total_seconds() > 30:
            return
        for tile in loot_tile_list:
            while True:
                osrs.move.spam_click(tile, 0.6)
                # check if there is additional loot on this tile
                additional_loot = osrs.server.get_ground_items(tile, '9999999')
                print(additional_loot)
                if additional_loot:
                    curr_inv = osrs.inv.get_inv()
                    if len(curr_inv) == 28:
                        kara = osrs.inv.is_item_in_inventory_v2(curr_inv, karambwan_id)
                        # unable to make any more space in inv
                        if not kara:
                            return
                        osrs.move.move_and_click(kara['x'], kara['y'], 3, 3)
                else:
                    break
        break


# do this in between kills just to make sure im not missing out on loot
# if i have to emergency tele
def quick_pickup_loot():
    global quick_loot
    global quick_parsed_loot
    global quick_loot_tile_list
    start_time = datetime.datetime.now()
    quick_loot = None
    quick_parsed_loot = []
    quick_loot_tile_list = set()
    while True:
        quick_loot = osrs.server.get_surrounding_ground_items_any_ids(15, port)
        # couldnt find loot in 30 seconds - bail
        if (datetime.datetime.now() - start_time).total_seconds() > 30:
            return
        elif quick_loot:
            for _, value in quick_loot.items():
                quick_parsed_loot += value
            break
    for item in quick_parsed_loot:
        quick_loot_tile_list.add('{},{},0'.format(item['x_coord'], item['y_coord']))
    start_time = datetime.datetime.now()
    while True:
        # bail after 30s
        if (datetime.datetime.now() - start_time).total_seconds() > 30:
            return
        for tile in quick_loot_tile_list:
            while True:
                # check if there is additional loot on this tile
                additional_loot = osrs.server.get_ground_items(tile, '9999999')
                if additional_loot:
                    curr_inv = osrs.inv.get_inv()
                    # inv is full or the only thing left are the dhides (unnoted)
                    if len(curr_inv) == 28:
                        return
                    elif len(additional_loot.keys()) == 1 and '1751' in additional_loot:
                        break
                    osrs.move.spam_click(tile, 0.6)
                else:
                    break
        break


def have_supplies_for_kill():
    inv = osrs.inv.get_inv()
    food_count = osrs.inv.get_item_quantity_in_inv(inv, karambwan_id)
    if food_count < 6:
        print('did not have enough food for fight: {}'.format(inv))
        return False
    return True


def vork_handler_v2():
    anchor_tile = start_trip()
    last_super_anti_dose = datetime.datetime.now()
    last_divine_range_dose = datetime.datetime.now()
    for i in range(3):
        # ensure i have enough food otherwise dont start fight
        if not have_supplies_for_kill():
            return
        # first vork fight i drink pots, afterward just need to wake him up
        if i > 0:
            begin_vork_fight(anchor_tile)
        doses = kill_vork(anchor_tile, last_super_anti_dose, last_divine_range_dose)
        # had to emergency tele out
        if not bool(doses):
            return
        last_super_anti_dose = doses['anti']
        last_divine_range_dose = doses['divine']
        inv = osrs.inv.get_inv()
        bolt_switch = osrs.inv.is_item_in_inventory_v2(inv, ruby_dragon_bolt_e)
        if bolt_switch:
            osrs.move.fast_move_and_click(bolt_switch['x'], bolt_switch['y'], 3, 3)
        osrs.player.toggle_prayer_slow('off', port)
        food_handler(False, None)
        super_restore_handler(False, None)
        osrs.clock.random_sleep(2, 3)
        quick_pickup_loot()
    # sleep for a bit to ensure the final loot pile has dropped
    osrs.clock.random_sleep(4, 4.1)


def withdraw_item(item):
    bank = osrs.bank.get_bank_data()
    if type(item['id']) is list:
        item_loc = osrs.inv.are_items_in_inventory_v2(bank, item['id'])
        if not item_loc:
            exit('unable to find {}.'.format(item['id']))
        if item['all']:
            osrs.move.right_click_menu_select(item_loc, False, port, '', 'Withdraw-All-but-1')
        else:
            osrs.move.move_and_click(item_loc['x'], item_loc['y'], 3, 3)
    else:
        item_loc = osrs.inv.is_item_in_inventory_v2(bank, item['id'])
        if not item_loc:
            exit('unable to find {}.'.format(item['id']))
        if item['all']:
            osrs.move.right_click_menu_select(item_loc, False, port, '', 'Withdraw-All-but-1')
        else:
            osrs.move.move_and_click(item_loc['x'], item_loc['y'], 3, 3)


def bank_at_ferox():
    while True:
        chest = osrs.server.get_game_object('3130,3632,0', '26711', port)
        if not chest:
            continue
        osrs.move.move_and_click(chest['x'], chest['y'], 3, 3)
        start_time = datetime.datetime.now()
        while True:
            bank_tabs = osrs.server.get_widget('12,11', port)
            if bank_tabs:
                osrs.clock.sleep_one_tick()
                osrs.bank.bank_dump_inv(port)
                # sometimes if the bank interface is just about to open, its position is wrong. so let the interace
                # fully open before doing any action
                bank_tabs = osrs.server.get_widget('12,11', port)
                # click the third tab
                osrs.move.move_and_click(bank_tabs['x'] - 100, bank_tabs['y'], 3, 3)
                osrs.clock.sleep_one_tick()
                for item in required_items:
                    withdraw_item(item)
                osrs.keeb.keyboard.press(Key.esc)
                osrs.keeb.keyboard.release(Key.esc)
                osrs.clock.sleep_one_tick()
                inv = osrs.inv.get_inv()
                bolt_switch = osrs.inv.is_item_in_inventory_v2(inv, ruby_dragon_bolt_e)
                if bolt_switch:
                    osrs.move.fast_move_and_click(bolt_switch['x'], bolt_switch['y'], 3, 3)
                return
            elif (datetime.datetime.now() - start_time).total_seconds() > 10:
                break


def bank_at_lunar_isle():
    while True:
        chest = osrs.server.get_game_object('2099,3920,0', '16700', port)
        if not chest:
            continue
        osrs.move.move_and_click(chest['x'], chest['y'], 3, 3)
        start_time = datetime.datetime.now()
        while True:
            bank_tabs = osrs.server.get_widget('12,11', port)
            if bank_tabs:
                osrs.clock.sleep_one_tick()
                osrs.bank.bank_dump_inv(port)
                # sometimes if the bank interface is just about to open, its position is wrong. so let the interace
                # fully open before doing any action
                bank_tabs = osrs.server.get_widget('12,11', port)
                # click the third tab
                osrs.move.move_and_click(bank_tabs['x'] - 100, bank_tabs['y'], 3, 3)
                osrs.clock.sleep_one_tick()
                for item in required_items:
                    withdraw_item(item)
                osrs.keeb.keyboard.press(Key.esc)
                osrs.keeb.keyboard.release(Key.esc)
                osrs.clock.sleep_one_tick()
                inv = osrs.inv.get_inv()
                bolt_switch = osrs.inv.is_item_in_inventory_v2(inv, ruby_dragon_bolt_e)
                if bolt_switch:
                    osrs.move.fast_move_and_click(bolt_switch['x'], bolt_switch['y'], 3, 3)
                return
            elif (datetime.datetime.now() - start_time).total_seconds() > 10:
                break


def get_deported_from_lunar_isle():
    while True:
        chest = osrs.server.get_game_object('2098,3920,0', '16700', port)
        if not chest:
            continue
        osrs.move.move_and_click(chest['x'], chest['y'], 3, 3)
        start_time = datetime.datetime.now()
        while True:
            loc = osrs.server.get_world_location(port)
            if loc and 2640 > loc['x'] > 2620 and 3640 < loc['y'] < 3690:
                return
            elif (datetime.datetime.now() - start_time).total_seconds() > 10:
                break
            else:
                osrs.keeb.keyboard.type(' ')


def tele_home():
    print('teleing home')
    attempts = 0
    while True:
        attempts += 1
        if attempts > 25:
            return print('tried to tele home 25 times')
        osrs.keeb.keyboard.press(Key.f6)
        osrs.keeb.keyboard.release(Key.f6)
        osrs.clock.random_sleep(0.2, 0.3)
        home_tele_button = osrs.server.get_widget('218,29', port)
        if home_tele_button:
            osrs.move.move_and_click(home_tele_button['x'], home_tele_button['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = osrs.server.get_world_location(port)
                if loc and loc['x'] > 4000:
                    osrs.player.toggle_prayer('off')
                    osrs.clock.random_sleep(2.5, 2.7)
                    osrs.keeb.keyboard.press(Key.esc)
                    osrs.keeb.keyboard.release(Key.esc)
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 15:
                    break


def enter_waterbirth_portal():
    while True:
        portal = osrs.server.get_surrounding_game_objects(15, [waterbirth_portal_id], port)
        if portal and waterbirth_portal_id in portal:
            osrs.move.move_and_click(portal[waterbirth_portal_id]['x'], portal[waterbirth_portal_id]['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = osrs.server.get_world_location(port)
                if loc and loc['x'] < 3000:
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 15:
                    break


def drink_from_pool():
    while True:
        osrs.player.toggle_prayer('off')
        rejuv_pool = osrs.server.get_surrounding_game_objects(15, [rejuv_pool_id], port)
        if rejuv_pool and rejuv_pool_id in rejuv_pool:
            osrs.move.move_and_click(rejuv_pool[rejuv_pool_id]['x'], rejuv_pool[rejuv_pool_id]['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                prayer_data = osrs.server.get_skill_data('prayer')
                if prayer_data and prayer_data['level'] == prayer_data['boostedLevel']:
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 7:
                    break


def tele_to_lunar_isle():
    while True:
        nexus = osrs.server.get_surrounding_game_objects(15, [portal_nex_id], port)
        if nexus and portal_nex_id in nexus:
            osrs.move.move_and_click(nexus[portal_nex_id]['x'], nexus[portal_nex_id]['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = osrs.server.get_world_location(port)
                if loc and 2120 > loc['x'] > 2090 and 3900 < loc['y'] < 3930:
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 7:
                    break


# might consider making exit condition that the tile i want to walk to has x and y coords on screen w a get tile call
# not sure if that would work but worth investigation
def travel_to_rellekka():
    while True:
        jarvald = osrs.server.get_npc_by_id('10407', port)
        if jarvald:
            osrs.move.move_and_click(jarvald['x'], jarvald['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = osrs.server.get_world_location(port)
                if loc and loc['y'] < 3700:
                    osrs.clock.random_sleep(4, 4.1)
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 9:
                    break


def take_boat_to_ungael_v2():
    print('taking boat to ungael')
    q = {
        'tiles': ['2640,3694,0']
    }

    # wait until relleka is loaded on screen!
    while True:
        data = osrs.server.query_game_data(q)
        if 'tiles' in data and data['tiles'] and '264036940' in data['tiles']:
            break

    while True:
        # 10405 torfinn
        boat = osrs.server.get_game_object('2638,3698,0', '29917', port)
        if boat:
            osrs.move.move_and_click(boat['x'], boat['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = osrs.server.get_world_location(port)
                if loc and loc['y'] > 4000:
                    osrs.clock.random_sleep(1.5, 2)
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 9:
                    break
        loc = osrs.server.get_world_location(port)
        if loc and loc['y'] > 4000:
            return


def enter_vorks_layer_v2():
    print('entering lair')
    while True:
        ice = osrs.server.get_game_object('2272,4053,0', '31990', port)
        print('get ice patch', ice)
        if ice:
            osrs.move.move_and_click(ice['x'], ice['y'], 3, 3)
            start_time = datetime.datetime.now()
            while True:
                loc = osrs.server.get_world_location(port)
                if loc and loc['x'] > 5000:
                    osrs.clock.random_sleep(2.5, 3)
                    return
                elif (datetime.datetime.now() - start_time).total_seconds() > 9:
                    break
        # may have clicked the ice patch already
        else:
            loc = osrs.server.get_world_location(port)
            if loc and loc['x'] > 5000:
                osrs.clock.random_sleep(1.5, 2)
                return


script_config = {
    'intensity': 'high',
    'logout': False,
    'login': False
}


# start at ferox w gear on
def vork_loop():
    while True:
        osrs.game.break_manager_v3(script_config)
        bank_at_lunar_isle()
        get_deported_from_lunar_isle()
        take_boat_to_ungael_v2()
        enter_vorks_layer_v2()
        vork_handler_v2()
        pickup_loot_v2()
        tele_home()
        drink_from_pool()
        tele_to_lunar_isle()
