import datetime

from autoscape import general_utils
port = '56799'
objs = [
    '28498',
    '28497',
    '28496',
]

sulf = 13571
def click_sulfur():
    for obj in objs:
        exists = general_utils.get_game_object('1424,3873,0', obj, port)
        if exists:
            general_utils.move_and_click(exists['x'], exists['y'], 3, 3)
            return True


def main():
    prev_inv = general_utils.get_inv(port)
    last_change = datetime.datetime.now()
    while True:
        inv = general_utils.get_inv(port)
        if inv != prev_inv:
            prev_inv = inv
            last_change = datetime.datetime.now()
        elif (datetime.datetime.now() - last_change).total_seconds() > 10:
            res = click_sulfur()
            if res:
                prev_inv = inv
                last_change = datetime.datetime.now()
            else:
                general_utils.power_drop(inv, [], [sulf])
        elif len(inv) == 28:
            general_utils.power_drop(inv, [], [sulf])


main()
