import datetime

import osrs
import osrs.move

from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'
trollheim_tele_widget_id = '218,54'


supplies = [
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.SUPER_RESTORE4,
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'All'
    },
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'X',
        'amount': '9'
    },
    {
        'id': osrs.item_ids.PRAYER_POTION4,
        'quantity': '10'
    },
]

equipment = [
    {'id': osrs.item_ids.TOKTZKETXIL, 'consume': 'Wield'},
    {'id': osrs.item_ids.ZAMORAK_CLOAK, 'consume': 'Wear'},
    {'id': [osrs.item_ids.BLACK_MASK, osrs.item_ids.SLAYER_HELMET, osrs.item_ids.SLAYER_HELMET_I], 'consume': 'Wear'},
    {'id': osrs.item_ids.ARMADYL_BRACERS, 'consume': 'Wear'},
    {'id': osrs.item_ids.BRIMSTONE_RING, 'consume': 'Wear'},
    {'id': osrs.item_ids.DRAGON_BOOTS, 'consume': 'Wear'},
    {'id': osrs.item_ids.BANDOS_CHESTPLATE, 'consume': 'Wear'},
    {'id': osrs.item_ids.BANDOS_TASSETS, 'consume': 'Wear'},
    {'id': osrs.item_ids.AMULET_OF_FURY, 'consume': 'Wear'},
    {'id': osrs.item_ids.OSMUMTENS_FANG, 'consume': 'Wield'},
    {'id': osrs.item_ids.HOLY_BLESSING, 'consume': 'Equip'},
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

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def pre_log():
    osrs.clock.random_sleep(11, 12)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.clock.sleep_one_tick()
        osrs.game.cast_spell(trollheim_tele_widget_id)
        transport_functions.godwars_main_room()
        task_started = True
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.SUPER_RESTORE4):
                osrs.move.fast_click(qh.get_inventory(osrs.item_ids.SUPER_RESTORE4))
            else:
                break
        # success = slayer_killer.main('spiritual mage', pot_config.asdict(), 35, prayers=['protect_mage'], ignore_interacting=True, pre_hop=pre_log)
        # success = slayer_killer.main('spiritual warrior', pot_config.asdict(), 35, prayers=['protect_melee'], ignore_interacting=True, pre_hop=pre_log)
        success = slayer_killer.main('spiritual ranger', pot_config.asdict(), 35, prayers=['protect_range'], ignore_interacting=True, pre_hop=pre_log)
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
