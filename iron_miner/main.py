#Script starting environment
#compass due north
#POV max top
#max zoom
import datetime
import keyboard as kb
from general_utils import checkBag, randomSleep, showInvCoords
from bezier import bezierMovement
import pyautogui as agui
import random
oreMined = 0
miningRock = 0
rockCoords = [
    [860, 961, 672, 814],
    [1199, 1290, 400, 475],
    [1540, 1600, 744, 807]
]
scriptStartTime = datetime.datetime.now()
status = 'initing'
#the script can click to fast before the ore has spawned, need to add in a fail safe counter
while oreMined < 2500:
    if status == 'initing':
        toRock = rockCoords[miningRock]
        bezierMovement(toRock[0],toRock[1],toRock[2],toRock[3])
        agui.click()
        randomSleep(0.2,0.4)
        toFirstInvSlot = showInvCoords(0)
        bezierMovement(toFirstInvSlot[0],toFirstInvSlot[1],toFirstInvSlot[2],toFirstInvSlot[3])
        status = 'mining'
        oreMined = oreMined + 1
        continue

    isIronInBag = checkBag()
    if isIronInBag:
        status = 'dropping ore'
        kb.press('shift')
        randomSleep(0.2,0.4)
        agui.click()
        randomSleep(0.2,0.4)
        kb.release('shift')
        toRock = rockCoords[oreMined % 3]
        bezierMovement(toRock[0],toRock[1],toRock[2],toRock[3])
        agui.click()
        randomSleep(0.2,0.4)
        toFirstInvSlot = showInvCoords(0)
        bezierMovement(toFirstInvSlot[0],toFirstInvSlot[1],toFirstInvSlot[2],toFirstInvSlot[3])
        status = 'mining'
        oreMined = oreMined + 1
        #potential break
        if random.randint(1,100) == 3:
            print('sleeping for up to 4 seconds')
            randomSleep(2.4,4.7)
        elif random.randint(1,225) == 9:
            randomSleep(10.7,16.9)
            print('sleeping for up to 16 seconds')
        elif random.randint(1,450) == 17:
            print('sleeping for up to 78 seconds')
            randomSleep(60.4,78.9)

        print('runtime: ', datetime.datetime.now() - scriptStartTime)
        print('ore mined ', oreMined)
        print('xp gained ', oreMined * 35)




