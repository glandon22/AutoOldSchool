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
    'search': [{'query': 'slayer', 'items': [osrs.item_ids.DRAMEN_STAFF, *supplies]}]
}

pot_config = slayer_killer.PotConfig(super_combat=True)


def pre_log():
    osrs.clock.random_sleep(12, 13)


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
            if qh.get_inventory(osrs.item_ids.osrs.item_ids.DRAMEN_STAFF):
                osrs.move.click(qh.get_inventory(osrs.item_ids.osrs.item_ids.DRAMEN_STAFF))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        qh.query_backend()
        osrs.game.tele_home_fairy_ring('ajr')
        transport_functions.frem_dungeon_turoth()
        task_started = True
        osrs.move.click(qh.get_inventory(osrs.item_ids.osrs.item_ids.LEAFBLADED_BATTLEAXE))
        success = slayer_killer.main('turoth', pot_config.asdict(), 35, hop=True, pre_hop=pre_log)
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
