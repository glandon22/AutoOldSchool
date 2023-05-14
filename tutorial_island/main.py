import random
import time

import numpy as np
import pyscreenshot
from autoscape import general_utils
import keyboard
import pyautogui

def type_something(phrase):
    for char in phrase:
        keyboard.send(char)
        general_utils.random_sleep(0.1, 0.2)

def main():
    general_utils.bezier_movement(1200, 1230, 30, 240)
    general_utils.random_sleep(0.1, 0.2)
    pyautogui.click()
    type_something('mr-donut778')
    look_up_name = general_utils.rough_img_compare('..\\screens\\tutorial_island\\create_username.png', .8, (0,0,2560,1440))
    general_utils.bezier_movement(look_up_name[0] + 3, look_up_name[0] + 36, look_up_name[1] + 2, look_up_name[1] + 7)
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click()
    general_utils.random_sleep(0.2, 0.3)
    general_utils.bezier_movement(1250, 1275, 200, 300)
    general_utils.random_sleep(4.5, 5.6)
    is_available = general_utils.rough_img_compare('..\\screens\\tutorial_island\\username_available.png', .8, (0,0,2560,1440))
    if not is_available:
        return 'name not available'
    set_name = general_utils.rough_img_compare('..\\screens\\tutorial_island\\set_name.png', .8, (0, 0, 2560, 1440))
    general_utils.bezier_movement(set_name[0] + 3, set_name[0] + 36, set_name[1] + 2, set_name[1] + 7)
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click()
    general_utils.random_sleep(4.5, 6.1)


def main1():
    arrow_locs = [
        [992, 1024, 496, 510],
        [994, 1024, 541, 556],
        [994, 1026, 584, 600],
        [994, 1026, 630, 645],
        [994, 1026, 675, 690],
        [994, 1026, 720, 735],
        [994, 1026, 765, 780],
        [1386, 1420, 494, 510],
        [1386, 1420, 540, 545],
        [1386, 1420, 585, 590],
        [1386, 1420, 630, 635],
        [1386, 1420, 675, 680]
    ]
    for loc in arrow_locs:
        general_utils.bezier_movement(loc[0], loc[1], loc[2], loc[3])
        for i in range(0, random.randint(1, 5)):
            general_utils.random_sleep(0.4, 0.5)
            pyautogui.click()
    general_utils.bezier_movement(1102, 1186, 761, 776)
    general_utils.random_sleep(0.2, 0.4)
    pyautogui.click()

def main2():
    pyautogui.scroll(random.randint(-9000, -7060))

def main3():
    while True:
        general_utils.find_moving_target_no_verify(np.array(pyscreenshot.grab()))
        general_utils.random_sleep(2.1, 2.5)
        guide = general_utils.rough_img_compare('..\\screens\\tutorial_island\\gielinor_guide.png', .8, ())
        if guide:
            break
    for i in range(1,6 ):
        keyboard.send('space')
        general_utils.random_sleep(0.9, 1.1)
    keyboard.send('1')
    for i in range(3):
        general_utils.random_sleep(0.4, 0.6)
        keyboard.send('space')
    general_utils.random_sleep(0.4, 0.6)
    general_utils.bezier_movement(2449, 2466, 1357, 1377)
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click()
    while True:
        general_utils.find_moving_target_no_verify(np.array(pyscreenshot.grab()))
        general_utils.random_sleep(2.1, 2.5)
        guide = general_utils.rough_img_compare('..\\screens\\tutorial_island\\gielinor_guide.png', .8, ())
        if guide:
            break

    for i in range(2):
        keyboard.send('space')
        general_utils.random_sleep(0.9, 1.1)

    general_utils.find_fixed_object(np.array(pyscreenshot.grab()), 0, 0)
    general_utils.bezier_movement(2446, 2466, 214, 220)
    general_utils.random_sleep(0.1, 0.2)
    pyautogui.click()
    general_utils.change_npc_highlights('survival expert')
    while True:
        general_utils.find_moving_target_no_verify(np.array(pyscreenshot.grab()))
        general_utils.random_sleep(2.1, 2.5)
        survival = general_utils.rough_img_compare('..\\screens\\tutorial_island\\survival.png', .8, ())
        if survival:
            break
    keyboard.send('space')
    general_utils.bezier_movement(2162, 2178, 1356, 1376)
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click()
    general_utils.change_npc_highlights('fishing spot')
    general_utils.change_fishing_settings()
    general_utils.find_moving_target_no_verify(np.array(pyscreenshot.grab()))
    while True:
        shrimp = general_utils.rough_img_compare('..\\screens\\tutorial_island\\shrimp.png', .8, ())
        if shrimp:
            break
    general_utils.change_npc_highlights('survival expert')
    general_utils.bezier_movement(2076, 2092, 1355, 1374)
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click()

    while True:
        general_utils.find_moving_target_no_verify(np.array(pyscreenshot.grab()))
        general_utils.random_sleep(2.1, 2.5)
        caught = general_utils.rough_img_compare('..\\screens\\tutorial_island\\caught_shrimp.png', .8, ())
        if caught:
            break
    for i in range(3):
        keyboard.send('space')
        general_utils.random_sleep(0.9, 1.1)

    general_utils.find_fixed_object(np.array(pyscreenshot.grab()),0,0)
    log_loc = None
    while True:
        logs = general_utils.rough_img_compare('..\\screens\\tutorial_island\\logs.png', .8, ())
        if logs:
            log_loc = logs
            break
        general_utils.random_sleep(1.0, 1.1)

    tind = general_utils.rough_img_compare('..\\screens\\tutorial_island\\tinderbox.png', .8, ())
    if not tind:
        print('no tinderbox')
    general_utils.bezier_movement(tind[0] + 1, tind[0] + 5, tind[1] + 2, tind[1] + 7)
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click()

    logs_bag = general_utils.rough_img_compare('..\\screens\\tutorial_island\\logs_in_bag.png', .8, ())
    if not logs_bag:
        print('no logs_bag')
    general_utils.bezier_movement(logs_bag[0] + 1, logs_bag[0] + 5, logs_bag[1] + 2, logs_bag[1] + 7)
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click()
    general_utils.random_sleep(3.2, 3.3)

    general_utils.find_fixed_object(np.array(pyscreenshot.grab()), 0, 0)
    shrimp = general_utils.rough_img_compare('..\\screens\\tutorial_island\\shrimp_bag.png', .8, ())
    if not shrimp:
        print('no logs_bag')
    general_utils.bezier_movement(shrimp[0] + 1, shrimp[0] + 5, shrimp[1] + 2, shrimp[1] + 7)
    general_utils.random_sleep(0.4, 0.5)
    pyautogui.click()
    general_utils.bezier_movement(1279, 1281, 719, 721)
    general_utils.random_sleep(0.1, 0.2)
    pyautogui.click()
general_utils.find_fixed_object(np.array(pyscreenshot.grab()), 0, 0)