# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank
varrock_tele_widget_id = '218,23'

weapon = gear_loadouts.dragon_melee_weapon
equipment = [
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.melee_str_chest,
    gear_loadouts.melee_str_legs,
    gear_loadouts.melee_boots,
    gear_loadouts.dragon_melee_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    weapon,
    gear_loadouts.prayer_ammo_slot
]

supplies = [
    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    },
]

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True, antifire=True)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('bjp')
        transport_functions.isle_of_souls_dungeon_v2(2134, 9305)
        qh.query_backend()
        osrs.move.click(qh.get_inventory(weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            ['blue dragon', 'baby blue dragon'], pot_config.asdict(), 35,
            hop=True, pre_hop=lambda: transport_functions.run_to_safe_spot(2136, 9307)
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def myths():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    m_supps = [osrs.item_ids.MYTHICAL_CAPE_22114] + list(filter(lambda supp: type(supp) is int or supp['id'] != osrs.item_ids.DRAMEN_STAFF, supplies))
    while True:
        bank(qh, task_started, equipment, m_supps)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.myths_guild('blue dragons')
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            ['blue dragon'], pot_config.asdict(), 35,
            pre_hop=lambda: transport_functions.tele_to_myths(),
            post_login=lambda: transport_functions.myths_guild('blue dragons'),
            hop=True
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def taverley():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    t_supps = list(filter(lambda supp: type(supp) is int or supp['id'] != osrs.item_ids.DRAMEN_STAFF, supplies))
    task_started = False
    while True:
        bank(qh, task_started, equipment, t_supps)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.cast_spell(osrs.widget_ids.fally_tele_widget_id)
        transport_functions.taverley('blue dragons')
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            ['blue dragon'], pot_config.asdict(), 35,
            pre_hop=lambda: osrs.move.interact_with_object_v3(
                16509, coord_type='x', coord_value=2889, greater_than=False
            ),
            post_login=lambda: osrs.move.interact_with_object_v3(
                16509, coord_type='x', coord_value=2888, greater_than=True
            )
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
