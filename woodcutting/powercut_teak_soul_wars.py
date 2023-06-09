import datetime


import osrs

wc_animations = [
    879,877,875,873,871,869,867,8303,2846,24,2117,7264,8324,8778
]
# reg logs 1511
# oak log 1521
# willow 1519
# teak 6333
expected_logs = 6333
#reg trees
# oak tree 10820
# teak
expected_tree = '40758'
port = '56799'

tiles = [
    '2185,2990,0',
    '2185,2988,0',
    '2187,2992,0'
]


def main():
    last_click = datetime.datetime.now()
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 51, 57, 456, 578, 'pass_70', False)
        animation = osrs.server.get_player_animation(port)
        inv = osrs.inv.get_inv(port)
        if animation in wc_animations:
            print('currently woodcutting.')
            osrs.clock.random_sleep(0.6, 0.7)
        elif len(inv) == 28:
            osrs.inv.power_drop(inv, [], [expected_logs])
        elif (datetime.datetime.now() - last_click).total_seconds() > 5:
            lookup = []
            for tile in tiles:
                lookup.append({
                    'tile': tile,
                    'object': expected_tree
                })
            tree = osrs.server.get_game_objects(lookup, port)
            if expected_tree in tree:
                osrs.move.move_and_click(tree[expected_tree]['x'], tree[expected_tree]['y'], 2, 2)
                last_click = datetime.datetime.now()
                osrs.clock.random_sleep(0.5, 1.6)
                osrs.move.click_off_screen(300, 1200, 400, 900, False)



main()