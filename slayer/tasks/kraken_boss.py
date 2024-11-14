# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer

from combat import cave_kraken

varrock_tele_widget_id = '218,23'


supplies = [
    osrs.item_ids.DRAMEN_STAFF,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.SUPER_DEFENCE4,
    osrs.item_ids.SUPER_DEFENCE4,
    {
        'id': [
            osrs.item_ids.NATURE_RUNE
        ],
        'quantity': 'All'
    },
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': [
            osrs.item_ids.FISHING_EXPLOSIVE_6664
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.SHARK
        ],
        'quantity': 'All'
    },
]

initial = [
    osrs.item_ids.TRIDENT_OF_THE_SWAMP,
    {
        'id': [
            osrs.item_ids.FIRE_RUNE,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.CHAOS_RUNE,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.DEATH_RUNE,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.ZULRAHS_SCALES,
        ],
        'quantity': 'All'
    },
]

equipment = [
    osrs.item_ids.BLACK_MASK,
    osrs.item_ids.FIRE_CAPE,
    osrs.item_ids.OCCULT_NECKLACE,
    {
        'id': [
            osrs.item_ids.KARILS_LEATHERTOP,
            osrs.item_ids.KARILS_LEATHERTOP_25,
            osrs.item_ids.KARILS_LEATHERTOP_50,
            osrs.item_ids.KARILS_LEATHERTOP_75,
            osrs.item_ids.KARILS_LEATHERTOP_100,
        ],
        'quantity': 1
    },
    {
        'id': [
            osrs.item_ids.KARILS_LEATHERSKIRT,
            osrs.item_ids.KARILS_LEATHERSKIRT_25,
            osrs.item_ids.KARILS_LEATHERSKIRT_50,
            osrs.item_ids.KARILS_LEATHERSKIRT_75,
            osrs.item_ids.KARILS_LEATHERSKIRT_100,
        ],
        'quantity': 1
    },
    osrs.item_ids.MALEDICTION_WARD,
    osrs.item_ids.BARROWS_GLOVES,
    osrs.item_ids.ETERNAL_BOOTS,
    osrs.item_ids.BRIMSTONE_RING,
]

initial_weapon_setup = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'slayer', 'items': initial}]
}

banking_config_equipment = {
    'dump_inv': True,
    'dump_equipment': False,
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
    while True:
        qh.query_backend()
        print('starting function')
        success = osrs.bank.banking_handler(initial_weapon_setup)
        if not success:
            print('failed to weapon and runes')
            return False
        while True:
            qh.query_backend()
            fire_rune = qh.get_inventory(osrs.item_ids.FIRE_RUNE)
            trident = qh.get_inventory(osrs.item_ids.TRIDENT_OF_THE_SWAMP)
            if fire_rune and trident:
                osrs.move.click(fire_rune)
                osrs.move.click(trident)
                osrs.clock.sleep_one_tick()
                osrs.keeb.write('2500')
                osrs.keeb.press_key('enter')
                osrs.move.click(trident)
                break

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
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.DRAMEN_STAFF):
                osrs.move.click(qh.get_inventory(osrs.item_ids.DRAMEN_STAFF))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('akq')
        transport_functions.kraken_cove_private()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(osrs.item_ids.TRIDENT_OF_THE_SWAMP))
        osrs.player.toggle_auto_retaliate('off')
        osrs.clock.sleep_one_tick()
        success = cave_kraken.main()
        qh.query_backend()
        osrs.player.toggle_auto_retaliate('on')
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

