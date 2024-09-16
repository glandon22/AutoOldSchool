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
            15608, 'z', 1, True, obj_type='decorative',
            right_click_option='Climb-up', timeout=4
        )
        osrs.move.interact_with_object(
            15609, 'y', 3310, True, obj_type='game'
        )
        osrs.move.interact_with_object(
            26635, 'x', 2661, False, obj_type='ground'
        )
        loot_handler.retrieve_loot()
        osrs.move.interact_with_object(
            15610, 'y', 3317, False, obj_type='game'
        )
        osrs.move.interact_with_object(
            15611, 'y', 3310, False
        )
        osrs.move.interact_with_object(
            28912, 'x', 2654, True
        )
        osrs.move.interact_with_object(
            15612, 'x', 2668, True
        )
main(99)