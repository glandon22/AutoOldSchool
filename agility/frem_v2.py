import random

import osrs
from osrs.game import slow_lumb_tele

equipment = [
    {'id': osrs.item_ids.GRACEFUL_TOP, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_CAPE, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_HOOD, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_LEGS, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_BOOTS, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_GLOVES, 'consume': 'Wear'},
    osrs.item_ids.RUNE_POUCH
]


def start():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 2619 <= qh.get_player_world_location('x') <= 2654 and 3635 <= qh.get_player_world_location('y') <= 3683:
        osrs.dev.logger.info('Already in Rellekka, no need to run starter function.')
        return
    osrs.game.slow_lumb_tele()
    osrs.move.go_to_loc(3208, 3211)
    osrs.move.interact_with_object_v3(
        14880, obj_type='ground', coord_type='y', coord_value=9000,
        greater_than=True, right_click_option='Climb-down', timeout=8
    )
    osrs.bank.banking_handler({
        'dump_equipment': True,
        'dump_inv': True,
        'search': [{'query': 'agil', 'items': equipment}]
    })
    osrs.game.cast_spell(osrs.widget_ids.camelot_tele_spell_widget_id)
    osrs.move.go_to_loc(2617, 3673)


def loot_handler(area):
    loot = osrs.loot.Loot()
    loot.retrieve_loot(loot_area=area)


def handle_falling(success):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_player_world_location('z') == 0:
        return True
    elif success['greater_than'] and qh.get_player_world_location(success['coord_type']) >= success['coord_value']:
        return True
    elif not success['greater_than'] and qh.get_player_world_location(success['coord_type']) <= success['coord_value']:
        return True


def main(goal=99, endless_loop=True):
    start()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'agility'})
    iter_count = 9999 if endless_loop else random.randint(3, 5)
    while True:
        break_info = osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False
        })
        if iter_count == 0:
            return
        elif 'took_break' in break_info and break_info['took_break']:
            iter_count -= 1
        qh.query_backend()
        if qh.get_skills('agility') and qh.get_skills('agility')['level'] >= goal:
            return
        osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False,
        })
        osrs.player.toggle_run('on')
        osrs.move.interact_with_object_v3(
            14946, 'z', 1, True,
            obj_type='decorative', right_click_option='Climb', timeout=15
        )
        osrs.move.interact_with_object_v3(
            14947, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 2622, 'x_max': 2626, 'y_min': 3672, 'y_max': 3676},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'y', 'coord_value': 3671, 'greater_than': False},
            right_click_option='Leap', timeout=5
        )
        osrs.move.interact_with_object_v3(
            14987, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 2615, 'x_max': 2622, 'y_min': 3658, 'y_max': 3668},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'x', 'coord_value': 2626, 'greater_than': True},
            right_click_option='Cross', timeout=9
        )
        osrs.move.interact_with_object_v3(
            14990, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 2626, 'x_max': 2630, 'y_min': 3651, 'y_max': 3655},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'x', 'coord_value': 2639, 'greater_than': True},
            right_click_option='Leap', timeout=15
        )
        osrs.move.interact_with_object_v3(
            14991, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 2639, 'x_max': 2644, 'y_min': 3649, 'y_max': 3653},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'y', 'coord_value': 3657, 'greater_than': True}
        )
        osrs.move.interact_with_object_v3(
            14992, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 2643, 'x_max': 2650, 'y_min': 3657, 'y_max': 3662},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'x', 'coord_value': 2654, 'greater_than': True},
            right_click_option='Cross', timeout=9
        )
        osrs.move.interact_with_object_v3(
            14994, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 2655, 'x_max': 2662, 'y_min': 3665, 'y_max': 3681},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'x', 'coord_value': 2652, 'greater_than': False}
        )
