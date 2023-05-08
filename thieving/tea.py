import datetime

from osrs_utils import general_utils
tea = 1978
port = '56799'
def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 53, 58, 423, 551, 'julenth', False)
        inv = general_utils.get_inv(port)
        tea_inv = general_utils.is_item_in_inventory_v2(inv, tea)
        if tea_inv:
            general_utils.power_drop(inv, [], [tea])
        stall = general_utils.get_game_object('3269,3410,0', '635', port)
        if stall:
            general_utils.move_and_click(stall['x'], stall['y'], 9, 9)
            general_utils.random_sleep(1.0, 1.4)

general_utils.random_sleep(1, 2)
main()