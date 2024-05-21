# 2134,9305,0
import datetime

import osrs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear


varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'

supplies = gear.slayer_leafbladed_melee['supplies']

equipment = gear.slayer_leafbladed_melee['equipment']

banking_config_equipment = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'slayer', 'items': equipment}]
}

banking_config_supplies = {
    'dump_inv': True,
    'dump_equipment': False,
    'search': [{'query': 'slayer', 'items': [osrs.item_ids.ItemIDs.DRAMEN_STAFF.value, *supplies]}]
}

pot_config = slayer_killer.PotConfig(super_combat=True)


def pre_log():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'2708,9992,0'})
    qh.set_player_world_location()
    last_off_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') != 2708 \
                or qh.get_player_world_location('y') != '9992':
            last_off_tile = datetime.datetime.now()

        if qh.get_player_world_location('x') == 2708 \
                and qh.get_player_world_location('y') == '9992' \
                and (datetime.datetime.now() - last_off_tile).total_seconds() > 11:
            osrs.player.turn_off_all_prayers()
            return
        elif qh.get_tiles('2708,9992,0'):
            osrs.move.fast_click(qh.get_tiles('2708,9992,0'))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2708, 'y': 9992, 'z': 0})


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
            if qh.get_inventory(osrs.item_ids.ItemIDs.DRAMEN_STAFF.value):
                osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.DRAMEN_STAFF.value))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        qh.query_backend()
        osrs.game.tele_home_fairy_ring('ajr')
        transport_functions.frem_dungeon_kurask()
        task_started = True
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.LEAFBLADED_BATTLEAXE.value))
        success = slayer_killer.main('kurask', pot_config.asdict(), 35)
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
