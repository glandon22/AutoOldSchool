# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'


supplies = [
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_3.value,
    {
        'id': ItemIDs.NATURE_RUNE.value,
        'quantity': 'All'
    },
    {
        'id': ItemIDs.PRAYER_POTION4.value,
        'quantity': '5'
    },
{
        'id': ItemIDs.MONKFISH.value,
        'quantity': '10'
    },
]

equipment = [
    ItemIDs.HOLY_BLESSING.value,
    ItemIDs.SLAYER_HELMET_I.value,
    ItemIDs.ZOMBIE_AXE.value,
    ItemIDs.BARROWS_GLOVES.value,
    ItemIDs.BRIMSTONE_RING.value,
    ItemIDs.DRAGON_BOOTS.value,
    {
        'id': [
            ItemIDs.KARILS_LEATHERTOP.value,
            ItemIDs.KARILS_LEATHERTOP_25.value,
            ItemIDs.KARILS_LEATHERTOP_50.value,
            ItemIDs.KARILS_LEATHERTOP_75.value,
            ItemIDs.KARILS_LEATHERTOP_100.value,
        ],
        'quantity': 1
    },
    {
        'id': [
            ItemIDs.KARILS_LEATHERSKIRT.value,
            ItemIDs.KARILS_LEATHERSKIRT_25.value,
            ItemIDs.KARILS_LEATHERSKIRT_50.value,
            ItemIDs.KARILS_LEATHERSKIRT_75.value,
            ItemIDs.KARILS_LEATHERSKIRT_100.value,
        ],
        'quantity': 1
    },
    ItemIDs.AMULET_OF_FURY.value,
    ItemIDs.RUNE_DEFENDER.value,
    ItemIDs.FIRE_CAPE.value,
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
            if qh.get_inventory(ItemIDs.DRAMEN_STAFF.value):
                osrs.move.click(qh.get_inventory(ItemIDs.DRAMEN_STAFF.value))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('akq')
        transport_functions.kraken_cove_waterfiends()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.ZOMBIE_AXE.value))
        task_started = True
        success = slayer_killer.main('waterfiend', pot_config.asdict(), 35, pre_hop=pre_log, prayers=['protect_range'])
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

'''
1633, 10054
'''