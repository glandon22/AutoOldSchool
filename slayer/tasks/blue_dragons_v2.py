# 2134,9305,0
import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'


supplies = [ItemIDs.DRAMEN_STAFF.value, *gear.melee_dragon['supplies']]

equipment = gear.melee_dragon['equipment']

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

pot_config = slayer_killer.PotConfig(super_combat=True, antifire=True)


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
            if qh.get_inventory(ItemIDs.DRAMEN_STAFF.value):
                osrs.move.click(qh.get_inventory(ItemIDs.DRAMEN_STAFF.value))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('bjp')
        transport_functions.isle_of_souls_dungeon(2134, 9305)
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.DRAGON_HUNTER_LANCE.value))
        task_started = True
        success = slayer_killer.main(['blue dragon', 'baby blue dragon'], pot_config.asdict(), 35, 15)
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
