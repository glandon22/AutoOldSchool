# 2134,9305,0
import datetime

import osrs

from combat import thermo_smoke_boss
from combat import slayer_killer

varrock_tele_widget_id = '218,23'

supplies = [
    {
        'id': [
            osrs.item_ids.RING_OF_DUELING1,
            osrs.item_ids.RING_OF_DUELING2,
            osrs.item_ids.RING_OF_DUELING3,
            osrs.item_ids.RING_OF_DUELING4,
            osrs.item_ids.RING_OF_DUELING5,
            osrs.item_ids.RING_OF_DUELING6,
            osrs.item_ids.RING_OF_DUELING7,
            osrs.item_ids.RING_OF_DUELING8
        ],
        'quantity': '1'
    },
    osrs.item_ids.RUNE_POUCH,
    {
        'id': [
            osrs.item_ids.NATURE_RUNE
        ],
        'quantity': 'All'
    },
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': [
            osrs.item_ids.SUPER_RESTORE4,
            osrs.item_ids.SUPER_RESTORE3,
            osrs.item_ids.SUPER_RESTORE2,
            osrs.item_ids.SUPER_RESTORE1
        ],
        'quantity': 'X',
        'amount': 20
    },
]

equipment = [
    osrs.item_ids.SLAYER_HELMET_I,
    osrs.item_ids.SANGUINESTI_STAFF,
    osrs.item_ids.FIRE_CAPE,
    osrs.item_ids.OCCULT_NECKLACE,
    {
        'id': [
            osrs.item_ids.AHRIMS_ROBESKIRT,
            osrs.item_ids.AHRIMS_ROBESKIRT_25,
            osrs.item_ids.AHRIMS_ROBESKIRT_50,
            osrs.item_ids.AHRIMS_ROBESKIRT_75,
            osrs.item_ids.AHRIMS_ROBESKIRT_100,
        ],
        'quantity': 1
    },
    {
        'id': [
            osrs.item_ids.AHRIMS_ROBETOP,
            osrs.item_ids.AHRIMS_ROBETOP_25,
            osrs.item_ids.AHRIMS_ROBETOP_50,
            osrs.item_ids.AHRIMS_ROBETOP_75,
            osrs.item_ids.AHRIMS_ROBETOP_100,
        ],
        'quantity': 1
    },
    osrs.item_ids.MALEDICTION_WARD,
    osrs.item_ids.BARROWS_GLOVES,
    osrs.item_ids.ETERNAL_BOOTS,
    osrs.item_ids.BRIMSTONE_RING,
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

