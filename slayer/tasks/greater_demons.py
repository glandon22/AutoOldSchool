# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer

from slayer.tasks import gear_loadouts
from slayer.utils import bank

varrock_tele_widget_id = '218,23'
weapon = gear_loadouts.high_def_weapon
supplies = [
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'All'
    },
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': [
            osrs.item_ids.DRAMEN_STAFF
        ],
        'consume': 'Wield'
    },
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
    weapon,
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
        osrs.game.tele_home_fairy_ring('bjp')
        transport_functions.isle_of_souls_dungeon_v2(2166, 9331)
        qh.query_backend()
        osrs.move.click(qh.get_inventory(weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            'greater demon', pot_config.asdict(), 35, hop=True,
            pre_hop=lambda: transport_functions.run_to_safe_spot(2156, 9322)
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def brim():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('ckr')
        transport_functions.brimhaven_dungeon_south('greater demons')
        qh.query_backend()
        osrs.move.click(qh.get_inventory(weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            'greater demon', pot_config.asdict(), 35, hop=True,
            pre_hop=lambda: transport_functions.run_to_safe_spot(2654, 9476, 2),
            post_login=lambda: osrs.move.go_to_loc(2633, 9490, 2)
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def chasm():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('djr')
        transport_functions.chasm_of_fire('greater demons')
        qh.query_backend()
        osrs.move.click(qh.get_inventory(weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            'greater demon', pot_config.asdict(), 35, hop=True,
            pre_hop=lambda: transport_functions.run_to_safe_spot(1453, 10098, 2)
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def karuulm():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('cir')
        transport_functions.mount_karuulm('greater demons')
        qh.query_backend()
        osrs.move.click(qh.get_inventory(weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            'greater demon', pot_config.asdict(), 35, hop=True,
            pre_hop=lambda: transport_functions.run_to_safe_spot(1300, 10213, 1),
            post_login=lambda: osrs.move.go_to_loc(1281, 10208, 1)
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
