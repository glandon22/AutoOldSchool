import osrs
KNIFE_ID = 946
FISH_TO_CUT = [
    22826, # bluegill
    22829 # common tench
]


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.inventory()
    qh.player_world_location()
    qh.projectiles()
    qh.npcs(['8523'])
    while True:
        qh.query_backend()
        fishing_spots = qh.get_npcs()
        curr_loc = qh.get_player_world_location()
        '''if curr_loc and (curr_loc['x'] != 1376 or curr_loc['y'] != 3629):
            osrs.move.run_towards_square_v2({'x': 1376, 'y': 3629, 'z': 0})'''
        if len(qh.get_inventory()) == 28:
            knife = osrs.inv.is_item_in_inventory_v2(qh.get_inventory(), KNIFE_ID)
            if not knife:
                exit('no knife in inv')
            for item in qh.get_inventory():
                if item['id'] in FISH_TO_CUT:
                    osrs.move.move_and_click(knife['x'], knife['y'], 3, 3)
                    osrs.move.move_and_click(item['x'], item['y'], 3, 3)
            osrs.clock.sleep_one_tick()
        # fishing spots are available and my bird is not flying
        if fishing_spots and len(qh.get_projectiles()) == 0:
            c = osrs.util.find_closest_target(fishing_spots)
            if c and 'x' in c and 'y' in c:
                osrs.move.move_and_click(c['x'], c['y'], 3, 3)
                osrs.clock.sleep_one_tick()
                continue


main()
