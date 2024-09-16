# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'


supplies = [
    ItemIDs.MOONCLAN_TELEPORT.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_4.value,
    {
        'id': ItemIDs.MONKFISH.value,
        'quantity': 'All'
    },
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

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True)


def pre_log():
    safe_tile = {
        'x': 2102,
        'y': 3852,
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
        qh.query_backend()
        tab = qh.get_inventory(ItemIDs.MOONCLAN_TELEPORT.value)
        if not tab:
            exit('missing tele tab')
        osrs.move.click(tab)
        transport_functions.run_to_suqahs()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'suqah',
            pot_config.asdict(), 35,
            attackable_area={'x_min': 2090, 'x_max': 2111, 'y_min': 3847, 'y_max': 3878},
            hop=True,
            pre_hop=pre_log
        )
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
        qh.query_backend()
