from datetime import datetime

import osrs
from trailblazer_scripts.tb4_zammy import ranger_id

'''
notes
luanr isle portal id 28339

tele home
drink restore pool
lunar isle portal
bank
talk to sirsal banker and get deported
run to 2640,3687,0
click torfinn - in ungael 2277,4034,0
run to 2272,4048,0
click 31990 then in instance break
toggle run off
drink divine then drink antifire
kill
toggle run on
start again!
'''
equipment = [
    {'id': osrs.item_ids.DRAGONFIRE_WARD_22003, 'consume': 'Wield'},
    {'id': osrs.item_ids.AVAS_ACCUMULATOR, 'consume': 'Wear'},
    {'id': osrs.item_ids.VOID_RANGER_HELM, 'consume': 'Wear'},
    {'id': osrs.item_ids.VOID_KNIGHT_GLOVES, 'consume': 'Wear'},
    {'id': osrs.item_ids.ARCHERS_RING_I, 'consume': 'Wear'},
    {'id': osrs.item_ids.BOOTS_OF_BRIMSTONE, 'consume': 'Wear'},
    {'id': osrs.item_ids.VOID_KNIGHT_TOP, 'consume': 'Wear'},
    {'id': osrs.item_ids.VOID_KNIGHT_ROBE, 'consume': 'Wear'},
    {'id': osrs.item_ids.SALVE_AMULETEI, 'consume': 'Wear'},
    {'id': osrs.item_ids.DRAGON_HUNTER_CROSSBOW, 'consume': 'Wield'},
    {'id': osrs.item_ids.RUBY_DRAGON_BOLTS_E, 'consume': 'Equip'},
]

trip_supplies = [
    {
        'id': [
            osrs.item_ids.DIAMOND_DRAGON_BOLTS_E
        ],
        'quantity': 'All'
    },
    osrs.item_ids.SUPER_RESTORE4,
    osrs.item_ids.SUPER_RESTORE4,
    osrs.item_ids.SUPER_RESTORE4,
    osrs.item_ids.DIVINE_RANGING_POTION4,
    osrs.item_ids.EXTENDED_ANTIVENOM4,
    osrs.item_ids.EXTENDED_SUPER_ANTIFIRE4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.SLAYERS_STAFF,
    {
        'id': [
            osrs.item_ids.COOKED_KARAMBWAN
        ],
        'quantity': 'All'
    },
]

acid_pool_id = 32000
loot = osrs.loot.Loot()


def in_lunar_isle():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 2058 <= qh.get_player_world_location('x') <= 2120 and 3845 <= qh.get_player_world_location('y') <= 3953:
        return True


def in_ungael():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 2238 <= qh.get_player_world_location('x') <= 2304 and 4032 <= qh.get_player_world_location('y') <= 4098:
        return True


def in_instance():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_player_world_location('x') >= 3967:
        return True


def determine_anchor():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {31822})
    while True:
        qh.query_backend()
        if qh.get_objects_v2('game'):
            anchor = qh.get_objects_v2('game')[0]
            return {
                'left': {'x': anchor['x_coord'] - 2, 'y': anchor['y_coord'] + 2, 'z': 0},
                'middle': {'x': anchor['x_coord'], 'y': anchor['y_coord'] + 2, 'z': 0},
                'right': {'x': anchor['x_coord'] + 2, 'y': anchor['y_coord'] + 2, 'z': 0}
            }


def wake_vork():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([8059, 8058, 8061])
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        # vorkath is awake or waking up
        if osrs.util.find_closest_target_in_game(
                qh.get_npcs(), qh.get_player_world_location(), lambda npc: npc['id'] == 8061 or npc['id'] == 8058
        ):
            return
        elif osrs.util.find_closest_target_in_game(
                qh.get_npcs(), qh.get_player_world_location(), lambda npc: npc['id'] == 8059
        ):
            osrs.move.fast_click_v2(
                osrs.util.find_closest_target_in_game(qh.get_npcs(), qh.get_player_world_location(),
                                                      lambda npc: npc['id'] == 8059)
            )


def avoid_fireball(projectile_destination, player_loc, anchor):
    # this first filters out any of the three safe tiles that are less than two tiles
    # away from the fireball destination. thats because you need to be at least two tiles
    # away to avoid damage. it then sorts the remaining tiles by which is closest to me
    dest = sorted(filter(
        lambda tile: osrs.dev.point_dist(
            projectile_destination['x'], projectile_destination['y'], tile['x'], tile['y']
        ) >= 2.0,
        osrs.util.combine_objects(anchor)
    ), key=lambda tile: osrs.dev.point_dist(
            player_loc['x'], player_loc['y'], tile['x'], tile['y']
        ))
    if len(dest):
        dest = dest[0]
    parsed_tile = osrs.util.tile_objects_to_strings([dest])[0]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_destination_tile()
    qh.set_projectiles_v2()
    qh.set_npcs([8061])
    qh.set_tiles({parsed_tile})
    while True:
        qh.query_backend()
        if qh.get_player_world_location() == dest:
            if not list(filter(lambda proj: proj['id'] == 1481, qh.get_projectiles_v2())):
                return
            elif qh.get_npcs():
                osrs.move.fast_click_v2(qh.get_npcs()[0])
        elif qh.get_destination_tile() != dest and qh.get_tiles(parsed_tile):
            osrs.move.fast_click_v2(qh.get_tiles(parsed_tile))


# there are three safe tiles in the chamber
# to guarantee a clean back row when the
# acid attack occurs, make sure to
# be on one of them at all times
def on_safe_tile(player_loc, anchor):
    for loc in anchor:
        if player_loc == anchor[loc]:
            return True
    return False


def kill_spawn():
    seen = False
    osrs.player.equip_item([osrs.item_ids.SLAYERS_STAFF])
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['8063'])
    qh.set_inventory()
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
    qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62'})
    qh.set_active_prayers()
    start = datetime.now()
    while True:
        qh.query_backend()
        spawn = osrs.util.find_closest_target_on_screen(qh.get_npcs(), lambda npc: npc['health'] != 0)
        if spawn:
            seen = True
            osrs.move.fast_click_v2(spawn)
        # i can kill vork right after the ice projectile comes out without the spawn ever appearing
        elif seen or (datetime.now() - start).total_seconds() > 30:
            osrs.dev.logger.info('Killed zombie spawn.')
            osrs.player.equip_item([osrs.item_ids.DRAGON_HUNTER_CROSSBOW])
            return
        elif not seen:
            osrs.combat_utils.fast_food_handler(qh, 80)
            osrs.combat_utils.pot_handler(qh, {'PRAYER': True}, min_prayer=55)


def avoid_acid(middle_anchor):
    seen_fireballs = False
    right_end = f"{middle_anchor['x'] + 4},{middle_anchor['y'] - 1},0"
    left_end = f"{middle_anchor['x'] - 4},{middle_anchor['y'] - 1},0"
    middle_tile_safe = f"{middle_anchor['x'] + 1},{middle_anchor['y'] - 1},0"
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {acid_pool_id})
    qh.set_npcs([8061])
    qh.set_player_world_location()
    qh.set_tiles({right_end, left_end, middle_tile_safe})
    qh.set_inventory()
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
    qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62'})
    qh.set_active_prayers()
    while True:
        qh.query_backend()
        if qh.get_objects_v2('game', acid_pool_id):
            seen_fireballs = True

        # fireballs have come and gone or vorkath is dead
        if (seen_fireballs and not qh.get_objects_v2('game', acid_pool_id)) or not qh.get_npcs():
            return
        # make sure i am actually on the back row
        elif qh.get_player_world_location('y') != middle_anchor['y'] - 1 and qh.get_tiles(middle_tile_safe):
            osrs.move.fast_click_v2(qh.get_tiles(middle_tile_safe))
        # I am on the right side of safe tiles
        elif qh.get_player_world_location('x') >= middle_anchor['x'] and qh.get_tiles(left_end):
            osrs.move.fast_click_v2(qh.get_tiles(left_end))
        # I am on the left side of safe tiles
        #elif qh.get_player_world_location('x') <= middle_anchor['x'] - 2 and qh.get_tiles(right_end):
        elif qh.get_tiles(right_end):
            osrs.move.fast_click_v2(qh.get_tiles(right_end))
            osrs.combat_utils.fast_food_handler(qh, 80)
            osrs.combat_utils.pot_handler(qh, {'PRAYER': True}, min_prayer=55)
            osrs.move.fast_click_v2(qh.get_tiles(right_end))


def wait_for_loot():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('ground_items', set())
    while True:
        qh.query_backend()
        if qh.get_objects_v2('ground_items', osrs.item_ids.SUPERIOR_DRAGON_BONES):
            osrs.dev.logger.info('Found loot: %s', qh.get_objects_v2('ground_items'))
            return True


def kill_vork(anchor):
    switched_bolts = False
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([8059, 8061, 8063])
    qh.set_projectiles_v2()
    qh.set_var_player(['102'])
    qh.set_widgets({'160,21', '160,29'}.union(osrs.combat_utils.pot_handler_required_prayer_widgets))
    qh.set_interating_with()
    qh.set_widgets({
        osrs.widget_ids.prayer_orb_widget_id
    })
    qh.set_inventory()
    qh.set_skills({'hitpoints', 'prayer', 'ranged'}.union(osrs.combat_utils.pot_handler_required_skills))
    qh.set_player_world_location()
    qh.set_varbit('6101')
    qh.set_objects_v2('game', {acid_pool_id})
    pot_config = osrs.combat_utils.PotConfig(superantifire=True, antivenom=True, prayer=True, ranging=True).asdict()
    while True:
        qh.query_backend()
        # turn run off if it is on
        if qh.get_widgets('160,29') and qh.get_widgets('160,29')['spriteID'] == 1065:
            osrs.move.fast_click_v2(qh.get_widgets('160,29'))
        osrs.combat_utils.fast_food_handler(qh, 35)
        osrs.combat_utils.turn_on_quick_prayers(qh)
        osrs.combat_utils.pot_handler(qh, pot_config)
        vorkath = list(filter(lambda npc: npc['id'] == 8061, qh.get_npcs() or []))
        acid_projectile = list(filter(lambda proj: proj['id'] == 1483, qh.get_projectiles_v2() or []))
        zombie_spawn_projectile = list(filter(lambda proj: proj['id'] == 395, qh.get_projectiles_v2() or []))
        fireball = list(filter(lambda proj: proj['id'] == 1481, qh.get_projectiles_v2() or []))

        if fireball:
            osrs.dev.logger.warning('Fireball incoming!')
            avoid_fireball(fireball[0]['destination'], qh.get_player_world_location(), anchor)
        elif zombie_spawn_projectile:
            osrs.dev.logger.warning('Zombie spawn incoming!')
            osrs.combat_utils.turn_off_quick_prayers(qh)
            kill_spawn()
        elif acid_projectile or qh.get_objects_v2('game', acid_pool_id):
            osrs.dev.logger.warning('Acid attack incoming!')
            osrs.combat_utils.turn_off_quick_prayers(qh)
            avoid_acid(anchor['middle'])
        elif not on_safe_tile(qh.get_player_world_location(), anchor):
            avoid_fireball({'x': 0, 'y': 0, 'z': 0}, qh.get_player_world_location(), anchor)
        elif not qh.get_interating_with() and vorkath:
            osrs.move.fast_click_v2(vorkath[0])
        elif not switched_bolts and vorkath and vorkath[0]['health'] / vorkath[0]['scale'] < .35:
            osrs.player.equip_item([osrs.item_ids.DIAMOND_DRAGON_BOLTS_E])
            switched_bolts = True
        elif (vorkath and vorkath[0]['health'] == 0) or (not vorkath and switched_bolts):
            osrs.player.equip_item([osrs.item_ids.RUBY_DRAGON_BOLTS_E])
            osrs.combat_utils.turn_off_quick_prayers(qh)
            osrs.player.toggle_run('on')
            return


while True:
    osrs.player.toggle_run('on')
    osrs.game.break_manager_v4({
        'intensity': 'high',
        'login': False,
        'logout': False,
    })
    osrs.game.tele_home_v2()
    osrs.game.click_restore_pool()
    osrs.move.interact_with_object_v3(
        29339, custom_exit_function=in_lunar_isle, obj_dist=25, right_click_option='Enter',
        timeout=9
    )
    osrs.bank.banking_handler({
        'dump_inv': True,
        'withdraw_v2': trip_supplies
    })
    osrs.game.talk_to_npc('sirsal banker', right_click=True)
    osrs.game.dialogue_handler([], 1)
    osrs.move.go_to_loc(2640, 3687)
    osrs.game.talk_to_npc('torfinn', custom_exit=in_ungael)
    osrs.move.go_to_loc(2272, 4048)
    osrs.move.interact_with_object_v3(
        31990, custom_exit_function=in_instance
    )
    for i in range(2):
        wake_vork()
        kill_vork(determine_anchor())
        wait_for_loot()
        loot.retrieve_loot(dist=25, disable_alchs=True)