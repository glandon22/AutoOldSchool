import datetime


import osrs
# anchor
# 2660,2608,0
# ladder 2666,2585,0
#+ 6, -23
port = '56799'
npcs_to_attack = '1693, 1736, 1707, 1692, 1721, 1702, 1691, 1732, 1730, 1708, 1720, 1731, 1722, 1706, 1713, 1737, 1701'
npc_ids = ['1693', '1736', '1707', '1692', '1721', '1702', '1691', '1732', '1730', '1708', '1720', '1731', '1722', '1706', '1713', '1737', '1701']
tower_ladder_id = '14296'


def enter_boat():
    plank = osrs.server.get_game_object('2637,2653,0', '25632', port)
    if plank:
        osrs.move.move_and_click(plank['x'], plank['y'], 3, 3)


def calc_anchor_point():
    boat_side = osrs.server.get_surrounding_wall_objects(15, ['14254'], port)
    if boat_side and '14254' in boat_side:
        return {'x': boat_side['14254'][0]['x_coord'], 'y': boat_side['14254'][0]['y_coord'], 'z': 0}
    return None


def climb_ladder(ap, qh: osrs.queryHelper.QueryHelper):
    last_click = datetime.datetime.now() - datetime.timedelta(seconds=500)
    while True:
        qh.set_game_objects(
            {
                '{},{},{}'.format(anchor_point['x'] + 6, anchor_point['y'] - 22, 0)
            },
            {tower_ladder_id}
        )
        qh.query_backend()
        if qh.get_player_world_location() and qh.get_player_world_location()['y'] < anchor_point['y'] - 22 and qh.get_player_world_location()['x'] == anchor_point['x'] + 6:
            return
        elif not qh.get_game_objects(tower_ladder_id):
            osrs.move.run_towards_square_v2({'x': anchor_point['x'] + 6, 'y': anchor_point['y'] - 22, 'z': 0})
        elif qh.get_game_objects(tower_ladder_id) and (datetime.datetime.now() - last_click).total_seconds() > 5:
            osrs.move.click(qh.get_game_objects(tower_ladder_id)[0])
            last_click = datetime.datetime.now()


def find_next_target(npcs):
    res = False
    for npc in npcs:
        if npc['health'] != 0:
            if not res or npc['dist'] < res['dist']:
                res = npc
    return res


script_config = {
    'intensity': 'high',
    'login': False,
    'logout': lambda: osrs.clock.random_sleep(11, 14),
}


def main():
    global anchor_point
    # Use this value to store what instanced tile I start the game on
    anchor_point = None
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(npc_ids)
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defense'})
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_player_world_location()
    while True:
        # log if its late
        curr_time = datetime.datetime.now()
        if curr_time.hour == 1:
            return print('its 1am')
        qh.query_backend()
        curr_loc = qh.get_player_world_location()
        # I am standing on dock
        if curr_loc and 'x' in curr_loc and 3000 > curr_loc['x'] >= 2638:
            anchor_point = None
            osrs.clock.sleep_one_tick()
            osrs.game.break_manager_v4(script_config)
            enter_boat()
            osrs.clock.random_sleep(2, 3)
            continue
        # In boat waiting for game to begin
        if curr_loc and 'x' in curr_loc and curr_loc['x'] < 2636:
            print('Waiting for the game to start, I am in the boat.')
            continue
        # Game has started, I am still in the boat
        if curr_loc and 'x' in curr_loc and 50000 > curr_loc['x'] > 3000 and not anchor_point:
            osrs.clock.random_sleep(0.6, 0.7)
            anchor_point = calc_anchor_point()
            print('Game has begun')
            climb_ladder(anchor_point, qh)
            continue
        if not qh.get_interating_with():
            npcs = osrs.server.get_npcs_by_id(npcs_to_attack, port)
            if npcs:
                closest = find_next_target(npcs)
                if closest and closest['x'] < 1915 and closest['y'] < 1040:
                    osrs.move.fast_click(closest)

