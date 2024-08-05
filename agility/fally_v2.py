import osrs


def fell():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_player_world_location('z') == 0:
        osrs.move.go_to_loc(3032, 3342)
        return True


def main(goal):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'agility'})
    loot_handler = osrs.loot.Loot()
    while True:
        qh.query_backend()
        if qh.get_skills('agility') and qh.get_skills('agility')['level'] >= goal:
            return
        osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False,
        })
        osrs.player.toggle_run('on')
        osrs.move.interact_with_object(
            14898, 'z', 1, True, obj_type='decorative'
        )
        osrs.move.interact_with_object(
            14899, 'x', 3041, True, obj_type='ground', custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14901, 'y', 3349, True, obj_type='game', custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14903, 'y', 3359, True, custom_exit_function=fell
        )
        # loot_handler.retrieve_loot()
        osrs.move.interact_with_object(
            14904, 'x', 3044, False, custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14905, 'x', 3033, False, custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14911, 'x', 3025, False, obj_type='ground', custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14919, 'y', 3351, False, custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14920, 'x', 3015, False, custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14921, 'y', 3342, False, custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14923, 'y', 3334, False, custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14924, 'x', 3018, True, custom_exit_function=fell
        )
        osrs.move.interact_with_object(
            14925, 'x', 3028, True, custom_exit_function=fell
        )

main(99)