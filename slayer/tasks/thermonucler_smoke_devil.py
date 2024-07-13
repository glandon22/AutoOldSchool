# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from combat import thermo_smoke_boss
from combat import slayer_killer

varrock_tele_widget_id = '218,23'

supplies = [
    {
        'id': [
            ItemIDs.RING_OF_DUELING1.value,
            ItemIDs.RING_OF_DUELING2.value,
            ItemIDs.RING_OF_DUELING3.value,
            ItemIDs.RING_OF_DUELING4.value,
            ItemIDs.RING_OF_DUELING5.value,
            ItemIDs.RING_OF_DUELING6.value,
            ItemIDs.RING_OF_DUELING7.value,
            ItemIDs.RING_OF_DUELING8.value
        ],
        'quantity': '1'
    },
    ItemIDs.RUNE_POUCH.value,
    {
        'id': [
            ItemIDs.NATURE_RUNE.value
        ],
        'quantity': 'All'
    },
    ItemIDs.KARAMJA_GLOVES_3.value,
    {
        'id': [
            ItemIDs.SUPER_RESTORE4.value,
            ItemIDs.SUPER_RESTORE3.value,
            ItemIDs.SUPER_RESTORE2.value,
            ItemIDs.SUPER_RESTORE1.value
        ],
        'quantity': 'X',
        'amount': 20
    },
]

equipment = [
    ItemIDs.SLAYER_HELMET_I.value,
    ItemIDs.SANGUINESTI_STAFF.value,
    ItemIDs.FIRE_CAPE.value,
    ItemIDs.OCCULT_NECKLACE.value,
    {
        'id': [
            ItemIDs.AHRIMS_ROBESKIRT.value,
            ItemIDs.AHRIMS_ROBESKIRT_25.value,
            ItemIDs.AHRIMS_ROBESKIRT_50.value,
            ItemIDs.AHRIMS_ROBESKIRT_75.value,
            ItemIDs.AHRIMS_ROBESKIRT_100.value,
        ],
        'quantity': 1
    },
    {
        'id': [
            ItemIDs.AHRIMS_ROBETOP.value,
            ItemIDs.AHRIMS_ROBETOP_25.value,
            ItemIDs.AHRIMS_ROBETOP_50.value,
            ItemIDs.AHRIMS_ROBETOP_75.value,
            ItemIDs.AHRIMS_ROBETOP_100.value,
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
    osrs.clock.random_sleep(10, 11)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    print('starting function')
    success = osrs.bank.banking_handler(banking_config_equipment)
    if not success:
        print('failed to withdraw equipment.')
        return False
    osrs.clock.sleep_one_tick()
    qh.query_backend()
    for item in qh.get_inventory():
        osrs.move.click(item)
    success = osrs.bank.banking_handler(banking_config_supplies)
    if not success:
        print('failed to withdraw supplies.')
        return False
    osrs.game.tele_home()
    osrs.game.click_restore_pool()
    osrs.transport.dueling_to_c_wars()
    osrs.transport.walk_out_of_c_wars()
    osrs.move.go_to_loc(2414, 3060)
    osrs.move.interact_with_object(30176, 'y', 5500, True)
    osrs.move.go_to_loc(2381, 9452, right_click=True)
    osrs.move.interact_with_object(535, 'x', 2376, False, obj_type='wall')
    osrs.move.go_to_loc(2367, 9447, right_click=True)
    thermo_smoke_boss.main()
    qh.query_backend()
    osrs.game.cast_spell(varrock_tele_widget_id)

