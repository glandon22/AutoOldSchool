# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank

varrock_tele_widget_id = '218,23'

weapon = gear_loadouts.dragon_melee_weapon
supplies = [
    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': '5'
    },
    {
        'id': osrs.item_ids.PRAYER_POTION4,
        'quantity': '10'
    },
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'X',
        'amount': 50
    },
]

equipment = [
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.melee_str_chest,
    gear_loadouts.melee_str_legs,
    gear_loadouts.melee_boots,
    gear_loadouts.dragon_melee_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    weapon,
    gear_loadouts.prayer_ammo_slot
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True, antifire=True)


def pre_log():
    safe_tile = {
        'x': 2140,
        'y': 9298,
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


def return_to_dragons():
    osrs.game.tele_home()
    osrs.game.click_restore_pool()
    while True:
        qh = osrs.qh_v2.qh()
        qh.set_inventory()
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.DRAMEN_STAFF):
            osrs.move.fast_click_v2(qh.get_inventory(osrs.item_ids.DRAMEN_STAFF))
            break
    osrs.game.tele_home_fairy_ring('ckr')
    transport_functions.brimhaven_dungeon_dragons(2681, 9461)


def brimhaven():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('ckr')
        transport_functions.brimhaven_dungeon_dragons(2637, 9458)
        qh.query_backend()
        osrs.move.click(qh.get_inventory(weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            'bronze dragon', pot_config.asdict(), 35, prayers=['protect_melee'],
            pre_hop=lambda: osrs.game.cast_spell(varrock_tele_widget_id), post_login=return_to_dragons
        )

        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
