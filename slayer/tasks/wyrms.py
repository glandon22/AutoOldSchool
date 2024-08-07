# 2134,9305,0
import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'


supplies = [
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.SUPER_COMBAT_POTION4.value,
    ItemIDs.SUPER_COMBAT_POTION4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_3.value,
    {
        'id': [
            ItemIDs.PRAYER_POTION4.value
        ],
        'quantity': '5'
    },
    {
        'id': ItemIDs.NATURE_RUNE.value,
        'quantity': 'All'
    },
    {
        'id': ItemIDs.MONKFISH.value,
        'quantity': 'All'
    },
]

equipment = [
    ItemIDs.DRAGON_HUNTER_LANCE.value,
    ItemIDs.RUNE_DEFENDER.value,
    ItemIDs.BARROWS_GLOVES.value,
    ItemIDs.FIRE_CAPE.value,
    ItemIDs.SLAYER_HELMET_I.value,
    ItemIDs.BRIMSTONE_RING.value,
    ItemIDs.BOOTS_OF_BRIMSTONE.value,
    ItemIDs.BANDOS_CHESTPLATE.value,
    ItemIDs.BANDOS_TASSETS.value,
    ItemIDs.AMULET_OF_FURY.value,
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

pot_config = slayer_killer.PotConfig(super_combat=True)


def pre_log():
    osrs.player.turn_off_all_prayers()
    osrs.clock.random_sleep(12, 12.1)


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
        osrs.game.tele_home_fairy_ring('cir')
        transport_functions.mount_karuulm_wyrms()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.DRAGON_HUNTER_LANCE.value))
        task_started = True
        success = slayer_killer.main(
            'wyrm', pot_config.asdict(), 35, pre_hop=pre_log, prayers=['protect_mage'],
            attackable_area={'x_min': 1251, 'x_max': 1276, 'y_min': 10147, 'y_max': 10161},
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
