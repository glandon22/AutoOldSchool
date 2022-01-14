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
        general_utils.randomSleep(2.3, 3.8)
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

def eat(food):
    food_loc = general_utils.look_for_item_in_bag(food)
    if food_loc:
        general_utils.bezierMovement(food_loc.get('x') + 2, food_loc.get('x') + 5, food_loc.get('y') + 2,
                                     food_loc.get('y') + 5)
        general_utils.randomSleep(0.1,0.2)
        pyautogui.click()
        return 'success'
    else:
        return 'out of food'

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


def go_to_bank():
    # begin walking north to find some moss giants
    cycles_looking_for_bank = 0
    while True:
        print('cycles looking for bank: ', cycles_looking_for_bank)
        screen = np.array(ImageGrab.grab())
        general_utils.walk_south_minimap()
        found_bank = general_utils.find_fixed_object_while_moving([0, 0, 2560, 1440], True)
        if found_bank:
            general_utils.bezierMovement(found_bank[0], found_bank[0] + 10, found_bank[1], found_bank[1] + 10)
            pyautogui.click()
            print('found bank, sleeping for a sec')
            break
        elif cycles_looking_for_bank > 10:
            return 'unable to find bank'
        else:
            print('didnt find the bank')
            cycles_looking_for_bank += 1
        general_utils.randomSleep(3.3, 4.8)
    general_utils.randomSleep(5.2, 5.6)
    cycles_trying_to_click_bank = 0
    while True:
        screen = np.array(ImageGrab.grab())
        clicked_bank = general_utils.find_fixed_object_while_moving([0, 0, 2560, 1440], False)
        if clicked_bank:
            print('clicked bank')
            break
        elif cycles_trying_to_click_bank > 5:
            return 'unable to find bank'
        else:
            print('didnt find the bank')
            cycles_trying_to_click_bank += 1
    return 'success'


def collect_loot():
    cycles_waiting_for_loot = 0
    general_utils.randomSleep(3.2, 3.3)
    while True:
        loot = general_utils.find_highlighted_item_on_ground(np.array(ImageGrab.grab([1167, 565, 1406, 800])), 1167,
                                                             565)
        loot_collected = False
        cycles_looting = 0
        # found loot on ground
        if loot:
            click_loc = loot
            # loot the pile, loop through in case there are multiple valuable drops
            while True:
                print('cycles looting', cycles_looting)
                general_utils.bezierMovement(click_loc[0] - 5, click_loc[0] + 5, click_loc[1] - 5, click_loc[1] + 5)
                general_utils.randomSleep(0.1, 0.2)
                pyautogui.click()
                general_utils.randomSleep(2.1, 2.2)
                more_loot = general_utils.find_highlighted_item_on_ground(
                    np.array(ImageGrab.grab([1167, 565, 1406, 800])), 1167, 565)
                # there is more loot on the ground
                if more_loot:
                    # more loot is on ground, but i havent been able to get it after five tries or my bag is full
                    if cycles_looting > 5 or general_utils.is_bag_full():
                        print('unable to finish looting')
                        loot_collected = True
                        break
                    click_loc = more_loot
                    cycles_looting += 1
                    continue
                # I picked up all the loot
                else:
                    loot_collected = True
                    break
            break
        # could not find loot after 150 cycles
        elif cycles_waiting_for_loot > 150:
            print('failed to get loot')
            break
        # i have gathered all the loot
        elif loot_collected:
            print('got all loot')
            break
        # continuing to look for loot pile
        else:
            print('waiting for loot')
            cycles_waiting_for_loot += 1


def main():
    while True:
        find = find_giants()
        print('f', find)
        if find != 'success':
            return find
        print('found giants')
        general_utils.randomSleep(2.0, 2.1)
        # attack giants until bag is full
        while True:
            attack = attack_giants()
            if attack != 'success':
                return print(attack)
            # currently in combat, make sure i dont die and wait til i kill the giant
            kill = kill_giant()
            if kill != 'success':
                return print(kill)
            # check my hp
            health = general_utils.check_health()
            if health and 10 < health < 40:
                print('current health', health)
                did_i_eat = eat('tuna_in_bag.png')
                if did_i_eat != 'success':
                    print(did_i_eat)
                    # return to bank to get more food
                    break
            collect_loot()
            is_bag_full = general_utils.is_bag_full()
            # return to bank if bag is full
            if is_bag_full:
                break
        find_bank = go_to_bank()
        if find_bank != 'success':
            return print(find_bank)
        wait_for_bank_interface = general_utils.wait_for_bank_interface([821, 1424, 108, 1102], 60)
        if wait_for_bank_interface != 'success':
            return print(wait_for_bank_interface)
        dump_bag = general_utils.dump_bag()
        if dump_bag != 'success':
            return print(dump_bag)
        withdraw_tuna = general_utils.withdraw_items_from_bank('tuna_in_bank.png', [821, 1424, 108, 1102])
        if withdraw_tuna != 'success':
            return print(withdraw_tuna)



main()
