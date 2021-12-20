#start fletching then start the bot
import keyboard as kb
from general_utils import lastSlotFletched, randomSleep, roughImgCompare, didILvlFletch
from bezier import bezierMovement
import pyautogui as agui
from PIL import Image, ImageGrab
bow = Image.open('.\\screens\\bow.png')
level = Image.open('.\\screens\\level.png')
status = 'initing'
bagsFletched = 0
def bank():
     #click on bank
    bezierMovement(1182, 1294, 436, 516)
    randomSleep(0.1,0.3)
    agui.click()
    randomSleep(0.5,1.2)
    #deposit bows
    bezierMovement(2371, 2395, 1034, 1058)
    agui.click()
    randomSleep(0.4,0.6)
    #click on logs
    bezierMovement(897, 921, 212, 232)
    randomSleep(0.2,0.4)
    agui.click()
    randomSleep(0.2,0.5)
    #close bank interface
    kb.send('esc')
    randomSleep(0.2,0.6)
def fletch(slot):
    #click on knife
    bezierMovement(2317, 2343, 1030, 1056)
    agui.click()
    randomSleep(0.2,0.5)
    #click on log
    if slot == 1:
        bezierMovement(2371, 2395, 1034, 1058)
    else:
        bezierMovement(2476, 2500, 1304, 1324)
    agui.click()
    randomSleep(1.2,1.7)
    agui.press('3')
    randomSleep(0.3,0.7)
    #move off screen
    bezierMovement(3500, 4000, 0, 250)
    randomSleep(0.4,0.7)
    agui.click()
while bagsFletched < 424:
    lastSlot = ImageGrab.grab([2476, 1304, 2500, 1324])
    lastSlot.save('.\\screens\\currLastSlot.png')
    if lastSlotFletched(lastSlot, bow):
        print('done fletching, banking')
        bank()
        print('banked, now starting to fletch')
        fletch(1)
        print('now fletching')
    elif didILvlFletch(level):
        print('leveled, starting to fletch again')
        randomSleep(15.5,23.7)
        fletch(2)
    else:
        print('still fletching, continue')
    randomSleep(6.9,9.3)
