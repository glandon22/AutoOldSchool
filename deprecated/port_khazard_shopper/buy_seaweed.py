"""
buys sea weed and soda ash from the traders in port khazard
full screen on the 2560x1440 screen
looking due north with view at max altitude
"""
import random
import numpy as np
from PIL import ImageGrab, Image
import cv2
import pyautogui
from osrs_utils import general_utils
import keyboard as kb
import math
import sys

storeInterface = [822, 1422, 427, 790]
bankInterface = [844, 1402, 438, 774]
sodaInStore = [1254, 1276, 606, 616]
seaweedInstore = [1196, 1220, 607, 620]
emptyLastSlot = Image.open('screens/empty_slot.png')
seaweedInBag = [1176, 1199, 558, 576]
sodaInBag = [1177, 1198, 497, 513]

def go_to_bank():
    found = False
    while not found:
        did_i_find = general_utils.find_fixed_object([400, 0, 2096, 966], 400, 0)
        if did_i_find:
            found = True
            general_utils.random_sleep(0.5, 0.7)


def buy_store_items(shop_coords):
    click_coords = general_utils.bezier_movement(shop_coords[0], shop_coords[1], shop_coords[2], shop_coords[3])
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click(button="right")
    general_utils.random_sleep(0.1, 0.2)
    general_utils.bezier_movement(click_coords[0], click_coords[0] + 15, click_coords[1] + 100, click_coords[1] + 108)
    general_utils.random_sleep(0.2, 0.3)
    pyautogui.click()
    general_utils.random_sleep(0.5, 0.7)


def is_bag_full():
    curr_slot = ImageGrab.grab([2474, 1306, 2512, 1330])
    curr_slot.save('.\\screens\\curr_slot.png')

    if general_utils.calc_img_diff(curr_slot, emptyLastSlot, 5) == 'same':
        return False
    else:
        return True


def walk_to_dock():
    general_utils.bezier_movement(1787, 1883, 1320, 1372)
    general_utils.random_sleep(0.1, 0.2)
    general_utils.pyautogui.click()
    general_utils.random_sleep(7.6, 8.3)


def process_img(image, iters):
    if iters > 75:
        print('failed to find traders after 150 iterations, program terminating')
        sys.exit()
    elif iters > 50:
        print('checking to see if we are on the ship')
        curr_map = ImageGrab.grab([2450, 76, 2486, 108])
        curr_map.save('.\\screens\\currMap.png')
        if general_utils.calc_img_diff(curr_map, Image.open('screens/ship_map.png'), 2) == 'same':
            print('on ship')
            general_utils.bezier_movement(1277, 1290, 672, 685)
            pyautogui.click()
            general_utils.random_sleep(2.4, 3.2)
    expected_store = ImageGrab.grab([1016, 436, 1064, 450])
    img = Image.open('screens/stan.png')
    if general_utils.calc_img_diff(img, expected_store, 5) == 'same':
        return True
    print('looking for martin')
    # cyan color boundaries [B, G, R]
    lower = [0, 255, 255]
    upper = [0, 255, 255]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if cv2.__version__[0] > '3':
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # draw in blue the contours that were founded
        # cv2.drawContours(output, contours, -1, 255, 3)

        # find the biggest contour (c) by the area
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        general_utils.bezier_movement((x + 926) + 10, (x + 926) + 15, (y + 344) + 10, (y + 344) + 15)
        general_utils.random_sleep(0.1, 0.2)
        pyautogui.click()
        general_utils.random_sleep(2.7, 3.1)
        # pyautogui.moveTo((x + 926) + 10,(y + 344) + 10)
        # draw the biggest contour (c) in green
    return False


def find_single_target():
    iters = 0
    found = False
    while not found:
        iters = iters + 1
        screen = np.array(ImageGrab.grab(bbox=(926, 344, 1664, 1114)))
        did_i_find = process_img(screen, iters)
        if did_i_find:
            found = True
            general_utils.random_sleep(0.5, 0.7)


def dump_item():
    seaweed = general_utils.rough_img_compare('.\\screens\\seaweed_in_bag.png', .75, (844, 438, 1402, 774))
    if seaweed:
        general_utils.bezier_movement(seaweed[0], seaweed[0] + 7, seaweed[1], seaweed[1] + 9)
        pyautogui.click()
        general_utils.random_sleep(0.2, 0.4)
    soda = general_utils.rough_img_compare('.\\screens\\soda_in_bag.png', .75, (844, 438, 1402, 774))
    if soda:
        general_utils.bezier_movement(soda[0], soda[0] + 6, soda[1], soda[1] + 6)
        pyautogui.click()
        general_utils.random_sleep(0.2, 0.4)
    kb.send('esc')
    general_utils.random_sleep(0.4, 0.6)


def main():
    while True:
        walk_to_dock()
        while True:
            # find charter ship traders
            find_single_target()
            # buy items
            buy_store_items([1196, 1220, 607, 620])
            if is_bag_full():
                print('bag is full')
                break
            # buy soda ash
            buy_store_items([1254, 1276, 606, 616])
            kb.send('esc')
            general_utils.random_sleep(0.3, 0.5)
            if is_bag_full():
                print('bag is full')
                break
            hopped = general_utils.hop_worlds()
            if hopped != 'success':
                return print(hopped)
        go_to_bank()
        dump_item()
        general_utils.random_sleep(4.3, 5.8)
        if random.randint(1, 10) == 2:
            general_utils.random_sleep(20.3, 25.9)


main()