# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'

supplies = [
    {
        'id': [
            ItemIDs.NATURE_RUNE.value
        ],
        'quantity': 'All'
    },
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_4.value,
    {
        'id': [
            ItemIDs.SLAYER_RING_1.value,
            ItemIDs.SLAYER_RING_2.value,
            ItemIDs.SLAYER_RING_3.value,
            ItemIDs.SLAYER_RING_4.value,
            ItemIDs.SLAYER_RING_5.value,
            ItemIDs.SLAYER_RING_6.value,
            ItemIDs.SLAYER_RING_7.value,
            ItemIDs.SLAYER_RING_8.value,
        ],
        'quantity': '1'
    },
    ItemIDs.MONKFISH.value,
    ItemIDs.MONKFISH.value,
    {
        'id': ItemIDs.PRAYER_POTION4.value,
        'quantity': 'X',
        'amount': '8'
    }
]

equipment = [
    {'id': ItemIDs.DRAGON_DEFENDER.value, 'consume': 'Wield'},
    {'id': ItemIDs.FIRE_CAPE.value, 'consume': 'Wear'},
    {'id': ItemIDs.SLAYER_HELMET_I.value, 'consume': 'Wear'},
    {'id': ItemIDs.BARROWS_GLOVES.value, 'consume': 'Wear'},
    {'id': ItemIDs.BRIMSTONE_RING.value, 'consume': 'Wear'},
    {'id': ItemIDs.DRAGON_BOOTS.value, 'consume': 'Wear'},
    {'id': ItemIDs.BANDOS_CHESTPLATE.value, 'consume': 'Wear'},
    {'id': ItemIDs.BANDOS_TASSETS.value, 'consume': 'Wear'},
    {'id': ItemIDs.AMULET_OF_FURY.value, 'consume': 'Wear'},
    {'id': ItemIDs.OSMUMTENS_FANG.value, 'consume': 'Wield'},
    {'id': ItemIDs.HOLY_BLESSING.value, 'consume': 'Equip'},
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def loot_builder():
    config = {
        'inv': [],
        'loot': []
    }

    item = osrs.loot.LootConfig(ItemIDs.ADAMANT_PLATELEGS.value, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNE_FULL_HELM.value, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNE_2H_SWORD.value, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNE_BOOTS.value, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.CHAOS_RUNE.value, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.LAW_RUNE.value, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.BLOOD_RUNE.value, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.SNAPDRAGON_SEED.value, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.SNAPE_GRASS_SEED.value, 3)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DEATH_RUNE.value, 3, min_quantity=10)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.COINS_995.value, 3, min_quantity=1000)
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
