# 2134,9305,0
import datetime

import osrs

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
        osrs.item_ids.MONKFISH,
        osrs.item_ids.MONKFISH,
        {
            'id': osrs.item_ids.NATURE_RUNE,
            'quantity': 'All'
        },
        {
            'id': osrs.item_ids.PRAYER_POTION4,
            'quantity': '10'
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

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        task_started = True
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        qh.query_backend()
        osrs.game.cast_spell(fally_tele_widget_id)
        osrs.move.go_to_loc(2945, 3370)
        transport_functions.taverley('black demons')
        success = slayer_killer.main(
            'black demon', pot_config.asdict(), 35,
            prayers=['protect_melee'], hop=True, pre_hop=lambda: transport_functions.run_to_safe_spot(2885, 9770)
        )
        osrs.player.turn_off_all_prayers()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def brim():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, [{'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'}] + supplies)
        task_started = True
        osrs.game.tele_home_v2()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('ckr')
        transport_functions.brimhaven_dungeon_south('black demons')
        qh.query_backend()
        osrs.move.fast_click_v2(qh.get_inventory(gear_loadouts.high_def_weapon['id'][0]))
        success = slayer_killer.main(
            'black demon', pot_config.asdict(), 35,
            prayers=['protect_melee'], hop=True, pre_hop=lambda: transport_functions.run_to_safe_spot(2696, 9492),
            attackable_area={'x_min': 2694, 'x_max': 2708, 'y_min': 9475, 'y_max': 9493},
        )
        osrs.player.turn_off_all_prayers()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def chasm():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, [{'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'}] + supplies)
        task_started = True
        osrs.game.tele_home_v2()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('djr')
        transport_functions.chasm_of_fire('black demons')
        qh.query_backend()
        osrs.move.fast_click_v2(qh.get_inventory(gear_loadouts.high_def_weapon['id'][0]))
        success = slayer_killer.main(
            'black demon', pot_config.asdict(), 35,
            prayers=['protect_melee'], pre_hop=lambda: osrs.game.tele_home_v2(),
            post_login=lambda: transport_functions.fairy_ring_back_slay_area(
                qh, transport_functions.chasm_of_fire, gear_loadouts.high_def_weapon['id'][0],
                'djr', fn_arg='black demons'
            )
        )
        osrs.player.turn_off_all_prayers()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
