import datetime

from osrs_utils import general_utils
fruits = [
    1955,
    1963,
    5504,
    247,
    2102,
    1951,
    2114,
    2120,
    464,
    19653,
    5972
]
port = '56799'

def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 53, 58, 423, 551, 'julenth', False)
        inv = general_utils.get_inv(port)
        fruit_inv = general_utils.are_items_in_inventory_v2(inv, fruits)
        if fruit_inv:
            general_utils.power_drop(inv, [], fruits)
        stall = general_utils.get_game_object('1801,3608,0', '28823', port)
        if stall:
            general_utils.move_and_click(stall['x'], stall['y'], 9, 9)
            general_utils.random_sleep(1.0, 1.4)

main()