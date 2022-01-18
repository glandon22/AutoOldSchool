# Script starting environment
# compass due north
# POV max top
# max zoom
# script doesn't really work anymore
import datetime
import keyboard as kb
from PIL import Image
import pyscreenshot as image_grab

from osrs_utils import general_utils
import pyautogui as agui
import random

oreMined = 0
miningRock = 0
rockCoords = [
    [860, 961, 672, 814],
    [1199, 1290, 400, 475],
    [1540, 1600, 744, 807]
]
emptySlot = Image.open('screens/empty_slot.png')


def check_bag():
    iron_ore_coords = general_utils.show_inv_coords(0)
    im = image_grab.grab([iron_ore_coords[0], iron_ore_coords[2], iron_ore_coords[1], iron_ore_coords[3]])
    return general_utils.calc_img_diff(im, emptySlot, 5)


scriptStartTime = datetime.datetime.now()
status = 'initing'
# the script can click to fast before the ore has spawned, need to add in a fail-safe counter
while oreMined < 2500:
    if status == 'initing':
        toRock = rockCoords[miningRock]
        general_utils.bezier_movement(toRock[0], toRock[1], toRock[2], toRock[3])
        agui.click()
        general_utils.random_sleep(0.2, 0.4)
        toFirstInvSlot = general_utils.show_inv_coords(0)
        general_utils.bezier_movement(toFirstInvSlot[0], toFirstInvSlot[1], toFirstInvSlot[2], toFirstInvSlot[3])
        status = 'mining'
        oreMined = oreMined + 1
        continue

    isIronInBag = check_bag()
    if isIronInBag:
        status = 'dropping ore'
        kb.press('shift')
        general_utils.random_sleep(0.2, 0.4)
        agui.click()
        general_utils.random_sleep(0.2, 0.4)
        kb.release('shift')
        toRock = rockCoords[oreMined % 3]
        general_utils.bezier_movement(toRock[0], toRock[1], toRock[2], toRock[3])
        agui.click()
        general_utils.random_sleep(0.2, 0.4)
        toFirstInvSlot = general_utils.show_inv_coords(0)
        general_utils.bezier_movement(toFirstInvSlot[0], toFirstInvSlot[1], toFirstInvSlot[2], toFirstInvSlot[3])
        status = 'mining'
        oreMined = oreMined + 1
        # potential break
        if random.randint(1, 100) == 3:
            print('sleeping for up to 4 seconds')
            general_utils.random_sleep(2.4, 4.7)
        elif random.randint(1, 225) == 9:
            general_utils.random_sleep(10.7, 16.9)
            print('sleeping for up to 16 seconds')
        elif random.randint(1, 450) == 17:
            print('sleeping for up to 78 seconds')
            general_utils.random_sleep(60.4, 78.9)

        print('runtime: ', datetime.datetime.now() - scriptStartTime)
        print('ore mined ', oreMined)
        print('xp gained ', oreMined * 35)
