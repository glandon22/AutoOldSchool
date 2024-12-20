# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from slayer.tasks import gear_loadouts
from slayer.utils import bank
from combat import slayer_killer

varrock_tele_widget_id = '218,23'

supplies = [
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    {
        'id': [
            osrs.item_ids.RING_OF_DUELING1,
            osrs.item_ids.RING_OF_DUELING2,
            osrs.item_ids.RING_OF_DUELING3,
            osrs.item_ids.RING_OF_DUELING4,
            osrs.item_ids.RING_OF_DUELING5,
            osrs.item_ids.RING_OF_DUELING6,
            osrs.item_ids.RING_OF_DUELING7,
            osrs.item_ids.RING_OF_DUELING8
        ],
        'quantity': '1'
    },
    osrs.item_ids.RUNE_POUCH,
    {
        'id': [
            osrs.item_ids.NATURE_RUNE
        ],
        'quantity': 'All'
    },
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': [
            osrs.item_ids.PRAYER_POTION4,
            osrs.item_ids.PRAYER_POTION3,
            osrs.item_ids.PRAYER_POTION2,
            osrs.item_ids.PRAYER_POTION1,
        ],
        'quantity': '10'
    },
    {
        'id': [
            osrs.item_ids.PRAYER_POTION4,
            osrs.item_ids.PRAYER_POTION3,
            osrs.item_ids.PRAYER_POTION2,
            osrs.item_ids.PRAYER_POTION1,
        ],
        'quantity': '5'
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


def pre_log():
    osrs.player.turn_off_all_prayers()
    osrs.clock.random_sleep(11, 12)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.transport.dueling_to_c_wars()
        osrs.transport.walk_out_of_c_wars()
        osrs.move.go_to_loc(2414, 3060)
        osrs.move.interact_with_object(30176, 'y', 5500, True)
        osrs.move.go_to_loc(2406, 9452, right_click=True)
        task_started = True
        success = slayer_killer.main(
            ['smoke devil'], pot_config.asdict(), 35, hop=True,
            pre_hop=pre_log, prayers=['protect_range']
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

'''
run to 2406,9452, 0




'''