import datetime

from autoscape import general_utils

wc_animations = [
    879,877,875,873,871,869,867,8303,2846,24,2117,7264,8324,8778
]
# reg logs 1511
# oak log 1521
expected_logs = 1521
#reg trees
# oak tree 10820
# teak
expected_tree = '10820'
port = '56799'

tiles = [
    '3107,3283,0',
    '3102,3287,0',
    '3097,3288,0'
]


def main():
    last_click = datetime.datetime.now()
    while True:
        animation = general_utils.get_player_animation(port)
        inv = general_utils.get_inv(port)
        if animation in wc_animations:
            print('currently woodcutting.')
            general_utils.random_sleep(0.6, 0.7)
        elif len(inv) == 28:
            general_utils.power_drop(inv, [], [expected_logs])
        elif (datetime.datetime.now() - last_click).total_seconds() > 5:
            lookup = []
            for tile in tiles:
                lookup.append({
                    'tile': tile,
                    'object': expected_tree
                })
            tree = general_utils.get_game_objects(lookup, port)
            if expected_tree in tree:
                general_utils.move_and_click(tree[expected_tree]['x'], tree[expected_tree]['y'], 2, 2)
                last_click = datetime.datetime.now()
                general_utils.click_off_screen(300, 1200, 400, 900, False)



main()