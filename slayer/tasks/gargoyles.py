# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'

# for this one i dont want a slayer ring with only one charge,
# bc i tele to the cave, then to nieve after the task is done
supplies = [
    {
        'id': [
            ItemIDs.NATURE_RUNE.value
        ],
        'quantity': 'All'
    },
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_3.value,
    {
        'id': [
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
    ItemIDs.ROCK_HAMMER.value,
    {
        'id': ItemIDs.PRAYER_POTION4.value,
        'quantity': 'X',
        'amount': '12'
    }
]

equipment = [
        ItemIDs.ZOMBIE_AXE.value,
        ItemIDs.HOLY_BLESSING.value,
        ItemIDs.RUNE_DEFENDER.value,
        ItemIDs.BARROWS_GLOVES.value,
        ItemIDs.FIRE_CAPE.value,
        ItemIDs.SLAYER_HELMET_I.value,
        ItemIDs.BRIMSTONE_RING.value,
        ItemIDs.DRAGON_BOOTS.value,
        ItemIDs.BANDOS_CHESTPLATE.value,
        ItemIDs.BANDOS_TASSETS.value,
        ItemIDs.AMULET_OF_FURY.value,
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

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True)


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
        transport_functions.morytania_gargoyles()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'gargoyle', pot_config.asdict(), 35, pre_hop=pre_log, prayers=['protect_melee']
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

