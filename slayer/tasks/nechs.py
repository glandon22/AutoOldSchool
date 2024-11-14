# 2134,9305,0
import datetime

import osrs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank

varrock_tele_widget_id = '218,23'

supplies = [
    {
        'id': [
            osrs.item_ids.NATURE_RUNE
        ],
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
            osrs.item_ids.SLAYER_RING_1,
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
    osrs.item_ids.MONKFISH,
    osrs.item_ids.MONKFISH,
    {
        'id': osrs.item_ids.PRAYER_POTION4,
        'quantity': 'X',
        'amount': '8'
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
    gear_loadouts.high_def_weapon,
    gear_loadouts.prayer_ammo_slot
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def loot_builder():
    config = {
        'inv': [],
        'loot': []
    }

    item = osrs.loot.LootConfig(osrs.item_ids.ADAMANT_PLATELEGS, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_FULL_HELM, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_2H_SWORD, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_BOOTS, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.CHAOS_RUNE, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.LAW_RUNE, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.BLOOD_RUNE, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.SNAPDRAGON_SEED, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.SNAPE_GRASS_SEED, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DEATH_RUNE, 3, min_quantity=10)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.COINS_995, 3, min_quantity=1000)
    config['loot'].append(item)
    return config


def pre_log():
    safe_tile = {
        'x': 3428,
        'y': 9940,
        'z': 3
    }
    safe_tile_string = f'{safe_tile["x"]},{safe_tile["y"]},{safe_tile["z"]}'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({safe_tile_string})
    qh.set_player_world_location()
    last_off_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') != safe_tile["x"] \
                or qh.get_player_world_location('y') != safe_tile["y"]:
            last_off_tile = datetime.datetime.now()

        if qh.get_player_world_location('x') == safe_tile["x"] \
                and qh.get_player_world_location('y') == safe_tile["y"]:
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 11:
                return
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 3:
                osrs.player.turn_off_all_prayers()
        elif qh.get_tiles(safe_tile_string):
            osrs.move.fast_click(qh.get_tiles(safe_tile_string))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), safe_tile)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.morytania_nechs()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'nechryael', pot_config.asdict(), 35,
            pre_hop=pre_log, prayers=['protect_melee'], loot_config=loot_builder(),
            attackable_area={'x_min': 3403, 'x_max': 3422, 'y_min': 9948, 'y_max': 9973},
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
