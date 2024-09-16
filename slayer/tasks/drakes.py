# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'


supplies = [
    osrs.item_ids.DRAMEN_STAFF,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': '10'
    },
    {
        'id': osrs.item_ids.PRAYER_POTION4,
        'quantity': '5'
    },
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'X',
        'amount': 50
    },
]

equipment = [
    osrs.item_ids.DRAGONFIRE_SHIELD,
    osrs.item_ids.BARROWS_GLOVES,
    osrs.item_ids.FIRE_CAPE,
    osrs.item_ids.SLAYER_HELMET_I,
    osrs.item_ids.BRIMSTONE_RING,
    osrs.item_ids.BOOTS_OF_BRIMSTONE,
    osrs.item_ids.BANDOS_CHESTPLATE,
    osrs.item_ids.BANDOS_TASSETS,
    osrs.item_ids.AMULET_OF_FURY,
    osrs.item_ids.DRAGON_HUNTER_LANCE,
    osrs.item_ids.HOLY_BLESSING,
]

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


def pre_log():
    safe_tile = {
        'x': 1316,
        'y': 10218,
        'z': 1
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


def loot_builder():
    config = {
        'inv': [],
        'loot': []
    }

    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_FULL_HELM, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RED_DHIDE_BODY, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.MYSTIC_EARTH_STAFF, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAGON_MACE, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNE_BATTLEAXE, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.RUNITE_LIMBS, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAKES_TOOTH, 999)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAKES_CLAW, 999)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAGON_THROWNAXE, 999)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DRAGON_KNIFE, 999)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.NATURE_RUNE, 7, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.LAW_RUNE, 7, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DEATH_RUNE, 7, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.COINS_995, 7, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DIAMOND + 1, 7, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.GRIMY_RANARR_WEED + 1, 7, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.GRIMY_SNAPDRAGON + 1, 7, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.GRIMY_TORSTOL + 1, 7, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.SNAPDRAGON_SEED, 7, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.SNAPE_GRASS_SEED, 7, stackable=True)
    config['loot'].append(item)

    return config


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
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.DRAMEN_STAFF):
                osrs.move.click(qh.get_inventory(osrs.item_ids.DRAMEN_STAFF))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('cir')
        transport_functions.mount_karuulm_drakes()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(osrs.item_ids.DRAGON_HUNTER_LANCE))
        task_started = True
        success = slayer_killer.main('drake', pot_config.asdict(), 35, prayers=['protect_range'], pre_hop=pre_log, loot_config=loot_builder())
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
