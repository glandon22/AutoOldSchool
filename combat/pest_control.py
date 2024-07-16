
import osrs

# square on dock: 2638,2653,0

# gangplank to start game 2637,2653,0 25632

# x < 2635 i am on boat

# 2657, 2612, 0 i am in game


# widget ids for portal healh
# sw = 408,24
# se = 408,23
# e = 408,22
# w = 408,21

port = '56799'
npcs_to_attack = '1693, 1736, 1707, 1692, 1721, 1702, 1691, 1732, 1730, 1708, 1720, 1731, 1722, 1706, 1713, 1737, 1701'

def enter_boat():
    plank = osrs.server.get_game_object('2637,2653,0', '25632', port)
    if plank:
        osrs.move.move_and_click(plank['x'], plank['y'], 3, 3)


def find_portal_to_run_to():
    east_portal = osrs.server.get_widget('408,22', port)
    if east_portal and 'text' in east_portal and int(east_portal['text']) > 0:
        return [20, -20]
    s_east_portal = osrs.server.get_widget('408,23', port)
    if s_east_portal and 'text' in s_east_portal and int(s_east_portal['text']) > 0:
        return [12, -35]
    s_west_portal = osrs.server.get_widget('408,24', port)
    if s_west_portal and 'text' in s_west_portal and int(s_west_portal['text']) > 0:
        return [-10, -40]
    west_portal = osrs.server.get_widget('408,21', port)
    if west_portal and 'text' in west_portal and int(west_portal['text']) > 0:
        return [-25, -20]
    return False

def main():
    # Use this value to store what instanced tile I start the game on
    global anchor_point
    anchor_point = None
    while True:
        curr_loc = osrs.server.get_world_location(port)
        interacting = osrs.server.get_interacting(port)
        # I am standing on dock
        if curr_loc and 'x' in curr_loc and 3000 > curr_loc['x'] >= 2638:
            anchor_point = None
            enter_boat()
            osrs.clock.random_sleep(2,3)
            continue
        # In boat waiting for game to begin
        if curr_loc and 'x' in curr_loc and curr_loc['x'] < 2636:
            print('Waiting for the game to start, I am in the boat.')
            continue
        # Game has started, I am still in the boat
        if curr_loc and 'x' in curr_loc and curr_loc['x'] > 3000 and not anchor_point:
            osrs.clock.random_sleep(1.2, 1.3)
            anchor_point = curr_loc
            print('Game has begun')
            osrs.move.run_towards_square_v2({'x': curr_loc['x'] + 20, 'y': curr_loc['y'] - 20, 'z': 0}, port)
            continue
        if not interacting and osrs.move.am_stationary(port):
            npcs = osrs.server.get_npcs_by_id(npcs_to_attack, port)
            if npcs:
                closest = osrs.util.find_closest_npc(npcs)
                if closest:
                    osrs.move.move_and_click(closest['x'], closest['y'], 2, 2)
                    osrs.clock.random_sleep(1, 1.2)
            # No NPCs in the area, run to a portal that is open.
            else:
                offset = find_portal_to_run_to()
                if offset and anchor_point:
                    osrs.move.run_towards_square_v2(
                        {'x': anchor_point['x'] + offset[0], 'y': anchor_point['y'] + offset[1], 'z': 0}, port
                    )
                continue

