from osrs_utils import general_utils
import pyscreenshot
import numpy as np
import pyautogui
import keyboard
from PIL import Image


def main():
    while True:
        if general_utils.calc_img_diff(
            pyscreenshot.grab(general_utils.show_inv_coords(0)),
            Image.open('..\\screens\\empty_bag\\slot0.png'),
            1
        ) == 'same':
            return print('all done making arrows')
        general_utils.bezier_movement(2317, 2343, 1030, 1056)
        general_utils.random_sleep(0.2, 0.3)
        pyautogui.click()
        general_utils.random_sleep(0.2, 0.3)
        general_utils.bezier_movement(2371, 2395, 1034, 1058)
        general_utils.random_sleep(0.2, 0.3)
        pyautogui.click()
        general_utils.random_sleep(0.7,0.8)
        keyboard.send('1')
        general_utils.bezier_movement(3750, 3800, 500, 700)
        while True:
            prev_val = pyscreenshot.grab((2364, 1021, 2396, 1062))
            general_utils.random_sleep(1.5,1.6)
            if general_utils.calc_img_diff(prev_val, pyscreenshot.grab((2364, 1021, 2396, 1062)), 1) == 'same':
                break


main()
