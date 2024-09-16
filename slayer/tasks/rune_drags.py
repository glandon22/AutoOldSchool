# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank
varrock_tele_widget_id = '218,23'


equipment = [
    {'id': ItemIDs.DRAGONFIRE_SHIELD.value, 'consume': 'Wield'},
    {'id': ItemIDs.FIRE_CAPE.value, 'consume': 'Wear'},
    {'id': ItemIDs.SLAYER_HELMET_I.value, 'consume': 'Wear'},
    {'id': ItemIDs.BARROWS_GLOVES.value, 'consume': 'Wear'},
    {'id': ItemIDs.BRIMSTONE_RING.value, 'consume': 'Wear'},
    {'id': ItemIDs.INSULATED_BOOTS.value, 'consume': 'Wear'},
    {'id': ItemIDs.BANDOS_CHESTPLATE.value, 'consume': 'Wear'},
    {'id': ItemIDs.BANDOS_TASSETS.value, 'consume': 'Wear'},
    {'id': ItemIDs.AMULET_OF_FURY.value, 'consume': 'Wear'},
    {'id': ItemIDs.DRAGON_HUNTER_LANCE.value, 'consume': 'Wield'},
    {'id': ItemIDs.HOLY_BLESSING.value, 'consume': 'Equip'},
]

supplies = [
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.PRAYER_POTION4.value,
    ItemIDs.PRAYER_POTION4.value,
    ItemIDs.PRAYER_POTION4.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_4.value,
    {
        'id': ItemIDs.MONKFISH.value,
        'quantity': 'All'
    },
]

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True, antifire=True)


def pre_log():
    osrs.move.interact_with_object(
        32153, 'x', 1574, False, obj_tile={'x': 1574, 'y': 5074, 'z': 0},
        right_click_option='Pass', timeout=10
    )


def post_log():
    osrs.move.interact_with_object(
        32153, 'x', 1574, True, obj_tile={'x': 1574, 'y': 5074, 'z': 0},
        right_click_option='Pass', timeout=10
    )


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.rune_dragons()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            ['rune dragon'], pot_config.asdict(), 35, pre_hop=pre_log, post_login=post_log,
            prayers=['protect_mage', 'piety']
        )
        osrs.player.turn_off_all_prayers()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True

