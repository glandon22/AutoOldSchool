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
        'id': osrs.item_ids.PRAYER_POTION4,
        'quantity': '10'
    },
]


lighthouse_supplies = [
    {
        'id': osrs.item_ids.DRAMEN_STAFF,
        'consume': 'Wield'
    },
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.PRAYER_POTION4,
        'quantity': '5'
    },
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
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
    transport_functions.catacombs_v2(1667, 9996)


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
        qh.query_backend()
        transport_functions.catacombs_v2(1667, 9996)
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            ['dagannoth', 'dagannoth spawn'],
            pot_config.asdict(), 35,
            pre_hop=pre_log,
            hop=True,
            post_login=post_log,
            prayers=['protect_melee']
        )
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
        qh.query_backend()


def return_to_lighthouse(qh):
    while True:
        osrs.keeb.press_key('esc')
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.DRAMEN_STAFF):
            osrs.move.fast_click_v2(qh.get_inventory(osrs.item_ids.DRAMEN_STAFF))
            break
    osrs.game.tele_home()
    osrs.game.click_restore_pool()
    transport_functions.lighthouse()
    qh.query_backend()
    osrs.move.fast_click_v2(qh.get_inventory(gear_loadouts.high_def_weapon['id'][0]))


def lighthouse():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, lighthouse_supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.lighthouse()
        qh.query_backend()
        osrs.move.fast_click_v2(qh.get_inventory(gear_loadouts.high_def_weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            ['dagannoth', 'dagannoth spawn'],
            pot_config.asdict(), 35,
            pre_hop=lambda: osrs.game.tele_home_v2(),
            post_login=lambda: return_to_lighthouse(qh),
            prayers=['protect_melee'],
            hop=True
        )
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
        qh.query_backend()
