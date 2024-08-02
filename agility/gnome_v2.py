import osrs


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
            23145, 'y', 3434, False, obj_type='ground'
        )
        osrs.move.interact_with_object(
            23134, 'z', 1, True, obj_type='game', obj_tile={'x': 2473, 'y': 3425}
        )
        osrs.move.interact_with_object(
            23559, 'z', 2, True, obj_type='game'
        )
        osrs.move.interact_with_object(
            23557, 'x', 2478, True, obj_type='ground'
        )
        loot_handler.retrieve_loot()
        osrs.move.interact_with_object(
            23560, 'z', 1, False
        )
        osrs.move.interact_with_object(
            23135, 'y', 3426, True
        )
        osrs.move.interact_with_object(
            23138, 'y', 3433, True, obj_tile={'x': 2484, 'y': 3431}
        )
        osrs.move.go_to_loc(2474, 3436)
