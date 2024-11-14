# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank

varrock_tele_widget_id = '218,23'


supplies = [
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
        'quantity': '10'
    },
]

equipment = [
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.melee_str_chest,
    gear_loadouts.melee_str_legs,
    gear_loadouts.melee_boots,
    gear_loadouts.melee_str_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    gear_loadouts.high_def_weapon,
    gear_loadouts.prayer_ammo_slot
]


pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def pre_log():
    osrs.player.turn_off_all_prayers()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    last_tele_cast = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 1623 <= qh.get_player_world_location('x') <= 1656 and 3664 <= qh.get_player_world_location('y') <= 3684:
            break
        elif (datetime.datetime.now() - last_tele_cast).total_seconds() > 10:
            osrs.game.cast_spell('218,36')
            last_tele_cast = datetime.datetime.now()
    osrs.clock.random_sleep(10, 11)


def post_log():
    transport_functions.catacombs(1633, 10054)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.catacombs(1633, 10066)
        qh.query_backend()
        task_started = True
        success = slayer_killer.main('fire giant', pot_config.asdict(), 35, pre_hop=pre_log, post_login=post_log, prayers=['protect_melee'])
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

'''
1633, 10054
'''