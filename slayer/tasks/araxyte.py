# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank
varrock_tele_widget_id = '218,23'

weapon = gear_loadouts.high_def_weapon
equipment = [
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.melee_str_chest,
    gear_loadouts.melee_str_legs,
    gear_loadouts.melee_boots,
    gear_loadouts.melee_str_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    weapon,
    gear_loadouts.prayer_ammo_slot
]

supplies = [
    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.PRAYER_POTION4,
    osrs.item_ids.EXTENDED_ANTIVENOM4,
    osrs.item_ids.EXTENDED_ANTIVENOM4,
    osrs.item_ids.EXTENDED_ANTIVENOM4,
    osrs.item_ids.EXTENDED_ANTIVENOM4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'All'
    }
]

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True, antivenom=True)


def pre_log():
    steps = osrs.move.run_towards_square(
        {'x': 3661, 'y': 9836, 'z': 0},
        steps_only=True
    )
    osrs.move.fixed_follow_path(steps)
    steps = osrs.move.run_towards_square(
        {'x': 3679, 'y': 9800, 'z': 0},
        steps_only=True
    )
    osrs.move.fixed_follow_path(steps)
    osrs.move.interact_with_object(42595, 'y', 9000, False)
    osrs.clock.random_sleep(5, 5.5)


def post():
    osrs.move.interact_with_object(42594, 'y', 9000, True)
    steps = osrs.move.run_towards_square(
        {'x': 3674, 'y': 9837, 'z': 0},
        steps_only=True
    )
    osrs.move.fixed_follow_path(steps)


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
    steps = osrs.move.run_towards_square(
        {'x': 3674, 'y': 9837, 'z': 0},
        steps_only=True
    )
    osrs.move.fixed_follow_path(steps)


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
        osrs.move.click(qh.get_inventory(weapon['id'][0]))
        task_started = True
        success = slayer_killer.main(
            ['araxyte'], pot_config.asdict(), 35,
            attackable_area={'x_min': 3671, 'x_max': 3690, 'y_min': 9835, 'y_max': 9847},
            pre_hop=pre_log, post_login=post, prayers=['protect_melee']
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
