import datetime

import pyautogui

import osrs

import osrs
import random
from pynput import keyboard


paused = False
world_list = [302, 376, 378]

def print_key(*key):
    global paused
    if key[0] == keyboard.KeyCode.from_char('/'):
        print('flipped', key)
        paused = not paused
        print('Script paused: {}. Sleeping for 10 seconds.'.format(paused))
        osrs.clock.random_sleep(10, 10.1)


listener = keyboard.Listener(on_press=print_key)
listener.start()


def get_more_wine():
    print('getting more wine.')
    osrs.clock.random_sleep(5, 6)
    banker = osrs.server.get_npc_by_id('1613', '56799')
    if banker:
        osrs.move.move_and_click(banker['x'], banker['y'], 3, 3)
        osrs.clock.random_sleep(3, 4)
        bank_data = osrs.bank.get_bank_data()
        if bank_data:
            wine = osrs.inv.is_item_in_inventory_v2(bank_data, 1993)
            if wine:
                inv = osrs.inv.get_inv()
                if inv:
                    empty_jugs = osrs.inv.is_item_in_inventory_v2(inv, 1935)
                    if empty_jugs:
                        osrs.move.right_click_menu_select(empty_jugs, False, '56799', 'Jug', 'Deposit-All')
                        osrs.clock.sleep_one_tick()
                    osrs.move.right_click_menu_select(wine, False, '56799', 'Jug of wine', 'Withdraw-All')
                    osrs.clock.sleep_one_tick()
                    new_inv = osrs.inv.get_inv()
                    sacks = osrs.inv.is_item_in_inventory_v2(new_inv, 22531)
                    if not sacks:
                        wine_in_inv = osrs.inv.is_item_in_inventory_v2(new_inv, 1993)
                        if wine_in_inv:
                            osrs.move.right_click_menu_select(wine_in_inv, False, '56799', 'Jug of wine', 'Deposit-1')
                    osrs.keeb.press_key('esc')


def climb_down_ladder():
    ladder = osrs.server.get_game_object('2650,3286,1', '16679')
    if ladder:
        osrs.move.move_and_click(ladder['x'], ladder['y'], 3, 3)
        osrs.clock.random_sleep(2, 3)


def climb_down_second_ladder():
    ladder = osrs.server.get_game_object('2649,3286,2', '16685')
    if ladder:
        osrs.move.move_and_click(ladder['x'], ladder['y'], 3, 3)
        osrs.clock.random_sleep(2, 3)


def steal_knight():
    clicks = random.randint(1, 5)
    # accidentally clicked bank, close interface
    bank_interface = osrs.bank.get_bank_data()
    inv = osrs.inv.get_inv()
    if len(bank_interface) > 0:
        osrs.keeb.press_key('esc')
    # I can't pickpocket because my bag is full of wine and jugs
    if len(inv) == 28 and not osrs.inv.is_item_in_inventory_v2(inv, 22531):
        jug = osrs.inv.is_item_in_inventory_v2(inv, 1935)
        if jug:
            osrs.move.right_click_menu_select(jug, False, '56799', 'Jug', 'Drop')
        else:
            wine = osrs.inv.is_item_in_inventory_v2(inv, 1993)
            if wine:
                osrs.move.right_click_menu_select(wine, False, '56799', 'Jug of wine', 'Drop')
    for i in range(clicks):
        print('getting knight loc.')
        knight = osrs.server.get_npcs_by_id('3297,11936', '56799')
        if knight:
            closest = osrs.util.find_closest_npc(knight)
            print('clicking knight: {}'.format(closest))
            osrs.move.move_and_click(closest['x'], closest['y'], 4, 4)


def main():
    start_time = datetime.datetime.now()
    curr_world = 0
    while True:
        start_time = osrs.game.break_manager(start_time, 43, 48, 423, 551, 'julenth', False)
        if paused:
            continue

        hp = osrs.server.get_skill_data('hitpoints')
        inv = osrs.inv.get_inv()
        wine = osrs.inv.is_item_in_inventory_v2(inv, 1993)
        loc = osrs.server.get_world_location()
        if loc and 'z' in loc and loc['z'] == 1:
            print('upstairs, climbing down ladder.')
            climb_down_ladder()
            continue
        if loc and 'z' in loc and loc['z'] == 2:
            print('upstairs, climbing down ladder.')
            climb_down_second_ladder()
            continue
        if not wine:
            print('out of wine.')
            get_more_wine()
            continue
        if hp and 'boostedLevel' and hp['boostedLevel'] < 10 and wine:
            print('drinking wine.')
            osrs.move.move_and_click(wine['x'], wine['y'], 3, 3)
            continue
        sacks = osrs.inv.is_item_in_inventory_v2(inv, 22531)
        if sacks and sacks['quantity'] >= 27:
            print('open loot sacks.')
            osrs.move.move_and_click(sacks['x'], sacks['y'], 3, 3)
            continue
        steal_knight()


main()
