# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank
varrock_tele_widget_id = '218,23'


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
    gear_loadouts.dragon_melee_weapon,
    gear_loadouts.prayer_ammo_slot
]

supplies = [
    {
        'id': osrs.item_ids.DRAMEN_STAFF,
        'consume': 'Wield'
    },
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    }
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        qh.query_backend()
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('aiq')
        transport_functions.skeletal_wyverns()
        qh.query_backend()
        osrs.move.fast_click_v2(qh.get_inventory(gear_loadouts.dragon_melee_weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            'skeletal wyvern', pot_config.asdict(), 35, prayers=['protect_melee'],
            pre_hop=lambda: osrs.move.interact_with_object_v3(53250, 'x', 3014),
            post_login=lambda: osrs.move.interact_with_object_v3(
                53251, 'x', 3024, greater_than=False
            ),
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
