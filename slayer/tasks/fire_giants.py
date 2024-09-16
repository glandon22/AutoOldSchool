# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'


supplies = [
    osrs.item_ids.SUPER_COMBAT_POTION4,
    osrs.item_ids.SUPER_COMBAT_POTION4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    osrs.item_ids.DRAMEN_STAFF,
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    },
]

equipment = [
    osrs.item_ids.SLAYER_HELMET_I,
    osrs.item_ids.ABYSSAL_WHIP,
    osrs.item_ids.BARROWS_GLOVES,
    osrs.item_ids.BRIMSTONE_RING,
    osrs.item_ids.DRAGON_BOOTS,
    osrs.item_ids.BANDOS_TASSETS,
    osrs.item_ids.BANDOS_CHESTPLATE,
    osrs.item_ids.AMULET_OF_FURY,
    osrs.item_ids.RUNE_DEFENDER,
    osrs.item_ids.FIRE_CAPE,
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

pot_config = slayer_killer.PotConfig(super_combat=True)


def pre_log():
    safe_tile = {
        'x': 2133,
        'y': 9329,
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
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.DRAMEN_STAFF):
                osrs.move.click(qh.get_inventory(osrs.item_ids.DRAMEN_STAFF))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.clock.random_sleep(2, 2.1)
        osrs.game.tele_home_fairy_ring('bjp')
        transport_functions.isle_of_souls_dungeon(2128, 9328)
        qh.query_backend()
        osrs.move.click(qh.get_inventory(osrs.item_ids.ABYSSAL_WHIP))
        task_started = True
        success = slayer_killer.main('fire giant', pot_config.asdict(), 35, hop=True, pre_hop=pre_log)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
