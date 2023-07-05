import datetime
import math

import osrs
# about to get hit by lightning game ovject 41006

def click_ladder():
    ladder = osrs.server.get_game_object('3135,2840,0', '41305')
    if ladder:
        osrs.move.move_and_click(ladder['x'], ladder['y'], 3, 3)
        return {'41305': datetime.datetime.now()}
    else:
        osrs.move.run_towards_square_v2({'x': 3135, 'y': 2840, 'z': 0})


def verify_inv(inv):
    rope = osrs.inv.is_item_in_inventory_v2(inv, '954')
    water_bucket_quantity = osrs.inv.get_item_quantity_in_inv(inv, 1929)
    empty_bucket_quantity = osrs.inv.get_item_quantity_in_inv(inv, 1925)
    need_buckets = True
    if water_bucket_quantity + empty_bucket_quantity >= 3:
        need_buckets = False
    return {'need_rope': not bool(rope), 'need_buckets': need_buckets}


def get_supplies(qh):
    while True:
        qh.query_backend()
        inv = qh.get_inventory()
        status = verify_inv(inv)
        if status['need_rope']:
            rope_box = osrs.server.get_surrounding_game_objects(7, ['40965'])
            if rope_box and '40965' in rope_box:
                osrs.move.move_and_click(rope_box['40965']['x'], rope_box['40965']['y'], 2, 2)
                start_time = datetime.datetime.now()
                while True:
                    inv = osrs.inv.get_inv()
                    rope = osrs.inv.is_item_in_inventory_v2(inv, '954')
                    if rope or (datetime.datetime.now() - start_time).total_seconds() > 3:
                        break
        elif status['need_buckets']:
            while True:
                bucket_box = osrs.server.get_surrounding_game_objects(7, ['40966'])
                if bucket_box and '40966' in bucket_box:
                    osrs.move.move_and_click(bucket_box['40966']['x'], bucket_box['40966']['y'], 2, 2)
                    start_time = datetime.datetime.now()
                    found = False
                    while True:
                        inv = osrs.inv.get_inv()
                        water_bucket_quantity = osrs.inv.get_item_quantity_in_inv(inv, 1929)
                        empty_bucket_quantity = osrs.inv.get_item_quantity_in_inv(inv, 1925)
                        if water_bucket_quantity + empty_bucket_quantity >= 3:
                            return
                        elif (datetime.datetime.now() - start_time).total_seconds() > 1:
                            break
                    if found:
                        break
        elif not status['need_buckets'] and not status['need_rope']:
            return


def fill_buckets():
    while True:
        pump = osrs.server.get_surrounding_game_objects(7, ['41000'])
        if pump and '41000' in pump:
            osrs.move.move_and_click(pump['41000']['x'], pump['41000']['y'], 2, 2)
            start_time = datetime.datetime.now()
            while True:
                inv = osrs.inv.get_inv()
                water_bucket_quantity = osrs.inv.get_item_quantity_in_inv(inv, 1929)
                if (datetime.datetime.now() - start_time). total_seconds() > 3:
                    break
                elif water_bucket_quantity >= 3:
                    return
        else:
            break

# 10571 spirit pool to fish
# 10570 spirit pool closed
# 10569 double fish spot
# 10565 reg fish spot
# 41344/5 totem


def dist_from_start_point(ap, qh):
    if not ap:
        return 999
    curr = qh.get_player_world_location()
    return math.floor(osrs.dev.point_dist(ap['x'], ap['y'], curr['x'], curr['y']))


def run_to_island():
    right_ship_crate = osrs.server.get_surrounding_game_objects(10, ['40971'])
    if right_ship_crate and '40971' in right_ship_crate:
        osrs.move.run_towards_square_v2(
            {
                'x': right_ship_crate['40971']['x_coord'] - 10,
                'y': right_ship_crate['40971']['y_coord'] - 12, ''
                                                               'z': 0
            }
        )
    else:
        left_ship_crate = osrs.server.get_surrounding_game_objects(10, ['40968'])
        if left_ship_crate:
            osrs.move.run_towards_square_v2(
                {
                    'x': left_ship_crate['40968']['x_coord'] + 2,
                    'y': left_ship_crate['40968']['y_coord'] + 20,
                    'z': 0
                }
            )


def kill_tempoross():
    global anchor_point
    global starting_game
    starting_game = True
    anchor_point = None
    # mast 41352
    # mast 41353
    # harpoonfish 25564
    # 40971 is bottom fish crate on right boat 3056,2967,0 -> 3046,2960,0 -10,-7,0
    qh = osrs.queryHelper.QueryHelper()
    while True:
        qh.player_world_location()
        qh.inventory()
        qh.is_fishing()
        qh.query_backend()
        harpoon_fish = osrs.inv.is_item_in_inventory_v2(qh.get_inventory(), '25564')
        dist = dist_from_start_point(anchor_point, qh)
        on_boat = dist < 6
        on_island = dist >= 6
        if starting_game:
            get_supplies(qh)
            fill_buckets()
            anchor_point = osrs.server.get_world_location()
            starting_game = False
            continue
        if not harpoon_fish and on_boat:
            run_to_island()
            continue
        if on_island and len(qh.get_inventory()) < 28 and not qh.get_is_fishing():
            fishing_spots = osrs.server.get_npcs_by_id('10565,10568,10569')
            print(fishing_spots)
            c = osrs.util.find_closest_target(fishing_spots)
            if c:
                print(c)
                osrs.move.fast_move_and_click(c['x'], c['y'], 3, 3)
        # once on island, begin fishing
        # if im not fishing a double spot and one is available, use it
        # look out for an rogue waves
        # once full, run to ship and load cannons
        # if tempoross energy is below 3% , run to spirit pool to fish
        # fish spirit pool if available
        # once game is over, leave arena and exit kill_tempoross function


def main():
    while True:
        loc = osrs.server.get_world_location()
        # Not in game, join boat
        if loc and 3134 < loc['x'] < 3200:
            click_ladder()
            continue
        # waiting for the next game to start
        if loc and 3125 < loc['x'] < 3135:
            continue
        # im in the instance
        elif loc and loc['x'] > 7000:
            kill_tempoross()

main()
