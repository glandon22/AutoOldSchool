import datetime


import osrs
tea = 1978
port = '56799'
def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 53, 58, 423, 551, 'julenth', False)
        inv = osrs.inv.get_inv(port)
        tea_inv = osrs.inv.is_item_in_inventory_v2(inv, tea)
        if tea_inv:
            osrs.inv.power_drop(inv, [], [tea])
        stall = osrs.server.get_game_object('3269,3410,0', '635', port)
        if stall:
            osrs.move.move_and_click(stall['x'], stall['y'], 9, 9)
            osrs.clock.random_sleep(1.0, 1.4)

osrs.clock.random_sleep(1, 2)
main()