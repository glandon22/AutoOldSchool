import datetime
import osrs
from threading import Thread

boat_plank_tile = '2637,2653,0'
boat_plank_id = '25632'
tower_ladder_id = '14296'

game_state = osrs.queryHelper.QueryHelper()


# +7 -24


def query_server(gs: osrs.queryHelper.QueryHelper):
    osrs.dev.logger.info('Starting server querying thread.')
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([])
    qh.set_player_world_location()
    qh.set_game_objects(
        {boat_plank_tile},
        {boat_plank_id}
    )
    qh.set_interating_with()
    while True:
        gs.game_data = qh.query_backend()


t = Thread(target=query_server, args=(game_state,))
t.start()


def find_next_target(npcs):
    res = False
    for npc in npcs:
        # dont attack the squire or the knight
        if npc['health'] != 0 and 'Void' not in npc['name'] and 'Squire' not in npc['name']:
            if not res or npc['dist'] < res['dist']:
                res = npc
    return res


def climb_tower():
    raw_tiles = [
        [2658, 2610, 0],
        [2659, 2602, 0],
        [2663, 2595, 0],
        [2664, 2587, 0]
    ]
    x_diff = game_state.get_player_world_location('x') - 2658
    y_diff = game_state.get_player_world_location('y') - 2610
    while True:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_tiles({
            f'{raw_tiles[0][0] + x_diff},{raw_tiles[0][1] + y_diff},0',
            f'{raw_tiles[1][0] + x_diff},{raw_tiles[1][1] + y_diff},0',
            f'{raw_tiles[2][0] + x_diff},{raw_tiles[2][1] + y_diff},0',
            f'{raw_tiles[3][0] + x_diff},{raw_tiles[3][1] + y_diff},0',
        })
        parsed_tiles = [
            f'{raw_tiles[0][0] + x_diff},{raw_tiles[0][1] + y_diff},0',
            f'{raw_tiles[1][0] + x_diff},{raw_tiles[1][1] + y_diff},0',
            f'{raw_tiles[2][0] + x_diff},{raw_tiles[2][1] + y_diff},0',
            f'{raw_tiles[3][0] + x_diff},{raw_tiles[3][1] + y_diff},0',
        ]
        area_to_search = osrs.util.generate_surrounding_tiles_from_point(
            15, game_state.get_player_world_location()
        )
        qh.set_objects(
            set(area_to_search),
            {tower_ladder_id},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.query_backend()
        stopped = False
        for tile in reversed(parsed_tiles):
            if abs(game_state.get_player_world_location('x') - (raw_tiles[3][0] + x_diff)) <= 2 \
                    and abs(game_state.get_player_world_location('y') - (raw_tiles[3][1] + y_diff)) <= 2:
                print(game_state.get_player_world_location('x'), raw_tiles[3][0] + x_diff,
                      game_state.get_player_world_location('y'), raw_tiles[3][1] + y_diff)
                stopped = True
                break
            if osrs.move.is_clickable(qh.get_tiles(tile)):
                osrs.move.fast_click(qh.get_tiles(tile))
                break
        if stopped:
            break

    last_ladder_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh = osrs.queryHelper.QueryHelper()
        area_to_search = osrs.util.generate_surrounding_tiles_from_point(
            15, game_state.get_player_world_location()
        )
        qh.set_objects(
            set(area_to_search),
            {tower_ladder_id},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.query_backend()
        ladders = qh.get_objects(
            osrs.queryHelper.ObjectTypes.GAME.value,
            tower_ladder_id
        )
        if ladders:
            c = osrs.util.find_closest_target(qh.get_objects(
                osrs.queryHelper.ObjectTypes.GAME.value,
                tower_ladder_id
            ))
            if c:
                if game_state.get_player_world_location('y') < c['y_coord']:
                    return
                elif (datetime.datetime.now() - last_ladder_click).total_seconds() > 3:
                    osrs.move.fast_click(c)
                    last_ladder_click = datetime.datetime.now()


script_config = {
    'intensity': 'high',
    'logout': False,
    'login': False
}


def main():
    # let the server populate game state
    osrs.clock.random_sleep(1, 1.1)
    last_plank_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    climbed_tower = False
    while True:
        if 3000 >= game_state.get_player_world_location('x') >= 2638:
            osrs.game.break_manager_v4(script_config)

        if 3000 >= game_state.get_player_world_location('x') >= 2638 \
                and (datetime.datetime.now() - last_plank_click).total_seconds() > 1:
            if game_state.get_game_objects(boat_plank_id) \
                    and osrs.move.is_clickable(game_state.get_game_objects(boat_plank_id)[0]):
                osrs.move.fast_click(game_state.get_game_objects(boat_plank_id)[0])
                osrs.move.fast_click(game_state.get_game_objects(boat_plank_id)[0])
                last_plank_click = datetime.datetime.now()
                climbed_tower = False
        elif game_state.get_player_world_location('x') > 3001:
            if not climbed_tower:
                climb_tower()
                climbed_tower = True
            elif not game_state.get_interating_with():
                c = find_next_target(game_state.get_npcs())
                if c and osrs.move.is_clickable(c):
                    osrs.move.fast_click(c)

