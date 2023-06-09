import datetime

import keyboard


import osrs

port = '56799'
widget = '312,29'
#  2347 hammer
# widget - dart tips - 312,29
# widget - bolts - 312,34
bar = 2359
# 2351 # iron
#2359  # mith
# 2353 steel
def bank():
    booth = osrs.server.get_game_object('3186,3436,0', '34810', port)
    osrs.move.move_and_click(booth['x'], booth['y'], 3, 3)
    osrs.bank.wait_for_bank_interface(port)
    while True:
        found_additional_items = False
        inv = osrs.inv.get_inv(port)
        for item in inv:
            if item['id'] != 2347:
                found_additional_items = True
                osrs.move.move_and_click(item['x'], item['y'], 3, 3)
                osrs.clock.random_sleep(0.5, 0.6)
                break
        if not found_additional_items:
            break
    bank_data = osrs.bank.get_bank_data(port)
    bar_in_bank = osrs.inv.is_item_in_inventory_v2(bank_data, bar)
    if not bar_in_bank:
        exit('no more bars')
    osrs.move.move_and_click(bar_in_bank['x'], bar_in_bank['y'], 4, 4)
    osrs.clock.random_sleep(0.5, 0.6)
    keyboard.send('esc')
    osrs.clock.random_sleep(0.5, 0.6)


def go_to_anvil():
    anvil = osrs.server.get_game_object('3188,3426,0', '2097', port)
    osrs.move.move_and_click(anvil['x'], anvil['y'], 4, 2)
    while True:
        anvil_interface = osrs.server.get_widget('312,0', port)
        if anvil_interface:
            osrs.clock.random_sleep(0.5, 0.6)
            break


def smith_item():
    item = osrs.server.get_widget(widget, port)
    osrs.move.move_and_click(item['x'], item['y'], 4, 4)
    osrs.clock.random_sleep(0.5, 0.6)


def post_login():
    inv = osrs.inv.get_inv(port)
    bar_in_inv = osrs.inv.is_item_in_inventory_v2(inv, bar)
    if not bar_in_inv:
        osrs.clock.random_sleep(0.6, 1.4)
        print('out of bars, getting more.')
        bank()
    go_to_anvil()
    smith_item()
    osrs.move.click_off_screen(200, 1100, 300, 800, False)


def main():
    # 2349  # bronze
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 51, 57, 453, 609, 'pass_70', post_login)
        inv = osrs.inv.get_inv(port)
        bar_in_inv = osrs.inv.is_item_in_inventory_v2(inv, bar)
        if not bar_in_inv:
            osrs.clock.random_sleep(0.6, 1.4)
            print('out of bars, getting more.')
            bank()
            go_to_anvil()
            smith_item()
            osrs.move.click_off_screen(200, 1100, 300, 800, False)
        leveled_up = osrs.server.get_widget('233,0', port)
        if leveled_up:
            osrs.clock.random_sleep(0.8, 1.9)
            print('leveled up.')
            go_to_anvil()
            smith_item()
            osrs.move.click_off_screen(200, 1100, 300, 800, False)

main()

