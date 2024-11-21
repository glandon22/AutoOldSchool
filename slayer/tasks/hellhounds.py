# 2134,9305,0
import datetime

import osrs
from osrs.widget_ids import kourend_telly_spell_widget_id

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'

supplies = [
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    }
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


def pre_log():
    transport_functions.run_to_safe_spot(2848, 9832)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        qh.query_backend()
        osrs.game.cast_spell(fally_tele_widget_id)
        transport_functions.taverley_dungeon_hellhounds()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main('hellhound', pot_config.asdict(), 35, hop=True, pre_hop=pre_log)
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def return_to_catacombs():
    osrs.game.tele_home()
    osrs.game.click_restore_pool()
    transport_functions.catacombs_v2(1644, 10067)


def catacombs():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.catacombs_v2(1644, 10067)
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'hellhound', pot_config.asdict(), 35,
            pre_hop=lambda: osrs.game.tele_home_v2(), post_login=return_to_catacombs
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def stronghold():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.stronghold_slayer_cave(2431, 9772)
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'hellhound', pot_config.asdict(), 35,
            pre_hop=lambda: transport_functions.run_to_safe_spot(2419, 9784),
            post_login=lambda: osrs.move.go_to_loc(2431, 9772),
            attackable_area={'x_min': 2423, 'x_max': 2436, 'y_min': 9767, 'y_max': 9778}
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
