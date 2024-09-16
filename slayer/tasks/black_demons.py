# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear
from slayer.utils import bank

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'

supplies = [
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.RUNE_POUCH,
        osrs.item_ids.KARAMJA_GLOVES_4,
        osrs.item_ids.MONKFISH,
        osrs.item_ids.MONKFISH,
        {
            'id': osrs.item_ids.NATURE_RUNE,
            'quantity': 'All'
        },
        {
            'id': osrs.item_ids.PRAYER_POTION4,
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
    {'id': osrs.item_ids.PROSELYTE_HAUBERK, 'consume': 'Wear'},
    {'id': osrs.item_ids.PROSELYTE_CUISSE, 'consume': 'Wear'},
    {'id': osrs.item_ids.AMULET_OF_FURY, 'consume': 'Wear'},
    {'id': osrs.item_ids.OSMUMTENS_FANG, 'consume': 'Wield'},
    {'id': osrs.item_ids.HOLY_BLESSING, 'consume': 'Equip'},
]

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True)


def pre_log():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'2885,9770,0'})
    qh.set_player_world_location()
    last_off_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') != 2885 \
                or qh.get_player_world_location('y') != 9770:
            last_off_tile = datetime.datetime.now()

        if qh.get_player_world_location('x') == 2885 \
                and qh.get_player_world_location('y') == 9770:
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 11:
                return
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 3:
                osrs.player.turn_off_all_prayers()
        elif qh.get_tiles('2885,9770,0') and osrs.move.is_clickable(qh.get_tiles('2885,9770,0')):
            osrs.move.fast_click(qh.get_tiles('2885,9770,0'))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2885, 'y': 9770, 'z': 0})


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        qh.query_backend()
        osrs.game.cast_spell(fally_tele_widget_id)
        transport_functions.taverley_dungeon_black_demons()
        task_started = True
        success = slayer_killer.main('black demon', pot_config.asdict(), 35, prayers=['protect_melee'], hop=True, pre_hop=pre_log)
        osrs.player.turn_off_all_prayers()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
