import datetime


import osrs

wc_animations = [
    879,877,875,873,871,869,867,8303,2846,24,2117,7264,8324,8778
]
# reg logs 1511
# oak log 1521
expected_logs = 1511
#reg trees
# oak tree 10820
# teak
expected_tree = '1276'
port = '56800'

tiles = [
    '3190,3218,0',
    '3188,3219,0',
    '3186,3221,0',
    '3189,3224,0',
    '3192,3224,0',
    '3195,3220,0',
    '3193,3218,0'
]


def main():
    last_click = datetime.datetime.now()
    while True:
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
            tree = osrs.server.get_game_objects(lookup, '56800')
            if expected_tree in tree:
                osrs.move.move_and_click(tree[expected_tree]['x'], tree[expected_tree]['y'], 2, 2)
                last_click = datetime.datetime.now()



main()