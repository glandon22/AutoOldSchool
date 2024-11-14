# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank
varrock_tele_widget_id = '218,23'

equipment = [
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.melee_str_chest,
    gear_loadouts.melee_str_legs,
    {'id': osrs.item_ids.INSULATED_BOOTS, 'consume': 'Wear'},
    gear_loadouts.dragon_melee_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    gear_loadouts.dragon_melee_weapon,
    gear_loadouts.prayer_ammo_slot
]

supplies = [
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.MONKFISH,
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

