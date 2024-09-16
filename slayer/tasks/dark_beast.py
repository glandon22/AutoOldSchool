# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'

# for this one i dont want a slayer ring with only one charge,
# bc i tele to the cave, then to nieve after the task is done
supplies = [
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.RUNE_POUCH.value,
        ItemIDs.KARAMJA_GLOVES_4.value,
        {
            'id': ItemIDs.NATURE_RUNE.value,
            'quantity': 'All'
        },
        {
            'id': ItemIDs.PRAYER_POTION4.value,
            'quantity': '10'
        },
        ItemIDs.ETERNAL_TELEPORT_CRYSTAL.value,
    ]


equipment = [
    {'id': ItemIDs.DRAGON_DEFENDER.value, 'consume': 'Wield'},
    {'id': ItemIDs.FIRE_CAPE.value, 'consume': 'Wear'},
    {'id': ItemIDs.SLAYER_HELMET_I.value, 'consume': 'Wear'},
    {'id': ItemIDs.BARROWS_GLOVES.value, 'consume': 'Wear'},
    {'id': ItemIDs.BRIMSTONE_RING.value, 'consume': 'Wear'},
    {'id': ItemIDs.DRAGON_BOOTS.value, 'consume': 'Wear'},
    {'id': ItemIDs.PROSELYTE_CUISSE.value, 'consume': 'Wear'},
    {'id': ItemIDs.PROSELYTE_HAUBERK.value, 'consume': 'Wear'},
    {'id': ItemIDs.AMULET_OF_FURY.value, 'consume': 'Wear'},
    {'id': ItemIDs.OSMUMTENS_FANG.value, 'consume': 'Wield'},
    {'id': ItemIDs.HOLY_BLESSING.value, 'consume': 'Equip'},
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def pre_log():
    safe_tile = {
        'x': 3176,
        'y': 12420,
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
        transport_functions.iorworth_dungeon_dark_beasts()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'dark beast',
            pot_config.asdict(),
            35, pre_hop=pre_log,
            prayers=['protect_melee']
        )
        osrs.player.turn_off_all_prayers()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
