# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank
varrock_tele_widget_id = '218,23'


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
    {'id': ItemIDs.OSMUMTENS_FANG.value},
    {'id': ItemIDs.HOLY_BLESSING.value, 'consume': 'Equip'},
]

supplies = [
    {'id': ItemIDs.DRAMEN_STAFF.value, 'consume': 'Wield'},
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.PRAYER_POTION4.value,
    ItemIDs.PRAYER_POTION4.value,
    ItemIDs.PRAYER_POTION4.value,
    ItemIDs.PRAYER_POTION4.value,
    ItemIDs.PRAYER_POTION4.value,
    ItemIDs.EXTENDED_ANTIVENOM4.value,
    ItemIDs.EXTENDED_ANTIVENOM4.value,
    ItemIDs.EXTENDED_ANTIVENOM4.value,
    ItemIDs.EXTENDED_ANTIVENOM4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_4.value,
    {
        'id': ItemIDs.NATURE_RUNE.value,
        'quantity': 'All'
    }
]

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True, antivenom=True)


def pre_log():
    osrs.player.turn_off_all_prayers()
    osrs.move.go_to_loc(3679, 9800)
    osrs.move.interact_with_object(42595, 'y', 9000, False)
    osrs.clock.random_sleep(5, 5.5)


def post():
    osrs.move.interact_with_object(42594, 'y', 9000, True)
    osrs.move.go_to_loc(3669, 9816)


# need to change the pre log func
#42595
def run_to_spiders():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_tiles({'3600,3492,0'})
    while True:
        qh.query_backend()
        if 3589 <= qh.get_player_world_location('x') <= 3609 and 3486 <= qh.get_player_world_location('y') <= 3504:
            break
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') > 3599 and qh.get_player_world_location('y') < 3493:
            break
        elif qh.get_tiles('3600,3492,0'):
            osrs.move.fast_click(qh.get_tiles('3600,3492,0'))
    osrs.move.go_to_loc(3655, 3404)
    osrs.move.interact_with_object(42594, 'y', 9000, True)
    osrs.move.go_to_loc(3669, 9816)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('alq')
        run_to_spiders()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.OSMUMTENS_FANG.value))
        task_started = True
        success = slayer_killer.main(
            ['araxyte'], pot_config.asdict(), 35,
            attackable_area={'x_min': 3658, 'x_max': 3674, 'y_min': 9811, 'y_max': 9825},
            pre_hop=pre_log, post_login=post, prayers=['protect_melee']
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True