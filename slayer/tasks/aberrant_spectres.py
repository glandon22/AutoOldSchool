# 2134,9305,0
import datetime

import osrs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
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
        osrs.item_ids.KARAMJA_GLOVES_3,
        {
            'id': osrs.item_ids.NATURE_RUNE,
            'quantity': 'All'
        },
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
        {
            'id': osrs.item_ids.PRAYER_POTION4,
            'quantity': 'X',
            'amount': '12'
        },
    ]

equipment = [
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.prayer_top,
    gear_loadouts.prayer_bottom,
    gear_loadouts.melee_boots,
    gear_loadouts.melee_str_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    gear_loadouts.high_def_weapon,
    gear_loadouts.prayer_ammo_slot
]
pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def leave_catacombs():
    osrs.move.interact_with_object_v3(
        28896, 'y', 9000, greater_than=False, right_click_option='Climb-up',
        timeout=4
    )
    osrs.clock.random_sleep(10, 11)


def leave_second_floor():
    osrs.move.interact_with_object_v3(
        16538, 'z', 0, greater_than=False, right_click_option='Climb-down',
        timeout=4
    )
    osrs.player.turn_off_all_prayers()
    osrs.clock.random_sleep(11, 11.1)


def return_to_loc():
    osrs.move.go_to_loc(2470, 9779)


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
        if area in ['', None, 'Stronghold Slayer Cave']:
            transport_functions.stronghold_slayer_cave(2470, 9778)
            success = slayer_killer.main(
                'aberrant spectre', pot_config.asdict(), 35,
                pre_hop=lambda: transport_functions.run_to_safe_spot(2446, 9803),
                prayers=['protect_mage'], hop=True,  post_login=return_to_loc,
                attackable_area={'x_min': 2465, 'x_max': 2474, 'y_min': 9775, 'y_max': 9784},
            )
        elif area == 'Catacombs of Kourend':
            transport_functions.catacombs_v2(1655, 9991)
            success = slayer_killer.main(
                'deviant spectre', pot_config.asdict(), 35,
                pre_hop=leave_catacombs,
                prayers=['protect_mage'], hop=True,
                attackable_area={'x_min': 1643, 'x_max': 1660, 'y_min': 9984, 'y_max': 9995},
                post_login=lambda: osrs.move.interact_with_object_v3(
                    28919, 'y', 9000, obj_type='ground', right_click_option='Enter',
                    timeout=4
                )
            )
        elif area == 'Slayer Tower':
            transport_functions.mory_slayer_tower('aberrant spectres')
            success = slayer_killer.main(
                'aberrant spectre', pot_config.asdict(), 35,
                pre_hop=leave_second_floor,
                prayers=['protect_mage'], hop=True,
                attackable_area={'x_min': 3431, 'x_max': 3445, 'y_min': 3542, 'y_max': 3553},
                post_login=lambda: osrs.move.interact_with_object_v3(
                    16537, 'z', 1, right_click_option='Climb-up',
                    timeout=4
                )
            )

        osrs.player.turn_off_all_prayers()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


'''
3431 3445
3542 3553

'''