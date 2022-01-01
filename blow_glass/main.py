from osrs_utils import general_utils
import keyboard as kb
import random
import pyautogui


def blow_glass():
    molten_glass_made = 0
    print('starting script, look for bank')
    first_bank = general_utils.goToTarget([1098, 599, 1435, 945])
    if not first_bank:
        return print('unable to find bank on script init')
    while molten_glass_made < 3246:
        withdrawing = general_utils.withdraw_items_from_bank(['molten_glass_in_bank.png'], [816, 1430, 101, 1105])
        if withdrawing != 'success':
            return print(withdrawing)
        general_utils.randomSleep(0.3, 0.4)
        kb.send('esc')
        processing_status = general_utils.process_with_tool(1, '7', '..\\screens\\lens_in_bag.png', 35)
        if processing_status != 'success':
            return processing_status
        first_bank = general_utils.goToTarget([1098, 599, 1435, 945])
        if not first_bank:
            return print('unable to find bank')
        general_utils.randomSleep(1.1, 1.2)
        general_utils.bezierMovement(2371, 2395, 1034, 1058)
        general_utils.randomSleep(0.1, 0.2)
        pyautogui.click()
        general_utils.randomSleep(1.3, 1.5)
        if random.randint(1, 10) == 1:
            general_utils.randomSleep(5.2, 9.3)
        elif random.randint(1, 25) == 1:
            general_utils.randomSleep(15.5, 23.4)


blow_glass()
