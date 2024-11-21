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
            'id': [
                osrs.item_ids.SLAYER_RING_2,
                osrs.item_ids.SLAYER_RING_3,
                osrs.item_ids.SLAYER_RING_4,
                osrs.item_ids.SLAYER_RING_5,
                osrs.item_ids.SLAYER_RING_6,
                osrs.item_ids.SLAYER_RING_7,
                osrs.item_ids.SLAYER_RING_8,
            ],
            'quantity': '1'
        },
        osrs.item_ids.KARAMJA_GLOVES_3,
        {
            'id': osrs.item_ids.MONKFISH,
            'quantity': 'All'
        },
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
    gear_loadouts.high_def_weapon,
    gear_loadouts.prayer_ammo_slot
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def leave_catabcombs():
    osrs.move.go_to_loc(1658, 9987)
    osrs.move.interact_with_object_v3(
        28896, 'y', 9000, greater_than=False, right_click_option='Climb-up',
        timeout=4
    )
    osrs.player.turn_off_all_prayers()
    osrs.clock.random_sleep(11, 11.1)


def return_to_catacombs():
    osrs.move.interact_with_object_v3(
        28919, 'y', 9000, obj_type='ground', right_click_option='Enter',
        timeout=4
    )
    osrs.move.go_to_loc(1639, 9993)


def main(area=None):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        qh.query_backend()
        task_started = True
        success = None
        if area in ['Stronghold Slayer Dungeon', None, '']:
            transport_functions.stronghold_slayer_cave(2478, 9800)
            success = slayer_killer.main(
                'ankou', pot_config.asdict(), 35, hop=True,
                pre_hop=lambda: transport_functions.run_to_safe_spot(2471, 9813),
                attackable_area={'x_min': 2470, 'x_max': 2479, 'y_min': 9806, 'y_max': 9810}
            )
        elif area == 'Catacombs of Kourend':
            transport_functions.catacombs_v2(1688, 10047)
            osrs.move.go_to_loc(1688, 9998)
            osrs.move.go_to_loc(1640, 9998)
            success = slayer_killer.main(
                'ankou', pot_config.asdict(), 35, hop=True,
                pre_hop=leave_catabcombs, post_login=return_to_catacombs,
                attackable_area={'x_min': 1635, 'x_max': 1644, 'y_min': 9990, 'y_max': 9998}
            )

        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

