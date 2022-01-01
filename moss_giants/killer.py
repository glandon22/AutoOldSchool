import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui
from osrs_utils import general_utils
import math
mini_map_north_click = [2440, 2458, 42, 54]
# click north every couple seconds until i see the cyan blobs
# click a cyan blob
# have to figure out how to pick up drops
# it appears my character sstays generally with then 1260-1290 for x and 700-730 for y
# next id liek to try to highlight the monster that is closest to me


def find_giants():
    # begin walking north to find some moss giants
    cycles_looking_for_giant = 0
    while True:
        print('cycles looking for giants: ', cycles_looking_for_giant)
        screen = np.array(ImageGrab.grab())
        general_utils.walk_north_minimap()
        found_giant = general_utils.find_moving_target(screen, True)
        if found_giant:
            cycles_looking_for_giant = 0
            break
        elif cycles_looking_for_giant > 30:
            return 'unable to find giants after banking'
        else:
            cycles_looking_for_giant += 1
        general_utils.randomSleep(1.3, 1.8)
    return 'success'


def attack_giants():
    cycles_to_attack_giant = 0
    while True:
        screen = np.array(ImageGrab.grab())
        attack_giant = general_utils.find_moving_target(screen, False)
        if attack_giant:
            cycles_to_attack_giant = 0
            general_utils.bezierMovement(3500,4000,700,1200)
            general_utils.randomSleep(0.1,0.2)
            pyautogui.click()
            return 'success'
        elif cycles_to_attack_giant > 7:
            return 'couldnt attack a giant'
        else:
            cycles_to_attack_giant += 1
        general_utils.randomSleep(1.1, 1.2)


def kill_giant():
    cycles_in_combat = 0
    while True:
        print('cycles in combat: ', cycles_in_combat)
        screen = np.array(ImageGrab.grab())
        still_in_combat = general_utils.find_click_x(screen)
        # been in combat for too long something is wrong, leave the area
        if cycles_in_combat > 5000:
            general_utils.walk_north_minimap()
            general_utils.randomSleep(1.1, 1.4)
            general_utils.walk_north_minimap()
            return 'been in combat for too long, leave the area'
        elif still_in_combat:
            cycles_in_combat += 1
        else:
            return 'success'


def experimental_kill_giant():
    cycles_in_combat = 0
    center_finds = 0
    aggregate_center = [0, 0]
    while True:
        general_utils.randomSleep(0.1, 0.2)
        print('cycles in combat: ', cycles_in_combat)
        screen = np.array(ImageGrab.grab())
        still_in_combat = general_utils.experimental_find_click_x(screen)
        if isinstance(still_in_combat, list):
            center_finds += 1
            aggregate_center[0] = still_in_combat[1][0] + aggregate_center[0] / center_finds
            aggregate_center[1] = still_in_combat[1][1] + aggregate_center[1] / center_finds
            # been in combat for too long something is wrong, leave the area
            if cycles_in_combat > 5000:
                general_utils.walk_north_minimap()
                general_utils.randomSleep(1.1, 1.4)
                general_utils.walk_north_minimap()
                return 'been in combat for too long, leave the area'
            elif still_in_combat[0]:
                cycles_in_combat += 1
            else:
                print('ag', round(aggregate_center[0]), round(aggregate_center[1]))
                pyautogui.moveTo(round(aggregate_center[0]) + 40, round(aggregate_center[1]) - 25)
                return 'success'
        else:
            if cycles_in_combat > 5000:
                general_utils.walk_north_minimap()
                general_utils.randomSleep(1.1, 1.4)
                general_utils.walk_north_minimap()
                return 'been in combat for too long, leave the area'
            elif still_in_combat:
                cycles_in_combat += 1
            else:
                print('ag', round(aggregate_center[0]), round(aggregate_center[1]))
                pyautogui.moveTo(round(aggregate_center[0]) + 40, round(aggregate_center[1]) - 25)
                return 'success'

def check_to_eat(food):
    while True:
        food_loc = general_utils.look_for_item_in_bag(food)
        if food_loc:
            general_utils.bezierMovement(food_loc.get('x') + 2, food_loc.get('x') + 5, food_loc.get('y') + 2, food_loc.get('y') + 5)
            general_utils.randomSleep(0.2,0.3)
            screen = ImageGrab.grab([2299, 1024, 2510, 1324])
            ate = general_utils.will_food_heal_full(screen)
            # I have food, but i no longer will get the max hp restore from eating
            if not ate:
                print('HAVE FOOD BUT DONT NEED TO EAT')
                break
            else:
                print('eating')
                pyautogui.click()
                general_utils.randomSleep(0.5,0.6)
        else:
            return 'no food'
    return 'success'


def generic_killer():
    kills = 0
    while True:
        attack = attack_giants()
        if attack != 'success':
            return print(attack)
        # currently in combat, make sure i dont die and wait til i kill the giant
        kill = kill_giant()
        if kill != 'success':
            return print(kill)
        kills += 1
        if kills % 5 == 0:
            # check if I need to eat
            ate = check_to_eat('tuna_in_bag.png')
            if ate != 'success':
                return print(ate)

def main():
    find = find_giants()
    print('f', find)
    if find != 'success':
        return find
    print('found giants')
    general_utils.randomSleep(2.0, 2.1)

    # attack giants until bag is full
    kills = 0
    while True:
        attack = attack_giants()
        if attack != 'success':
            return print(attack)
        # currently in combat, make sure i dont die and wait til i kill the giant
        kill = kill_giant()
        if kill != 'success':
            return print(kill)
        kills += 1
        if kills % 3 == 0:
            # check if I need to eat
            ate = check_to_eat('tuna_in_bag.png')
            if ate != 'success':
                return print(ate)
        # pick up loot
        # loot = general_utils.find_loot((913, 312, 1574, 1047))
        # if not loot:
            #print('couldnt find my loot')
        #check to see if i need to eat
        #loot monster drops
        #continue loop
        # TODO: find_giants will not click more than once, it always finds a giant even when not there
        # TODO: create a runelite plugin in the plugin hub that fills the loots square


#main()

def main1():
    print(experimental_kill_giant())


def main2():
    while True:
        print(pyautogui.position())
        time.sleep(1)
generic_killer()