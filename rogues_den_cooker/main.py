"""
cook whatever is in the first bank slot at rogues den
"""
import random
import pyautogui
from PIL import Image, ImageGrab
import keyboard as kb
from osrs_utils import general_utils


def continue_cooking():
    inv_slot = general_utils.show_inv_coords(27)
    general_utils.bezier_movement(inv_slot[0], inv_slot[1], inv_slot[2], inv_slot[3])
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click()
    general_utils.random_sleep(0.2, 0.3)
    fire = general_utils.find_fixed_object([400, 0, 2096, 966], 400, 0)
    if not fire:
        return print('couldnt find the fire')
    general_utils.random_sleep(0.6, 0.8)
    kb.send('space')
    return 'success'


def main():
    while True:
        find_bank = general_utils.find_fixed_npc([400, 0, 2096, 966], 400, 0)
        if not find_bank:
            return print('couldn\'t find the bank')
        bank = general_utils.wait_for_bank_interface([794, 1455, 90, 1126], 60)
        if bank != 'success':
            return print(bank)
        general_utils.random_sleep(0.2, 0.3)
        general_utils.dump_bag()
        general_utils.random_sleep(0.4, 0.5)
        withdraw = general_utils.withdraw_items_from_bank(['seaweed_in_bank.png'], [794, 1455, 90, 1126])
        if withdraw != 'success':
            return print(withdraw)
        general_utils.random_sleep(0.2, 0.3)
        kb.send('esc')
        general_utils.random_sleep(0.2, 0.3)
        inv_slot = general_utils.show_inv_coords(random.randint(0, 27))
        general_utils.bezier_movement(inv_slot[0], inv_slot[1], inv_slot[2], inv_slot[3])
        general_utils.random_sleep(0.1, 0.2)
        pyautogui.click()
        general_utils.random_sleep(0.2, 0.3)
        fire = general_utils.find_fixed_object([400, 0, 2096, 966], 400, 0)
        if not fire:
            return print('couldnt find the fire')
        general_utils.random_sleep(1.1, 1.8)
        kb.send('space')
        cycles_waiting = 0
        expected_last_slot = Image.open('..\\screens\\soda_in_bag.png')
        while True:
            last_slot = general_utils.calc_img_diff(expected_last_slot, ImageGrab.grab([2476, 1304, 2500, 1324]), 3)
            if last_slot == 'same':
                break
            elif general_utils.did_level():
                restart = continue_cooking()
                if restart != 'success':
                    return 'after leveling, did not successfully finish processing'
            elif cycles_waiting > 180:
                return 'did not finishing processing in acceptable number of cycles'
            else:
                cycles_waiting += 1
            general_utils.random_sleep(1.0, 1.2)
        if random.randint(0, 10) == 1:
            general_utils.random_sleep(10.5, 14.9)
        elif random.randint(0, 25) == 1:
            general_utils.random_sleep(33.5, 34.9)


main()
