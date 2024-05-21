# 2134,9305,0
import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'


supplies = [ItemIDs.WATERBIRTH_TELEPORT.value, *gear.slayer_melee['supplies']]

equipment = gear.slayer_melee['equipment']

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
        qh.query_backend()
        tab = qh.get_inventory(ItemIDs.WATERBIRTH_TELEPORT.value)
        if not tab:
            exit('missing tele tab')
        osrs.move.click(tab)
        transport_functions.waterbirth_dungeon()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.ABYSSAL_WHIP.value))
        task_started = True
        success = slayer_killer.main(
            'dagannoth',
            pot_config.asdict(), 35,
            attackable_area={'x_min': 2442, 'x_max': 2487, 'y_min': 10125, 'y_max': 10163}
        )
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.DRAMEN_STAFF.value))
