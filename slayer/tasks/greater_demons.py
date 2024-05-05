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
            for item in qh.get_inventory():
                osrs.move.click(item)
            qh.query_backend()
        success = osrs.bank.banking_handler(banking_config_supplies)
        if not success:
            print('failed to withdraw supplies.')
            return False
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.clock.random_sleep(2, 2.1)
        osrs.game.tele_home_fairy_ring('bjp')
        transport_functions.isle_of_souls_dungeon(2166, 9331)
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.ABYSSAL_WHIP.value))
        task_started = True
        success = slayer_killer.main('greater demon', pot_config.asdict(), 35, -1, -1, -1, )
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.DRAMEN_STAFF.value))
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True


'''
notes

add var like "trip_started" and set to true once trip begins,
that way if i need to re supply i can check that and know i dont need
to re gear. additionally i can break gear and supplies into two vars

also after banking i should put on my gear, then bank again and withdraw supplies

prob need to make a pre logout function here to run to a place i wont be aggro'd before logging out
'''
