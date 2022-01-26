"""
cook whatever is in the first bank slot at rogues den
"""
import random
import time

import numpy as np
import pyautogui
import pyscreenshot
from PIL import Image, ImageGrab
import keyboard as kb
from osrs_utils import general_utils
import datetime


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


def main(fish):
    while True:
        find_bank = general_utils.find_fixed_npc([0, 0, 2560, 1440], 0, 0)
        if not find_bank:
            return print('couldn\'t find the bank')
        bank = general_utils.wait_for_bank_interface([794, 1455, 90, 1126], 60)
        if bank != 'success':
            return print(bank)
        general_utils.random_sleep(0.2, 0.3)
        general_utils.dump_bag()
        general_utils.random_sleep(0.4, 0.5)
        withdraw = general_utils.withdraw_items_from_bank(fish, [794, 1455, 90, 1126])
        if withdraw != 'success':
            return print(withdraw)
        general_utils.random_sleep(0.2, 0.3)
        kb.send('esc')
        general_utils.random_sleep(0.2, 0.3)
        inv_slot = general_utils.show_inv_coords(0)
        general_utils.bezier_movement(inv_slot[0], inv_slot[2], inv_slot[1], inv_slot[3])
        general_utils.random_sleep(0.1, 0.2)
        pyautogui.click()
        general_utils.random_sleep(0.2, 0.3)
        fire = general_utils.find_fixed_object(np.array(pyscreenshot.grab((400, 0, 2096, 966))), 400, 0)
        if not fire:
            return print('couldnt find the fire')
        general_utils.random_sleep(1.1, 1.8)
        kb.send('space')
        general_utils.bezier_movement(3500, 3600, 300, 400)
        general_utils.random_sleep(0.1, 0.2)
        pyautogui.click()
        start_time = datetime.datetime.now()
        while True:
            if general_utils.did_level():
                general_utils.antiban_rest()
                break
            elif (datetime.datetime.now() - start_time).seconds > 71:
                general_utils.antiban_rest()
                break
            general_utils.random_sleep(1.0, 1.2)


main(['tuna_in_bank.png'])
