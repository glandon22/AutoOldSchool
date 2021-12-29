"""
buys sea weed and soda ash from the traders in port khazard
full screen on the 2560x1440 screen
looking due north with view at max altitude
"""
import random
from PIL import ImageGrab, Image
import pyautogui
from general_utils import randomSleep, calcImgDiff
import keyboard as kb
from osrs_utils import general_utils

bankInterface = [816, 1430, 101, 1105]


def runToFurnace(furnaceLoc):
    print('running to furnace')
    furnace = general_utils.goToTarget(furnaceLoc)
    if not furnace:
        return 'exiting script, unable to find furnace'
    else:
        return 'success'


def waitingToArriveAtFurnace():
    cyclesWaitingForGlassPrompt = 0
    while True:
        print('waiting to see molten glass make prompt')
        isPromptUp = general_utils.roughImgCompare('.\\screens\\molten_glass_prompt.png', .8, (2, 1190, 645, 1350))
        im = ImageGrab.grab([2, 1190, 645, 1350])
        im.save('.\\screens\\currChatBox.png')
        if isPromptUp:
            kb.send('space')
            break
        elif cyclesWaitingForGlassPrompt > 10:
            return 'never made it to furnace'
        else:
            cyclesWaitingForGlassPrompt += 1
        randomSleep(1.2, 2.5)
    return 'success'


def makeGlass():
    cyclesMakingGlass = 0
    general_utils.bezierMovement(3500, 4000, 0, 1400)
    randomSleep(0.1, 0.2)
    pyautogui.click()
    while True:
        print('waiting to finish cooking glass')
        lastSlot = ImageGrab.grab([2476, 1304, 2500, 1324])
        lastSlot.save('.\\screens\\currLastSlot.png')
        # check to see if last inv slot contains a molten glass
        if calcImgDiff(lastSlot, Image.open('.\\screens\\glass_in_bag.png'), 4) == 'same':
            print('done making glass')
            return 'success'
        elif cyclesMakingGlass > 10:
            return print('never finished making glass, exiting')
        # check if i leveled
        elif general_utils.roughImgCompare('.\\screens\\level.png', .8, (2, 645, 1190, 1350)):
            foundFurnace = runToFurnace([1078, 584, 1376, 854])
            if foundFurnace != 'success':
                return foundFurnace
            randomSleep(3.4, 4.1)
            arrivedAtFurnace = waitingToArriveAtFurnace()
            if arrivedAtFurnace != 'success':
                return arrivedAtFurnace
            cyclesMakingGlass = 0
        else:
            cyclesMakingGlass += 1
        randomSleep(2.3, 3.2)


def waitForBankInterfaceAndDump():
    cyclesWaitingForBank = 0
    while True:
        print('waiting for bank interface')
        if general_utils.dumpBag():
            return 'success'
        elif cyclesWaitingForBank > 10:
            return 'never saw bank interface, exiting'
        else:
            cyclesWaitingForBank += 1
        randomSleep(1.2, 2.5)


# main function needs to be sanity tested, as i have done some partial refactoring
def main():
    moltenGlassMade = 0
    print('starting script, look for bank')
    firstBank = general_utils.goToTarget([1098, 599, 1435, 945])
    if not firstBank:
        return print('unable to find bank on script init')
    randomSleep(0.5, 1.2)
    while moltenGlassMade < 3287:
        withdrawing = general_utils.withdrawItemsFromBank(['soda_in_bank.png', 'sand_in_bank.png'],
                                                          [816, 1430, 101, 1105])
        if withdrawing != 'success':
            return print(withdrawing)
        randomSleep(0.3, 0.4)
        foundFurnace = runToFurnace([1618, 422, 1966, 699])
        if foundFurnace != 'success':
            return print(foundFurnace)
        randomSleep(3.4, 4.1)
        arrivedAtFurnace = waitingToArriveAtFurnace()
        if arrivedAtFurnace != 'success':
            return print(arrivedAtFurnace)
        glassMade = makeGlass()
        if glassMade != 'success':
            return print(glassMade)
        # find bank from furnace
        banking = general_utils.goToTarget([474, 873, 781, 1102])
        if not banking:
            return print('unable to find bank after making glass')
        dumping = waitForBankInterfaceAndDump()
        if dumping != 'success':
            return print(dumping)
        moltenGlassMade += 14
        print('-----------------------------------------------------------------')
        print('MOLTEN GLASS MADE: ', moltenGlassMade)
        print('-----------------------------------------------------------------')
        if random.randint(1, 10) == 1:
            randomSleep(5.2, 9.3)
        elif random.randint(1, 25) == 1:
            randomSleep(15.5, 23.4)


main()
