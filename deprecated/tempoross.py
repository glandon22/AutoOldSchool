
import osrs


port = '56800'


def board_ship():
    while True:
        ladder = osrs.server.get_game_object('3135,2841,0', '41305', '56800')
        if ladder:
            osrs.move.move_and_click(ladder['x'], ladder['y'], 5, 5)
            break

board_ship()

# totem pole 41355, 3043,2961,0
# shrine to cook is 41236 3036,2956,0