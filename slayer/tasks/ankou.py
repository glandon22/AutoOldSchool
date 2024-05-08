# 2134,9305,0
import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'

# for this one i dont want a slayer ring with only one charge,
# bc i tele to the cave, then to nieve after the task is done
supplies = [
        ItemIDs.SUPER_COMBAT_POTION4.value,
        ItemIDs.SUPER_COMBAT_POTION4.value,
        ItemIDs.RUNE_POUCH.value,
        {
            'id': [
                ItemIDs.SLAYER_RING_2.value,
                ItemIDs.SLAYER_RING_3.value,
                ItemIDs.SLAYER_RING_4.value,
                ItemIDs.SLAYER_RING_5.value,
                ItemIDs.SLAYER_RING_6.value,
                ItemIDs.SLAYER_RING_7.value,
                ItemIDs.SLAYER_RING_8.value,
            ],
            'quantity': '1'
        },
        {
            'id': ItemIDs.MONKFISH.value,
            'quantity': 'All'
        },
    ]
equipment = gear.pure_melee['equipment']

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


def hop_logic():
    osrs.clock.random_sleep(11, 11.1)


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
        transport_functions.stronghold_slayer_dungeon_ankou()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main('ankou', pot_config.asdict(), 35, 15, -1, -1, -1, hop=True, pre_hop=hop_logic)
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

