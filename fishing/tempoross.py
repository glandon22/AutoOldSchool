from autoscape import general_utils


port = '56800'


def board_ship():
    while True:
        ladder = general_utils.get_game_object('3135,2841,0', '41305', '56800')
        if ladder:
            general_utils.move_and_click(ladder['x'], ladder['y'], 5, 5)
            general_utils
            break

board_ship()

# totem pole 41355, 3043,2961,0
# shrine to cook is 41236 3036,2956,0