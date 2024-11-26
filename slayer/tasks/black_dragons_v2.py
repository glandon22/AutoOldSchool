
# run to 2865,9827,1
# then exit
# 2134,9305,0
import datetime

import osrs
import osrs.move

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.transport_functions import taverley
from slayer.utils import bank

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'


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
    gear_loadouts.dragon_melee_weapon,
    gear_loadouts.prayer_ammo_slot
]

supplies = [
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    },
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
        'x': 2868,
        'y': 9827,
        'z': 1
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
        osrs.clock.sleep_one_tick()
        osrs.game.cast_spell(fally_tele_widget_id)
        transport_functions.taverley('black dragons')
        task_started = True
        success = slayer_killer.main(
            'baby black dragon', pot_config.asdict(), 35, hop=True, pre_hop=pre_log
        )
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


def myths():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    m_supps = [osrs.item_ids.MYTHICAL_CAPE_22114] + list(filter(lambda supp: type(supp) is int or supp['id'] != osrs.item_ids.DRAMEN_STAFF, supplies))
    while True:
        bank(qh, task_started, equipment, m_supps)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.myths_guild('black dragons')
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            ['black dragon'], slayer_killer.PotConfig(super_atk=True, super_str=True, antifire=True).asdict(), 35,
            pre_hop=lambda: transport_functions.tele_to_myths(),
            post_login=lambda: transport_functions.myths_guild('black dragons'), hop=True,
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
