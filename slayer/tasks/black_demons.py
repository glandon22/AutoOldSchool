# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'

supplies = [
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.RUNE_POUCH,
        osrs.item_ids.KARAMJA_GLOVES_3,
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
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.prayer_top,
    gear_loadouts.prayer_bottom,
    gear_loadouts.melee_boots,
    gear_loadouts.melee_str_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    gear_loadouts.high_def_weapon,
    gear_loadouts.prayer_ammo_slot
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
