# this code depends on the bank stander plugin
# this code assumes high alch spell is in top right of spell book
# after filtering, uncheck show combat spells, teleport, and spells u dont have runes to cast

# code:
# start w spell book open
# move mouse to one of approved spots
# click
# wait for next screen
# click again
# take break when needed, then move mouse back to approved position
import random

import pyautogui

from autoscape import general_utils

def main():
    prev_screen = 'spell book'
    general_utils.move_around_center_screen(1867, 766, 1871, 772)
    pyautogui.click()
    while True:
        general_utils.move_around_center_screen(1867, 766, 1871, 772)
        # move spot im clicking every 175 alchs or so
        while True:
            if random.randint(0, 175) == 1:
                break
            # wait for screen to change
            while True:
                curr_screen = general_utils.rough_img_compare(
                    '..\\screens\\inventory_icon.png',
                    .9,
                    (1500, 600, 1920, 1080)
                )
                if curr_screen and prev_screen == 'spell book':
                    pyautogui.click()
                    prev_screen = 'inventory'
                    general_utils.random_sleep(0.1, 0.2)
                    break
                elif not curr_screen and prev_screen == 'inventory':
                    pyautogui.click()
                    prev_screen = 'spell book'
                    general_utils.random_sleep(0.1, 0.2)
                    break
            general_utils.antiban_rest(200, 300, 500)


main()

