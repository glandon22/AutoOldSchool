"""
buys sea weed and soda ash from the traders in port khazard
full screen on the 2560x1440 screen
looking due north with view at max altitude
"""
import random
from PIL import ImageGrab, Image
import pyautogui
import keyboard as kb
from osrs_utils import general_utils

bankInterface = [816, 1430, 101, 1105]


def run_to_furnace(furnace_loc):
    print('running to furnace')
    furnace = general_utils.go_to_target(furnace_loc)
    if not furnace:
        return 'exiting script, unable to find furnace'
    else:
        return 'success'


def waiting_to_arrive_at_furnace():
    cycles_waiting_for_prompt = 0
    while True:
        print('waiting to see molten glass make prompt')
        is_prompt_up = general_utils.rough_img_compare('.\\screens\\molten_glass_prompt.png', .8, (2, 1190, 645, 1350))
        im = ImageGrab.grab([2, 1190, 645, 1350])
        im.save('.\\screens\\currChatBox.png')
        if is_prompt_up:
            kb.send('space')
            break
        elif cycles_waiting_for_prompt > 10:
            return 'never made it to furnace'
        else:
            cycles_waiting_for_prompt += 1
        general_utils.random_sleep(1.2, 2.5)
    return 'success'


def make_glass():
    cycles_making_glass = 0
    general_utils.bezier_movement(3500, 4000, 0, 1400)
    general_utils.random_sleep(0.1, 0.2)
    pyautogui.click()
    while True:
        print('waiting to finish cooking glass')
        last_slot = ImageGrab.grab([2476, 1304, 2500, 1324])
        last_slot.save('.\\screens\\currLastSlot.png')
        # check to see if last inv slot contains a molten glass
        if general_utils.calc_img_diff(last_slot, Image.open('.\\screens\\glass_in_bag.png'), 4) == 'same':
            print('done making glass')
            return 'success'
        elif cycles_making_glass > 10:
            return print('never finished making glass, exiting')
        # check if I leveled
        elif general_utils.rough_img_compare('.\\screens\\level.png', .8, (2, 645, 1190, 1350)):
            found_furnace = run_to_furnace([1078, 584, 1376, 854])
            if found_furnace != 'success':
                return found_furnace
            general_utils.random_sleep(3.4, 4.1)
            arrived_at_furnace = waiting_to_arrive_at_furnace()
            if arrived_at_furnace != 'success':
                return arrived_at_furnace
            cycles_making_glass = 0
        else:
            cycles_making_glass += 1
        general_utils.random_sleep(2.3, 3.2)


def wait_for_bank_interface_and_dump():
    cycles_waiting_for_bank = 0
    while True:
        print('waiting for bank interface')
        if general_utils.dumpBag():
            return 'success'
        elif cycles_waiting_for_bank > 10:
            return 'never saw bank interface, exiting'
        else:
            cycles_waiting_for_bank += 1
        general_utils.random_sleep(1.2, 2.5)


# main function needs to be sanity tested, as I have done some partial refactoring
def main():
    molten_glass_made = 0
    print('starting script, look for bank')
    first_bank = general_utils.go_to_target([1098, 599, 1435, 945])
    if not first_bank:
        return print('unable to find bank on script init')
    general_utils.random_sleep(0.5, 1.2)
    while molten_glass_made < 3287:
        withdrawing = general_utils.withdraw_items_from_bank(['soda_in_bank.png', 'sand_in_bank.png'],
                                                             [816, 1430, 101, 1105])
        if withdrawing != 'success':
            return print(withdrawing)
        general_utils.random_sleep(0.3, 0.4)
        found_furnace = run_to_furnace([1618, 422, 1966, 699])
        if found_furnace != 'success':
            return print(found_furnace)
        general_utils.random_sleep(3.4, 4.1)
        arrived_at_furnace = waiting_to_arrive_at_furnace()
        if arrived_at_furnace != 'success':
            return print(arrived_at_furnace)
        glass_made = make_glass()
        if glass_made != 'success':
            return print(glass_made)
        # find bank from furnace
        banking = general_utils.go_to_target([474, 873, 781, 1102])
        if not banking:
            return print('unable to find bank after making glass')
        dumping = wait_for_bank_interface_and_dump()
        if dumping != 'success':
            return print(dumping)
        molten_glass_made += 14
        print('-----------------------------------------------------------------')
        print('MOLTEN GLASS MADE: ', molten_glass_made)
        print('-----------------------------------------------------------------')
        if random.randint(1, 10) == 1:
            general_utils.random_sleep(5.2, 9.3)
        elif random.randint(1, 25) == 1:
            general_utils.random_sleep(15.5, 23.4)


main()
