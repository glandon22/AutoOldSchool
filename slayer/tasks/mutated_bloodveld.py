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
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.RUNE_POUCH.value,
        ItemIDs.KARAMJA_GLOVES_3.value,
        {
            'id': ItemIDs.PRAYER_POTION4.value,
            'quantity': '10'
        },
        {
            'id': ItemIDs.NATURE_RUNE.value,
            'quantity': 'All'
        },
    ]
equipment = [
    ItemIDs.SLAYER_HELMET_I.value,
    ItemIDs.ABYSSAL_WHIP.value,
    ItemIDs.BARROWS_GLOVES.value,
    ItemIDs.BRIMSTONE_RING.value,
    ItemIDs.DRAGON_BOOTS.value,
    ItemIDs.MONKS_ROBE.value,
    ItemIDs.MONKS_ROBE_TOP.value,
    ItemIDs.AMULET_OF_FURY.value,
    ItemIDs.RUNE_DEFENDER.value,
    ItemIDs.HOLY_BLESSING.value,
    ItemIDs.FIRE_CAPE.value,
]

banking_config_equipment = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'slayer', 'items': list(equipment)}]
}

banking_config_supplies = {
    'dump_inv': True,
    'dump_equipment': False,
    'search': [{'query': 'slayer', 'items': supplies}]
}

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def hop_logic():
    osrs.player.turn_off_all_prayers()
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
        transport_functions.catacombs(1693, 10015)
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'mutated bloodveld',
            pot_config.asdict(), 35,
            hop=True, pre_hop=hop_logic, prayers=['protect_melee']
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
