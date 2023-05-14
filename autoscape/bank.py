import pyautogui
from pynput.keyboard import Key

import move
import general_utils
import inv

def solve_bank_pin():
    for i in range(4):
        num = None
        if i == 0 or i == 3:
            num = '8'
        else:
            num = '7'

        loc = general_utils.rough_img_compare('..\\screens\\bank_pin_' + num + '.png', .8, [641, 306, 1648, 1008])
        if loc:
            move.bezier_movement(loc[0], loc[0] + 1, loc[1], loc[1] + 1)
            general_utils.random_sleep(0.2, 0.3)
            pyautogui.click()
            general_utils.random_sleep(0.2, 0.3)
            move.bezier_movement(1200, 1700, 12, 209)
        else:
            return 'couldnt find ' + num
        general_utils.random_sleep(1.1, 1.2)


def dump_items_in_bank():
    # wait for interface and withdraw item
    while True:
        loc = general_utils.rough_img_compare('..\\screens\\bank_interface.png', .9, (0, 0, 1920, 1080))
        if loc:
            loc = general_utils.rough_img_compare('..\\screens\\dump.png', .9, (0, 0, 1920, 1080))
            move.move_and_click(loc[0] + 15, loc[1] + 15, 4, 4)
            general_utils.random_sleep(.5, .6)
            general_utils.keyboard.press(Key.esc)
            general_utils.keyboard.release(Key.esc)
            general_utils.random_sleep(.5, .6)
            break


def get_bank_data(port='56799'):
    q = {
        'bank': True
    }
    while True:
        data = general_utils.query_game_data(q, port)
        if 'bankItems' in data:
            return data['bankItems']

def deposit_box_dump_inv():
    q = {
        'widget': '192,5'
    }
    # wait to first see the button,
    # since there is a lag from its first appearance
    # to actually being on screen in the correct location
    while True:
        data = general_utils.query_game_data(q)
        if 'widget' in data:
            break
    general_utils.random_sleep(0.5, 0.61)
    while True:
        data = general_utils.query_game_data(q)
        if 'widget' in data:
            move.move_and_click(data['widget']['x'], data['widget']['y'], 6, 6)
            break
    general_utils.keyboard.press(Key.esc)
    general_utils.keyboard.release(Key.esc)


def deposit_all_of_x(items, port='56799'):
    while True:
        found_additional_items = False
        curr_inv = inv.get_inv(port)
        for item in curr_inv:
            if item['id'] in items:
                found_additional_items = True
                move.move_and_click(item['x'], item['y'], 3, 3)
                general_utils.random_sleep(0.5, 0.6)
                break
        if not found_additional_items:
            break
    general_utils.random_sleep(0.5, 0.6)


def deposit_all_but_x_in_bank(items, port='56799'):
    while True:
        found_additional_items = False
        curr_inv = inv.get_inv(port)
        for item in curr_inv:
            if item['id'] not in items:
                found_additional_items = True
                move.move_and_click(item['x'], item['y'], 3, 3)
                general_utils.random_sleep(0.5, 0.6)
                break
        if not found_additional_items:
            break
    general_utils.random_sleep(0.5, 0.6)