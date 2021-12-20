#Script starting environment
#compass due north
#POV max top
#max zoom
import cv2
import datetime
import keyboard as kb
from general_utils import checkBag, randomSleep, showInvCoords
from bezier import bezierMovement
import pyautogui as agui
import random
stolen = 0
stall = [1561, 1659, 850, 919]
scriptStartTime = datetime.datetime.now()
status = 'initing'
#the script can click to fast before the ore has spawned, need to add in a fail safe counter
while stolen < 3266:
    randomSleep(1.9,2.4)
    if status == 'initing':
        bezierMovement(stall[0],stall[1],stall[2],stall[3])
        agui.click()
        randomSleep(0.2,0.4)
        toFirstInvSlot = showInvCoords(0)
        bezierMovement(toFirstInvSlot[0],toFirstInvSlot[1],toFirstInvSlot[2],toFirstInvSlot[3])
        status = 'thieving'
        stolen = stolen + 1
        continue

    isIronInBag = checkBag()
    if isIronInBag:
        status = 'dropping fruit'
        kb.press('shift')
        randomSleep(0.2,0.4)
        agui.click()
        randomSleep(0.2,0.4)
        kb.release('shift')
        bezierMovement(stall[0],stall[1],stall[2],stall[3])
        agui.click()
        randomSleep(0.2,0.4)
        toFirstInvSlot = showInvCoords(0)
        bezierMovement(toFirstInvSlot[0],toFirstInvSlot[1],toFirstInvSlot[2],toFirstInvSlot[3])
        status = 'thieving'
        stolen = stolen + 1
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
        print('fruit stolen ', stolen)
        print('xp gained ', stolen * 28)




