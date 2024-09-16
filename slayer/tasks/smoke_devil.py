# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from slayer.utils import bank
from combat import slayer_killer

varrock_tele_widget_id = '218,23'

supplies = [
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
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
    ItemIDs.KARAMJA_GLOVES_4.value,
    {
        'id': [
            ItemIDs.PRAYER_POTION4.value,
            ItemIDs.PRAYER_POTION3.value,
            ItemIDs.PRAYER_POTION2.value,
            ItemIDs.PRAYER_POTION1.value,
        ],
        'quantity': '10'
    },
    {
        'id': [
            ItemIDs.PRAYER_POTION4.value,
            ItemIDs.PRAYER_POTION3.value,
            ItemIDs.PRAYER_POTION2.value,
            ItemIDs.PRAYER_POTION1.value,
        ],
        'quantity': '5'
    },
]

equipment = [
    {'id': ItemIDs.DRAGON_DEFENDER.value, 'consume': 'Wield'},
    {'id': ItemIDs.FIRE_CAPE.value, 'consume': 'Wear'},
    {'id': ItemIDs.SLAYER_HELMET_I.value, 'consume': 'Wear'},
    {'id': ItemIDs.BARROWS_GLOVES.value, 'consume': 'Wear'},
    {'id': ItemIDs.BRIMSTONE_RING.value, 'consume': 'Wear'},
    {'id': ItemIDs.DRAGON_BOOTS.value, 'consume': 'Wear'},
    {'id': ItemIDs.BANDOS_CHESTPLATE.value, 'consume': 'Wear'},
    {'id': ItemIDs.BANDOS_TASSETS.value, 'consume': 'Wear'},
    {'id': ItemIDs.AMULET_OF_FURY.value, 'consume': 'Wear'},
    {'id': ItemIDs.OSMUMTENS_FANG.value, 'consume': 'Wield'},
    {'id': ItemIDs.HOLY_BLESSING.value, 'consume': 'Equip'},
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def pre_log():
    osrs.player.turn_off_all_prayers()
    osrs.clock.random_sleep(11, 12)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.transport.dueling_to_c_wars()
        osrs.transport.walk_out_of_c_wars()
        osrs.move.go_to_loc(2414, 3060)
        osrs.move.interact_with_object(30176, 'y', 5500, True)
        osrs.move.go_to_loc(2406, 9452, right_click=True)
        task_started = True
        success = slayer_killer.main(
            ['smoke devil'], pot_config.asdict(), 35, hop=True,
            pre_hop=pre_log, prayers=['protect_range']
        )
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

'''
run to 2406,9452, 0




'''