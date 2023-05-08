import datetime

from osrs_utils import general_utils
import random
from pynput import keyboard


paused = False


def print_key(*key):
    global paused
    if key[0] == keyboard.KeyCode.from_char('d'):
        print('flipped', key)
        paused = not paused
        print('Script paused: {}. Sleeping for 10 seconds.'.format(paused))
        general_utils.random_sleep(10, 10.1)


listener = keyboard.Listener(on_press=print_key)
listener.start()


def get_more_wine():
    print('getting more wine.')
    general_utils.random_sleep(5, 6)
    banker = general_utils.get_npc_by_id('1613', '56799')
    if banker:
        general_utils.move_and_click(banker['x'], banker['y'], 3, 3)
        general_utils.random_sleep(3, 4)
        bank_data = general_utils.get_bank_data()
        if bank_data:
            wine = general_utils.is_item_in_inventory_v2(bank_data, 1993)
            if wine:
                inv = general_utils.get_inv()
                if inv:
                    empty_jugs = general_utils.is_item_in_inventory_v2(inv, 1935)
                    if empty_jugs:
                        general_utils.right_click_menu_select(empty_jugs, False, '56799', 'Jug', 'Deposit-All')
                        general_utils.sleep_one_tick()
                        general_utils.right_click_menu_select(wine, False, '56799', 'Jug of wine', 'Withdraw-All')
                        general_utils.sleep_one_tick()
                        general_utils.press_key('esc')


def climb_down_ladder():
    ladder = general_utils.get_game_object('2650,3286,1', '16679')
    if ladder:
        general_utils.move_and_click(ladder['x'], ladder['y'], 3, 3)
        general_utils.random_sleep(2, 3)


def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 43, 48, 423, 551, 'julenth', False)
        if paused:
            continue

        hp = general_utils.get_skill_data('hitpoints')
        inv = general_utils.get_inv()
        wine = general_utils.is_item_in_inventory_v2(inv, 1993)
        loc = general_utils.get_world_location()
        if loc and 'z' in loc and loc['z'] > 0:
            print('upstairs, climbing down ladder.')
            climb_down_ladder()
        if not wine:
            print('out of wine.')
            get_more_wine()
            continue
        if hp and 'boostedLevel' and hp['boostedLevel'] < 10 and wine:
            print('drinking wine.')
            general_utils.move_and_click(wine['x'], wine['y'], 3, 3)
            continue
        sacks = general_utils.is_item_in_inventory_v2(inv, 22531)
        if sacks and sacks['quantity'] >= 27:
            print('open loot sacks.')
            general_utils.move_and_click(sacks['x'], sacks['y'], 3, 3)
            continue
        clicks = random.randint(1, 5)
        for i in range(clicks):
            print('getting knight loc.')
            knight = general_utils.get_npc_by_id('3297', '56799')
            if knight:
                print('clicking knight: {}'.format(knight))
                general_utils.move_and_click(knight['x'], knight['y'], 4, 4)


main()
