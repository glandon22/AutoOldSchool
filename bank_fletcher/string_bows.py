from osrs_utils import general_utils
from PIL import Image
import keyboard
import pyscreenshot
import numpy as np


def string():
    while True:
        general_utils.antiban_rest()
        general_utils.antiban_randoms()
        if general_utils.find_fixed_object(np.array(pyscreenshot.grab((0, 0, 2560, 1440))), 0, 0):
            break
        general_utils.random_sleep(3, 3.1)
    interface = general_utils.wait_for_bank_interface((0, 2560, 0, 1440), 50)
    if interface != 'success':
        return print(interface)
    dump = general_utils.dump_bag()
    if dump != 'success':
        return print(dump)
    general_utils.random_sleep(0.2, 0.3)
    withdraw = general_utils.withdraw_items_from_bank(['bowstring_in_bank.png', 'unstrung_in_bank.png'], (0, 2560, 0, 1440))
    if withdraw != 'success':
        return print(withdraw)
    general_utils.random_sleep(0.1, 0.2)
    keyboard.send('esc')
    general_utils.random_sleep(0.5, 0.6)
    process = general_utils.combine_two_items_14_times('..\\screens\\empty_bag\\slot27.png', 75)
    if process != 'success':
        return print(process)


while True:
    try:
        status = string()
        if status:
            break
    except:
        break
