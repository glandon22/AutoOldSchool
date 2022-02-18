import numpy as np
import pyscreenshot
from PIL import ImageGrab
import cv2
import time
import pyautogui
from osrs_utils import general_utils
import keyboard

# click lizard, make sure i got it
# while waiting to kill it, check health and see if i need to eat
# once dead, find loot

"""
Ground Items Highlight List:
Fire rune,  Nature rune, Iron ore, Coal, Iron bar, Steel bar, Silver ore, Silver bar, Mithril ore, Rainbow fish, 
Mystic gloves (light), Uncut*, Loop half of key, Tooth half of key, Rune spear, Dragon spear, Shield left half
"""

def eat(inventory, ids):
    for item in inventory:
        if item["id"] in ids:
            general_utils.click_inv_slot(item["index"])
            return True
    else:
        return False


def kill_sulphur_lizards():
    while True:
        cycles = 0
        # Attack a lizard
        while True:
            general_utils.wait_until_stationary()
            if cycles <= 10:
                screen = np.array(pyscreenshot.grab((640, 360, 1920, 1080)))
                lizard = general_utils.find_moving_target_near(screen, False, 640, 360)
                if lizard:
                    break
                else:
                    cycles += 1
            elif cycles > 50:
                return 'couldnt attack lizard'
            elif cycles > 10:
                screen = np.array(pyscreenshot.grab())
                lizard = general_utils.find_moving_target(screen, False,)
                if lizard:
                    break
                else:
                    cycles += 1
        # Wait to kill the lizard
        while True:
            player_info = general_utils.get_player_info()
            if player_info:
                for skill in player_info["skills"]:
                    if skill["skillName"] == 'HITPOINTS':
                        print('current health: ', skill["boostedLevel"])
                        if skill["realLevel"] > skill["boostedLevel"] + 20:
                            # eat
                            ate = eat(player_info["inventory"], {10136, 361})
                            # let the monster re-attack me before checking if im in combat
                            general_utils.random_sleep(2.0, 2.1)
                            if not ate:
                                return 'out of food'
            screen = np.array(pyscreenshot.grab((640, 360, 1920, 1080)))
            if not general_utils.find_click_x(screen):
                break
        # Loot kill, wait for death animation to finish
        general_utils.random_sleep(6.0, 6.1)
        cycles = 0
        while True:
            print('looking for loot')
            if cycles > 10:
                print('couldnt find loot, waited too long')
                break
            screen = np.array(pyscreenshot.grab((640, 360, 1920, 1080)))
            loot = general_utils.find_loot(screen, 640, 360)
            if loot:
                break
            cycles += 1




kill_sulphur_lizards()