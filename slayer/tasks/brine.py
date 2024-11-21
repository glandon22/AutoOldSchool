# 2134,9305,0
import datetime

import osrs
from slayer.tasks import gear_loadouts
from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'

# for this one i dont want a slayer ring with only one charge,
# bc i tele to the cave, then to nieve after the task is done
supplies = [
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    {
        'id': osrs.item_ids.DRAMEN_STAFF,
        'consume': 'Wield'
    },
    osrs.item_ids.KARAMJA_GLOVES_3,
    osrs.item_ids.SPADE,
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': '10'
    },
    osrs.item_ids.MONKFISH,
    osrs.item_ids.MONKFISH,
    osrs.item_ids.MONKFISH,
]

equipment = [
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.melee_str_chest,
    gear_loadouts.melee_str_legs,
    gear_loadouts.melee_boots,
    gear_loadouts.melee_str_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    gear_loadouts.low_def_weapon,
    gear_loadouts.prayer_ammo_slot
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('dks')
        transport_functions.brine_cavern()
        qh.query_backend()
        osrs.move.fast_click_v2(qh.get_inventory(gear_loadouts.low_def_weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            'brine rat', pot_config.asdict(), 35, hop=True
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
