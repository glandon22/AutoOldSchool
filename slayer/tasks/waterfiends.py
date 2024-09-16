# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'


supplies = [
    osrs.item_ids.DRAMEN_STAFF,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.PRAYER_POTION4,
        'quantity': '5'
    },
{
        'id': osrs.item_ids.MONKFISH,
        'quantity': '10'
    },
]

equipment = [
    osrs.item_ids.HOLY_BLESSING,
    osrs.item_ids.SLAYER_HELMET_I,
    osrs.item_ids.ZOMBIE_AXE,
    osrs.item_ids.BARROWS_GLOVES,
    osrs.item_ids.BRIMSTONE_RING,
    osrs.item_ids.DRAGON_BOOTS,
    {
        'id': [
            osrs.item_ids.KARILS_LEATHERTOP,
            osrs.item_ids.KARILS_LEATHERTOP_25,
            osrs.item_ids.KARILS_LEATHERTOP_50,
            osrs.item_ids.KARILS_LEATHERTOP_75,
            osrs.item_ids.KARILS_LEATHERTOP_100,
        ],
        'quantity': 1
    },
    {
        'id': [
            osrs.item_ids.KARILS_LEATHERSKIRT,
            osrs.item_ids.KARILS_LEATHERSKIRT_25,
            osrs.item_ids.KARILS_LEATHERSKIRT_50,
            osrs.item_ids.KARILS_LEATHERSKIRT_75,
            osrs.item_ids.KARILS_LEATHERSKIRT_100,
        ],
        'quantity': 1
    },
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

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def pre_log():
    safe_tile = {
        'x': 2288,
        'y': 9993,
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
        osrs.game.tele_home_fairy_ring('akq')
        transport_functions.kraken_cove_waterfiends()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(osrs.item_ids.ZOMBIE_AXE))
        task_started = True
        success = slayer_killer.main('waterfiend', pot_config.asdict(), 35, pre_hop=pre_log, prayers=['protect_range'])
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

'''
1633, 10054
'''