# 2134,9305,0
import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'


supplies = gear.slayer_melee['supplies']

equipment = gear.slayer_melee['equipment']

banking_config_equipment = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'slayer_melee', 'items': equipment}]
}

banking_config_supplies = {
    'dump_inv': True,
    'dump_equipment': False,
    'search': [{'query': 'slayer_melee', 'items': supplies}]
}

pot_config = slayer_killer.PotConfig(super_combat=True)


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
            osrs.inv.power_drop(qh.get_inventory(), [], equipment)
            qh.query_backend()
        success = osrs.bank.banking_handler(banking_config_supplies)
        if not success:
            print('failed to withdraw supplies.')
            return False
        osrs.game.tele_home()
        osrs.clock.random_sleep(2, 2.1)
        osrs.game.tele_home_fairy_ring('bjp')
        transport_functions.isle_of_souls_dungeon(2128, 9328)
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.ABYSSAL_WHIP.value))
        task_started = True
        success = slayer_killer.main('fire giant', pot_config.asdict(), 35, -1, -1, -1, )
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
