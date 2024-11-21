# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.transport_functions import travel_to_priff
from slayer.utils import bank


varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'

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
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'X',
        'amount': '17'
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
    gear_loadouts.leaf_weapon,
    gear_loadouts.prayer_ammo_slot
]


pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def loot_builder():
    config = {
        'inv': [],
        'loot': []
    }

    item = osrs.loot.InvConfig(osrs.item_ids.MONKFISH, osrs.loot.monkfish_eval)
    config['inv'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_LONGSWORD, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.ADAMANT_PLATEBODY, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_AXE, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.LEAFBLADED_SWORD, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.MYSTIC_ROBE_TOP_LIGHT, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.LEAFBLADED_BATTLEAXE, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.NATURE_RUNE, 6, min_quantity=15)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.SNAPDRAGON_SEED, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.SNAPE_GRASS_SEED, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.COINS_995, 8, min_quantity=1000)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.PAPAYA_FRUIT + 1, 8)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.COCONUT + 1, 8)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.KURASK_HEAD, 8)
    config['loot'].append(item)

    return config


def main(loc=None):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    safe_tiles = []
    attackable_area={}
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        qh.query_backend()
        if loc is None or loc == "Fremennik Slayer Dungeon":
            transport_functions.frem_dungeon('kurask')
            safe_tiles = [2710, 9993]
            attackable_area = {'x_min': 2690, 'x_max': 2708, 'y_min': 9990, 'y_max': 10007}
        elif loc == 'Iorwerth Dungeon':
            transport_functions.travel_to_priff()
            transport_functions.iorworth_dungeon(3220, 12366)
            safe_tiles = [3234, 12373]
            attackable_area = {'x_min': 3203, 'x_max': 3236, 'y_min': 12354, 'y_max': 12379}

        task_started = True
        success = slayer_killer.main(
            'kurask', pot_config.asdict(), 35,
            pre_hop=lambda: transport_functions.run_to_safe_spot(*safe_tiles), loot_config=loot_builder(),
            max_players=3, hop=True, attackable_area=attackable_area
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
