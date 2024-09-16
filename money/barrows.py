import datetime

import osrs

logger = osrs.dev.instantiate_logger()
varrock_tele_widget_id = '218,23'
tunnel_monsters_for_points = [
    1678,
    1679,
    1680,
    1681,
    1682,
    1683,
    1684,
    1685,
    1686,
    1687,
    1688,
]

equipment = [
    osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
    osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
    osrs.item_ids.ItemIDs.SHARK.value,
    osrs.item_ids.ItemIDs.SHARK.value,
    osrs.item_ids.ItemIDs.SHARK.value,
    osrs.item_ids.ItemIDs.SHARK.value,
    osrs.item_ids.ItemIDs.SHARK.value,
    osrs.item_ids.ItemIDs.SHARK.value,
    osrs.item_ids.ItemIDs.SHARK.value,
    osrs.item_ids.ItemIDs.SHARK.value,
    osrs.item_ids.ItemIDs.SPADE.value,
    osrs.item_ids.ItemIDs.TOXIC_BLOWPIPE.value,
    osrs.item_ids.ItemIDs.RUNE_POUCH.value,
    osrs.item_ids.ItemIDs.ABYSSAL_WHIP.value,
    osrs.item_ids.ItemIDs.AVAS_ACCUMULATOR.value,
    osrs.item_ids.ItemIDs.SALVE_AMULETEI.value,
    {
        'id': [
            osrs.item_ids.ItemIDs.STRANGE_OLD_LOCKPICK_FULL.value,
            osrs.item_ids.ItemIDs.STRANGE_OLD_LOCKPICK.value,
        ],
        'quantity': '1'
    },

]

class BarrowsBrother():
    def __init__(self, mound_tile, crypt_id, staircase_id, npc_id, prayer):
        self.mound_tile = mound_tile
        self.crypt_id = crypt_id
        self.staircase_id = staircase_id
        self.npc_id = npc_id
        self.prayer = prayer

    def as_dict(self):
        return {
            'mound_tile': self.mound_tile,
            'crypt_id': self.crypt_id,
            'staircase_id': self.staircase_id,
            'npc_id': self.npc_id,
            'prayer': self.prayer,
        }


tunnel_brother = None


def enter_mound():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('z') == 3:
            return
        elif qh.get_inventory(osrs.item_ids.ItemIDs.SPADE.value):
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.SPADE.value))


def find_my_target(brother):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([brother])
    qh.set_widgets({'229,1'})
    qh.query_backend()
    if qh.get_widgets('229,1'):
        return True
    if qh.get_npcs():
        for npc in qh.get_npcs():
            # make sure the final brother is in the chest room so i can attack!
            if npc['id'] == brother and 'interacting' in npc and npc['interacting'].lower() == 'DJT Fan 14':
                osrs.move.fast_click(npc)
                osrs.move.fast_click(npc)
                osrs.move.fast_click(npc)
                return True


def find_my_target_in_chest_room(args):
    brother = args[0]
    time = args[1]
    logger.info(f"total time searching for final brother: {(datetime.datetime.now() - time).total_seconds()}")
    # sometimes the brother spawns close to the chest room
    # and when i open the chest it just despawns
    # instead of spawning again in the chest room
    if (datetime.datetime.now() - time).total_seconds() > 10:
        return True
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([brother])
    qh.set_widgets({'229,1'})
    qh.set_objects_v2('game', {20973})
    qh.set_canvas()
    qh.query_backend()
    if qh.get_npcs():
        for npc in qh.get_npcs():
            if npc['id'] == brother:
                print('brother found: ', npc)
            # make sure the final brother is in the chest room so i can attack!
            if (npc['id'] == brother
                    and 'interacting' in npc
                    and npc['interacting'].lower() == 'DJT Fan 14'
                    and 3546 <= npc['x_coord'] <= 3557
                    and 9689 <= npc['y_coord'] <= 9700):
                logger.info("found final brother, attacking!")
                osrs.move.fast_click(npc)
                osrs.move.fast_click(npc)
                osrs.move.fast_click(npc)
                return True


def loot_popup():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'155,1'})
    qh.query_backend()
    if qh.get_widgets('155,1'):
        return True


# loot widget 155,1
def awaken_brother(brother: BarrowsBrother, tunnel):
    logger.info("Running to mound.")
    osrs.move.go_to_loc(*brother.as_dict()['mound_tile'])
    enter_mound()
    logger.info("searching crypt.")
    osrs.move.interact_with_object(
        brother.as_dict()['crypt_id'], 'a', 1, False, right_click_option='Search',
        custom_exit_function=find_my_target, custom_exit_function_arg=brother.as_dict()['npc_id'], timeout=8
    )
    not_found = kill_brother(brother.as_dict()['npc_id'], brother.as_dict()['prayer'])
    logger.info(f"killed brother. not found: {not_found}")
    osrs.move.interact_with_object(
        brother.as_dict()['staircase_id'], 'z', 0, False
    )
    osrs.player.turn_off_all_prayers()
    if not_found:
        tunnel = brother
    return tunnel


def kill_brother(brother, prayer):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([brother])
    qh.set_widgets({'229,1'})
    qh.set_interating_with()
    while True:
        qh.query_backend()
        target = qh.get_npcs(brother, interacting_with_me=True)
        if qh.get_widgets('229,1'):
            logger.info('found chat dialogue')
            return True
        if not target or target['health'] == 0:
            logger.info('killed brother')
            return

        if not target and not qh.get_interating_with():
            osrs.move.fast_click(target)

        osrs.combat_utils.prayer_handler(None, prayer)
        osrs.combat_utils.food_handler(None, 35)
        # Drink prayer pots vs karil and dharok if necessary
        if brother in [1673, 1675]:
            osrs.combat_utils.pot_handler(None, {})


def kill_brother_final(brother, prayer):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([brother])
    qh.set_widgets({'229,1'})
    qh.set_interating_with()
    while True:
        qh.query_backend()
        target = qh.get_npcs(brother, interacting_with_me=True)
        if not (3546 <= target['x_coord'] <= 3557 and 9689 <= target['y_coord'] <= 9700):
            logger.info('brother is outside of the throne room, unable to kill. exiting.')
            return
        if not target or target['health'] == 0:
            logger.info('killed brother')
            return

        if not target and not qh.get_interating_with():
            osrs.move.fast_click(target)

        osrs.combat_utils.prayer_handler(None, prayer)
        osrs.combat_utils.food_handler(None, 35)
        # Drink prayer pots vs karil and dharok if necessary
        if brother in [1673, 1675]:
            osrs.combat_utils.pot_handler(None, {})

brothers = [
    BarrowsBrother([3575, 3298, 0], 20720, 20668, 1673, ['protect_melee']),  # D
    BarrowsBrother([3565, 3289, 0], 20770, 20667, 1672, ['protect_mage']),  # A
    BarrowsBrother([3565, 3276, 0], 20771, 20670, 1675, ['protect_range']),  # K
    BarrowsBrother([3577, 3282, 0], 20722, 20669, 1674, ['protect_melee']),  # G
    BarrowsBrother([3553, 3282, 0], 20721, 20671, 1676, ['protect_melee']),  # T
    BarrowsBrother([3556, 3298, 0], 20772, 20672, 1677, ['protect_melee']),  # V
]


def kill_all_brothers():
    logger.info("Starting to kill all brothers.")
    brother_in_tunnel = None
    for brother in brothers:
        if brother.as_dict()['npc_id'] == 1672:
            logger.info("equipping ranging gear to fight ahrim.")
            osrs.player.equip_item([
                osrs.item_ids.ItemIDs.TOXIC_BLOWPIPE.value,
                osrs.item_ids.ItemIDs.AVAS_ACCUMULATOR.value,
            ])
        brother_in_tunnel = awaken_brother(brother, brother_in_tunnel)
        if brother.as_dict()['npc_id'] == 1672:
            logger.info("equiping mage gear after ahrim fight.")
            osrs.player.equip_item([
                osrs.item_ids.ItemIDs.TRIDENT_OF_THE_SWAMP.value,
                osrs.item_ids.ItemIDs.ELIDINIS_WARD.value,
                osrs.item_ids.ItemIDs.IMBUED_GUTHIX_CAPE.value,
            ])
    return brother_in_tunnel


def enter_crypt(brother: BarrowsBrother):
    logger.info("five brothers killed. entering crypt")
    osrs.move.go_to_loc(*brother.as_dict()['mound_tile'], exact_tile=True)
    enter_mound()
    osrs.move.interact_with_object(
        brother.as_dict()['crypt_id'], 'a', 1, False, right_click_option='Search',
        custom_exit_function=find_my_target, custom_exit_function_arg=brother.as_dict()['npc_id']
    )
    osrs.game.dialogue_handler(["Yeah I'm fearless!"], timeout=1)


def click_lock_pick():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(
            [osrs.item_ids.ItemIDs.STRANGE_OLD_LOCKPICK.value, osrs.item_ids.ItemIDs.STRANGE_OLD_LOCKPICK_FULL.value]
    ):
        osrs.move.fast_click(qh.get_inventory([osrs.item_ids.ItemIDs.STRANGE_OLD_LOCKPICK.value, osrs.item_ids.ItemIDs.STRANGE_OLD_LOCKPICK_FULL.value]))


def kill_tunnel_monster(x_min, x_max, y_min, y_max):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([])
    qh.set_interating_with()
    qh.set_canvas()
    start = datetime.datetime.now()
    while True:
        if (datetime.datetime.now() - start).total_seconds() > 3 and not qh.get_interating_with():
            return
        qh.query_backend()
        if qh.get_npcs():
            sorted_npcs = sorted(qh.get_npcs(), key=lambda n: n['dist'])
            for npc in sorted_npcs:
                if 'interacting' in npc and npc['interacting'].lower() == 'DJT Fan 14':
                    if npc['id'] not in tunnel_monsters_for_points or npc['health'] == 0:
                        return
                    elif (not qh.get_interating_with()
                          and x_min <= npc['x_coord'] <= x_max and y_min <= npc['y_coord'] <= y_max):
                        osrs.move.instant_click_v2(npc)
                        break


def go_to_chest(brother):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        # In Chest room
        if 3546 <= qh.get_player_world_location('x') <= 3557 and 9689 <= qh.get_player_world_location('y') <= 9700:
            osrs.player.equip_item([
                osrs.item_ids.ItemIDs.TRIDENT_OF_THE_SWAMP.value,
                osrs.item_ids.ItemIDs.ELIDINIS_WARD.value,
                osrs.item_ids.ItemIDs.OCCULT_NECKLACE.value,
            ])
            curr_time = datetime.datetime.now()
            osrs.move.interact_with_object(
                20973, 'y', 9705, False, right_click_option='Open',
                custom_exit_function=find_my_target_in_chest_room, custom_exit_function_arg=[brother.as_dict()['npc_id'], curr_time], timeout=7
            )
            return
        # Northwest
        elif 3530 <= qh.get_player_world_location('x') <= 3540 and 9707 <= qh.get_player_world_location('y') <= 9716:
            kill_tunnel_monster(3530, 3540, 9707, 9716)
            osrs.move.interact_with_object(
                20702, 'y', 9705, False, obj_type='wall',
                obj_tile={'x': 3534, 'y': 9705, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
            kill_tunnel_monster(3534, 3435, 9701, 9705)
            osrs.move.interact_with_object(
                20683, 'y', 9700, False, obj_type='wall',
                obj_tile={'x': 3534, 'y': 9701, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
        # Northeast
        elif 3563 <= qh.get_player_world_location('x') <= 3574 and 9706 <= qh.get_player_world_location(
                'y') <= 9717:
            kill_tunnel_monster(3563, 3574, 9706, 9717)
            osrs.move.interact_with_object(
                20706, 'y', 9705, False, obj_type='wall',
                obj_tile={'x': 3568, 'y': 9705, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
            kill_tunnel_monster(3568, 3569, 9701, 9705)
            osrs.move.interact_with_object(
                20687, 'y', 9700, False, obj_type='wall',
                obj_tile={'x': 3568, 'y': 9701, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
        # West
        elif 3530 <= qh.get_player_world_location('x') <= 3540 and 9689 <= qh.get_player_world_location('y') <= 9700:
            kill_tunnel_monster(3530, 3540, 9689, 9700)
            osrs.move.interact_with_object(
                20689, 'x', 3541, True, obj_type='wall',
                obj_tile={'x': 3541, 'y': 9695, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
            kill_tunnel_monster(3541, 3545, 9694, 9695)
            osrs.move.interact_with_object(
                20708, 'x', 3546, True, obj_type='wall',
                obj_tile={'x': 3545, 'y': 9695, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
        # Southeast
        elif 3563 <= qh.get_player_world_location('x') <= 3573 and 9672 <= qh.get_player_world_location('y') <= 9683:
            kill_tunnel_monster(3563, 3573, 9672, 9683)
            osrs.move.interact_with_object(
                20712, 'y', 9684, True, obj_type='wall',
                obj_tile={'x': 3569, 'y': 9684, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
            kill_tunnel_monster(3568, 3569, 9684, 9688)
            osrs.move.interact_with_object(
                20693, 'y', 9689, True, obj_type='wall',
                obj_tile={'x': 3569, 'y': 9688, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
        # East
        elif 3563 <= qh.get_player_world_location('x') <= 3573 and 9689 <= qh.get_player_world_location(
                'y') <= 9700:
            kill_tunnel_monster(3563, 3573, 9689, 9700)
            osrs.move.interact_with_object(
                20709, 'x', 3562, False, obj_type='wall',
                obj_tile={'x': 3562, 'y': 9695, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
            kill_tunnel_monster(3558, 3562, 9694, 9695)
            osrs.move.interact_with_object(
                20690, 'x', 3557, False, obj_type='wall',
                obj_tile={'x': 3558, 'y': 9695, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
        # Southwest
        elif 3529 <= qh.get_player_world_location('x') <= 3540 and 9672 <= qh.get_player_world_location(
                'y') <= 9683:
            kill_tunnel_monster(3529, 3540, 9672, 9683)
            osrs.move.interact_with_object(
                20691, 'y', 9684, True, obj_type='wall',
                obj_tile={'x': 3534, 'y': 9684, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )
            kill_tunnel_monster(3534, 3535, 9684, 9688)
            osrs.move.interact_with_object(
                20710, 'y', 9689, True, obj_type='wall',
                obj_tile={'x': 3534, 'y': 9688, 'z': 0}, pre_interact=click_lock_pick, right_click_option='Use'
            )


def loot_chest():
    osrs.move.interact_with_object(
        20973, 'y', 9705, False,
        custom_exit_function=loot_popup, timeout=3
    )


def handle_banking():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    # bank if inv is almost full, i have less than 4 sharks, no full prayer pots, or no more strange old lockpicks
    if len(qh.get_inventory()) > 24 \
        or not qh.get_inventory(osrs.item_ids.ItemIDs.PRAYER_POTION4.value) \
            or (not qh.get_inventory(osrs.item_ids.ItemIDs.STRANGE_OLD_LOCKPICK.value)
                and not qh.get_inventory(osrs.item_ids.ItemIDs.STRANGE_OLD_LOCKPICK_FULL.value)
                ) \
            or osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.ItemIDs.SHARK.value) < 4:
        osrs.game.cast_spell(varrock_tele_widget_id)
        osrs.bank.banking_handler({
            'dump_inv': True,
            'search': [{'query': 'barrows', 'items': equipment}]
        })


def main():
    while True:
        osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False
        })
        brother_in_tunnel = kill_all_brothers()
        enter_crypt(brother_in_tunnel)
        osrs.player.equip_item([
            osrs.item_ids.ItemIDs.ABYSSAL_WHIP.value,
            osrs.item_ids.ItemIDs.SALVE_AMULETEI.value,
        ])
        go_to_chest(brother_in_tunnel)
        if brother_in_tunnel.as_dict()['npc_id'] == 1672:
            osrs.player.equip_item([
                osrs.item_ids.ItemIDs.TOXIC_BLOWPIPE.value,
                osrs.item_ids.ItemIDs.AVAS_ACCUMULATOR.value,
            ])
        overhead_prayer = ['protect_range'] if brother_in_tunnel.as_dict()['npc_id'] == 1675 else ['protect_melee']
        kill_brother_final(brother_in_tunnel.as_dict()['npc_id'], overhead_prayer)
        if brother_in_tunnel.as_dict()['npc_id'] == 1672:
            osrs.player.equip_item([
                osrs.item_ids.ItemIDs.TRIDENT_OF_THE_SWAMP.value,
                osrs.item_ids.ItemIDs.ELIDINIS_WARD.value,
                osrs.item_ids.ItemIDs.IMBUED_GUTHIX_CAPE.value,
            ])
        loot_chest()
        handle_banking()
        osrs.game.tele_home()
        osrs.player.turn_off_all_prayers()
        osrs.game.click_restore_pool()
        osrs.game.use_portal_nexus('barrows')


main()
