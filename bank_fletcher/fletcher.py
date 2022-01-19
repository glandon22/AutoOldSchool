from osrs_utils import general_utils
from PIL import Image
import keyboard
import pyscreenshot
import numpy as np
# go to bank
# withdraw willow logs
# fletch themleague
# deposit them

def main():
    # click bank
    while True:
        if general_utils.find_fixed_object(np.array(pyscreenshot.grab((0, 0, 2560, 1440))), 0, 0):
            break
        general_utils.random_sleep(3, 3.1)
    interface = general_utils.wait_for_bank_interface((0, 2560, 0, 1440), 50)
    if interface != 'success':
        return print(interface)
    general_utils.click_inv_slot(1)
    general_utils.random_sleep(0.2, 0.3)
    withdraw = general_utils.withdraw_items_from_bank(['willows_in_bank.png'], (0, 2560, 0, 1440))
    if withdraw != 'success':
        return print(withdraw)
    general_utils.random_sleep(0.1, 0.2)
    keyboard.send('esc')
    general_utils.random_sleep(0.2,0.3)
    process = general_utils.process_with_tool(1, '3', '..\\screens\\willow_long_bag.png', 100)
    if process != 'success':
        return print(process)


while True:
    try:
        main()
    except:
        break
