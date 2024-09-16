import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'

supplies = [
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_4,
    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    },
]

equipment = [
    {'id': osrs.item_ids.DRAGON_DEFENDER, 'consume': 'Wield'},
    {'id': osrs.item_ids.FIRE_CAPE, 'consume': 'Wear'},
    {'id': osrs.item_ids.SLAYER_HELMET_I, 'consume': 'Wear'},
    {'id': osrs.item_ids.BARROWS_GLOVES, 'consume': 'Wear'},
    {'id': osrs.item_ids.BRIMSTONE_RING, 'consume': 'Wear'},
    {'id': osrs.item_ids.DRAGON_BOOTS, 'consume': 'Wear'},
    {'id': osrs.item_ids.BANDOS_CHESTPLATE, 'consume': 'Wear'},
    {'id': osrs.item_ids.BANDOS_TASSETS, 'consume': 'Wear'},
    {'id': osrs.item_ids.AMULET_OF_FURY, 'consume': 'Wear'},
    {'id': osrs.item_ids.ABYSSAL_WHIP},
    {'id': osrs.item_ids.HOLY_BLESSING, 'consume': 'Equip'},
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def pre_log():
    safe_tile = {
        'x': 1227,
        'y': 3480,
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
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('bls')
        transport_functions.south_quidamortem_trolls()
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.ABYSSAL_WHIP):
                osrs.move.click(qh.get_inventory(osrs.item_ids.ABYSSAL_WHIP))
                break
        task_started = True
        success = slayer_killer.main('mountain troll', pot_config.asdict(), 35, hop=True, pre_hop=pre_log)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
