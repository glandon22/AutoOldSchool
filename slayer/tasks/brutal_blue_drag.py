# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from deprecated import gear

varrock_tele_widget_id = '218,23'


supplies = [
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.PRAYER_POTION4,
        'quantity': '10'
    },
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    },
]

equipment = gear.melee_dragon['equipment']

banking_config_equipment = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'slayer', 'items': equipment}]
}

banking_config_supplies = {
    'dump_inv': True,
    'dump_equipment': False,
    'search': [{'query': 'slayer', 'items': supplies}]
}

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True, antifire=True)


def loot_builder():
    config = {
        'inv': [],
        'loot': []
    }

    item = osrs.loot.LootConfig(osrs.item_ids.ADAMANT_PLATELEGS, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_LONGSWORD, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.BLUE_DHIDE_BODY, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAGON_DAGGER, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAGON_LONGSWORD, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAGON_MED_HELM, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_FULL_HELM, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_PLATEBODY, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.CHAOS_RUNE, 3, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DEATH_RUNE, 3, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.LAW_RUNE, 3, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAGON_DART_TIP, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAGON_ARROWTIPS, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNITE_ORE + 1, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAGON_JAVELIN_HEADS, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRACONIC_VISAGE, 93)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.ANCIENT_SHARD, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DARK_TOTEM_TOP, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DARK_TOTEM_BASE, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DARK_TOTEM_MIDDLE, 9)
    config['loot'].append(item)

    return config


def pre_log():
    safe_tile = {
        'x': 1638,
        'y': 10074,
        'z': 0
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
        qh.query_backend()
        print('starting function')
        if not task_started:
            success = osrs.bank.banking_handler(banking_config_equipment)
            if not success:
                print('failed to withdraw equipment.')
                return False
            osrs.clock.sleep_one_tick()
            qh.query_backend()
            for item in qh.get_inventory():
                osrs.move.click(item)
            qh.query_backend()
        success = osrs.bank.banking_handler(banking_config_supplies)
        if not success:
            print('failed to withdraw supplies.')
            return False
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.catacombs_v2(1638, 10074)
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'brutal blue dragon', pot_config.asdict(), 35,
            hop=True, pre_hop=pre_log, loot_config=loot_builder(), prayers=['protect_mage']
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
