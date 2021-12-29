"""
cook whatever is in the first bank slot at rogues den
"""
import pyautogui
from bezier import bezierMovement
from general_utils import randomSleep
import keyboard as kb
import timeit

start = timeit.default_timer()
bank = [1288, 1358, 987, 1052]
firstBankSlot = [898, 922, 208, 230]
fire = [1615, 1684, 804, 868]
cooked = 0

while cooked < 2342:
    #click bank
    bezierMovement(1293, 1344, 991, 1087)
    randomSleep(0.2,0.3)
    pyautogui.click()
    randomSleep(0.6, 0.9)
    #dump cooked
    bezierMovement(1338, 1366, 1064, 1086)
    randomSleep(0.2,0.3)
    pyautogui.click()
    randomSleep(0.4,0.6)
    #click first tile
    bezierMovement(898, 922, 208, 230)
    randomSleep(0.2,0.3)
    pyautogui.click()
    randomSleep(0.2,0.3)
    #close interface
    kb.send('esc')
    randomSleep(0.2,0.3)
    #click first inv slot
    bezierMovement(2317, 2343, 1030, 1056)
    randomSleep(0.2,0.3)
    pyautogui.click()
    randomSleep(0.2,0.3)
    #click fire
    bezierMovement(1615, 1684, 804, 868)
    randomSleep(0.2,0.3)
    pyautogui.click()
    randomSleep(1.4,1.5)
    #cook stuff
    kb.send('1')
    #wait til its done
    randomSleep(67.4,69.3)
    cooked = cooked + 28
    print('food cooked: ', cooked)
    print('run time: ', timeit.default_timer() - start)
