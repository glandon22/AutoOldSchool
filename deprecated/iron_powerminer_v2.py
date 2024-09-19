import datetime


import osrs

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
        rock = osrs.server.get_game_object(tile, iron_rock, port)
        if rock:
            osrs.move.move_and_click(rock['x'], rock['y'], 4, 4)
            osrs.move.click_off_screen(1500, 1700, 800, 1000, False)
            break


def dump_iron():
    inv = osrs.inv.get_inv(port)
    osrs.inv.power_drop(inv, [], [iron_ore_id])


def wait_for_ore():
    start_time = datetime.datetime.now()
    while True:
        inv = osrs.inv.get_inv(port)
        ore = osrs.inv.is_item_in_inventory_v2(inv, iron_ore_id)
        if ore:
            dump_iron()
            break
        elif (datetime.datetime.now() - start_time).total_seconds() > 10:
            #something is wrong, re mine rock
            break


script_config = {
    'intensity': 'high',
    'login': lambda: osrs.clock.random_sleep(4, 5),
    'logout': lambda: osrs.clock.random_sleep(11, 14),
}


def main():
    start_time = datetime.datetime.now()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        if len(qh.get_inventory()) == 28:
            exit('full inv')
        else:
            print(len(qh.get_inventory()))
        qh.query_backend()
        osrs.game.break_manager_v4(script_config)
        mine()
        wait_for_ore()

main()