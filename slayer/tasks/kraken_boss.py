# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

from combat import cave_kraken

varrock_tele_widget_id = '218,23'


supplies = [
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.SUPER_DEFENCE4.value,
    ItemIDs.SUPER_DEFENCE4.value,
    {
        'id': [
            ItemIDs.NATURE_RUNE.value
        ],
        'quantity': 'All'
    },
    ItemIDs.KARAMJA_GLOVES_3.value,
    {
        'id': [
            ItemIDs.FISHING_EXPLOSIVE_6664.value
        ],
        'quantity': 'All'
    },
    {
        'id': [
            ItemIDs.SHARK.value
        ],
        'quantity': 'All'
    },
]

equipment = [
    ItemIDs.SLAYER_HELMET_I.value,
    ItemIDs.FIRE_CAPE.value,
    ItemIDs.OCCULT_NECKLACE.value,
    ItemIDs.TRIDENT_OF_THE_SWAMP.value,
    {
        'id': [
            ItemIDs.KARILS_LEATHERTOP.value,
            ItemIDs.KARILS_LEATHERTOP_25.value,
            ItemIDs.KARILS_LEATHERTOP_50.value,
            ItemIDs.KARILS_LEATHERTOP_75.value,
            ItemIDs.KARILS_LEATHERTOP_100.value,
        ],
        'quantity': 1
    },
    {
        'id': [
            ItemIDs.KARILS_LEATHERSKIRT.value,
            ItemIDs.KARILS_LEATHERSKIRT_25.value,
            ItemIDs.KARILS_LEATHERSKIRT_50.value,
            ItemIDs.KARILS_LEATHERSKIRT_75.value,
            ItemIDs.KARILS_LEATHERSKIRT_100.value,
        ],
        'quantity': 1
    },
    ItemIDs.MALEDICTION_WARD.value,
    ItemIDs.BARROWS_GLOVES.value,
    ItemIDs.ETERNAL_BOOTS.value,
    ItemIDs.BRIMSTONE_RING.value,
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

pot_config = slayer_killer.PotConfig(super_def=True)


def pre_log():
    osrs.clock.random_sleep(10,11)


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
        osrs.game.tele_home_fairy_ring('akq')
        transport_functions.kraken_cove_private()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.TRIDENT_OF_THE_SWAMP.value))
        task_started = True
        success = cave_kraken.main()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

