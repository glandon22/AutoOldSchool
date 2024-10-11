import osrs


def click_start():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'3508,3489,0'})
    qh.query_backend()
    if qh.get_tiles('3508,3489,0'):
        osrs.move.fast_click_v2(qh.get_tiles('3508,3489,0'))
    else:
        steps = osrs.move.run_towards_square(
            {'x': 3508, 'y': 3489, 'z': 0},
            steps_only=True
        )
        osrs.move.fixed_follow_path(steps)


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


def main(goal):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'agility'})
    while True:
        qh.query_backend()
        if qh.get_skills('agility') and qh.get_skills('agility')['level'] >= goal:
            return
        osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False,
        })
        # '3490,3491,0'
        osrs.player.toggle_run('on')
        osrs.move.interact_with_object_v3(
            14843, 'z', 1, True, right_click_option='Climb',
            pre_interact=click_start
        )
        osrs.move.interact_with_object_v3(
            14844, 'y', 3498, True, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 3503, 'x_max': 3511, 'y_min': 3491, 'y_max': 3499}
        )
        osrs.move.interact_with_object_v3(
            14845, 'x', 3496, False, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 3496, 'x_max': 3504, 'y_min': 3503, 'y_max': 3507}
        )
        osrs.move.interact_with_object_v3(
            14848, 'x', 3485, False, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 3485, 'x_max': 3493, 'y_min': 3498, 'y_max': 3505}
        )
        # can fail after obstacle above
        osrs.move.interact_with_object_v3(
            14846, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 3474, 'x_max': 3480, 'y_min': 3491, 'y_max': 3500},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'y', 'coord_value': 3490, 'greater_than': False}
        )
        osrs.move.interact_with_object_v3(
            14894, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 3477, 'x_max': 3484, 'y_min': 3481, 'y_max': 3487},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'y', 'coord_value': 3480, 'greater_than': False}
        )
        osrs.move.interact_with_object_v3(
            14847, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 3488, 'x_max': 3403, 'y_min': 3468, 'y_max': 3478},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'x', 'coord_value': 3504, 'greater_than': True}
        )
        osrs.move.interact_with_object_v3(
            14897, 'y', 3483, True, pre_interact=loot_handler,
            pre_interact_arg={'x_min': 3508, 'x_max': 3516, 'y_min': 3474, 'y_max': 3482},
            custom_exit_function=handle_falling,
            custom_exit_function_arg={'coord_type': 'y', 'coord_value': 3483, 'greater_than': True}
        )

main(99)