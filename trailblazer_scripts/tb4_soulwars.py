import datetime

import osrs

barrier_tile = '2199,2842,0'
barrier_id = '41199'
blue_barrier = '40454'
red_barrier = '40457'
red_cem_barrier = '40455'
blue_cem_barrier = '40453'

def main():
    global team
    team = 'blue'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_wall_objects(
        {barrier_tile},
        {barrier_id}
    )
    qh.set_npcs(['10535', '10534'])
    qh.set_interating_with()
    last_barrier_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    team = False
    while True:
        sw_stuff = osrs.server.get_surrounding_wall_objects(8, [blue_barrier, red_barrier, red_cem_barrier, blue_cem_barrier])
        qh.query_backend()
        print(qh.get_player_world_location())
        if 2203 <= qh.get_player_world_location('x') <= 2218 and osrs.clock.time_diff_in_seconds(last_barrier_click).total_seconds() > 15:
            team = False
            osrs.move.run_towards_square_v2({'x': 2210, 'y': 2845, 'z': 0})
            osrs.clock.random_sleep(2, 2.3)
            qh.query_backend()
            barrier = qh.get_wall_objects(barrier_id)
            if barrier:
                osrs.move.click(barrier[0])
                last_barrier_click = datetime.datetime.now()
        elif 2839 <= qh.get_player_world_location('y') <= 2845 and 2190 <= qh.get_player_world_location('x') <= 2199:
            team = False
            print('waiting for game')
        # in the game, determine which team im on
        elif qh.get_player_world_location('x') >= 5000 and not team:
            if red_barrier in sw_stuff:
                team = 'red'
                osrs.move.click(sw_stuff[red_barrier][0])
                osrs.clock.random_sleep(4, 4.1)
                osrs.move.spam_click('{},{},0'.format(qh.get_player_world_location('x') - 20, qh.get_player_world_location('y') - 8), 0.6)
            elif blue_barrier in sw_stuff:
                team = 'blue'
                osrs.move.click(sw_stuff[blue_barrier][0])
                osrs.clock.random_sleep(4, 4.1)
                osrs.move.spam_click(
                    '{},{},0'.format(qh.get_player_world_location('x') + 20, qh.get_player_world_location('y') + 20),
                    0.6)
        elif qh.get_player_world_location('x') >= 5000 and not qh.get_interating_with():
            npcs = qh.get_npcs()
            closest = osrs.util.find_closest_alive_npc(npcs)
            if closest and closest['x'] and closest['y']:
                print('gggg', closest)
                osrs.move.fast_click(closest)
        elif qh.get_player_world_location('x') >= 5000 and red_cem_barrier in sw_stuff:
            print('dead')
            osrs.clock.random_sleep(5, 5.1)
            osrs.move.click(sw_stuff[red_cem_barrier][0])
            osrs.clock.random_sleep(3, 3.1)
            osrs.move.spam_click(
                '{},{},0'.format(qh.get_player_world_location('x'), qh.get_player_world_location('y') - 10),
                0.6)
            osrs.clock.random_sleep(1, 1.1)
            osrs.move.spam_click(
                '{},{},0'.format(qh.get_player_world_location('x'), qh.get_player_world_location('y') - 20),
                0.6)
        elif qh.get_player_world_location('x') >= 5000 and blue_cem_barrier in sw_stuff:
            print('dead')
            osrs.clock.random_sleep(5, 5.1)
            osrs.move.click(sw_stuff[blue_cem_barrier][0])
            osrs.clock.random_sleep(3, 3.1)
            osrs.move.spam_click(
                '{},{},0'.format(qh.get_player_world_location('x'), qh.get_player_world_location('y') + 10),
                0.6)
            osrs.clock.random_sleep(1, 1.1)
            osrs.move.spam_click(
                '{},{},0'.format(qh.get_player_world_location('x'), qh.get_player_world_location('y') + 20),
                0.6)
main()
