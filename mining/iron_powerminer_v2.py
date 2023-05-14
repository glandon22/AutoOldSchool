import datetime

from autoscape import general_utils

rock_tiles = [
    '2195,2792,0',
    '2196,2793,0',
    '2197,2792,0'
]
port = '56799'
iron_rock = '11364'
iron_ore_id = 440


def mine():
    for tile in rock_tiles:
        rock = general_utils.get_game_object(tile, iron_rock, port)
        if rock:
            general_utils.move_and_click(rock['x'], rock['y'], 4, 4)
            general_utils.click_off_screen(1500, 1700, 800, 1000, False)
            break


def dump_iron():
    inv = general_utils.get_inv(port)
    general_utils.power_drop(inv, [], [iron_ore_id])


def wait_for_ore():
    start_time = datetime.datetime.now()
    while True:
        inv = general_utils.get_inv(port)
        ore = general_utils.is_item_in_inventory_v2(inv, iron_ore_id)
        if ore:
            dump_iron()
            break
        elif (datetime.datetime.now() - start_time).total_seconds() > 10:
            #something is wrong, re mine rock
            break

def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 49, 52, 432, 673, 'julenth')
        mine()
        wait_for_ore()

main()