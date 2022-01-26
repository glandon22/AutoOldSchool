# click martin
# wait for store interface
# sell bows
# exit interface
# hop worlds
import keyboard
import pyscreenshot
import numpy as np
from osrs_utils import general_utils
import pyautogui

def sell():
    while True:
        screen = pyscreenshot.grab((200, 100, 2300, 1300))
        general_utils.find_moving_target(np.array(screen), False, 200, 100)
        general_utils.wait_until_stationary()
        store = general_utils.rough_img_compare('..\\screens\\martin_shop_interface.png', .8, (200, 100, 2300, 1300))
        if store:
            break
    click = general_utils.show_inv_coords(0)
    general_utils.bezier_movement(click[0], click[2], click[1], click[3])
    pyautogui.click(button='right')
    general_utils.random_sleep(0.1, 0.2)
    sell = general_utils.rough_img_compare('..\\screens\\sell50.png', .9, (0, 0, 2560, 1440))
    if not sell:
        return print('no sell')
    general_utils.bezier_movement(sell[0] - 3, sell[0] + 3, sell[1] - 3, sell[1] + 3)
    pyautogui.click()
    general_utils.random_sleep(0.3, 0.4)
    keyboard.send('esc')
    general_utils.random_sleep(0.3, 0.4)
    general_utils.hop_worlds()

while True:
    try:
        sell()
    except:
        break