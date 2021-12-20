import random
import keyboard as kb
from general_utils import isInvFull, randomSleep, roughImgCompare
from bezier import bezierMovement
import pyautogui as agui
from PIL import Image, ImageGrab
import numpy
bank = '.\\screens\\new_bank.png'
logsChopped = 0
fullInv = Image.open('.\\screens\\full.png')
trees = [
    '.\\screens\\tree1_1.png',
    '.\\screens\\tree1_2.png',
    '.\\screens\\tree2_1.png',
    '.\\screens\\tree2_2.png',
    '.\\screens\\tree3_1.png',
    '.\\screens\\tree3_2.png'
]

sq1 = [
    '.\\screens\\b1.png',
    '.\\screens\\b2.png',
    '.\\screens\\b3.png'
]

def bankAndReturn():
    for sq in sq1:
        nextSq = roughImgCompare(sq, .7, (0, 0, 1200, 1440))
        if nextSq:
            print('found the next square ', nextSq)
            nextSqCoords = [nextSq.get('x') + 5, nextSq.get('x') + 20, nextSq.get('y') + 5, nextSq.get('y') + 20]
            bezierMovement(nextSqCoords[0], nextSqCoords[1], nextSqCoords[2], nextSqCoords[3])
            agui.click()
            break
    randomSleep(9.4, 10.8)
    bankSq = roughImgCompare(bank, .7, (0, 0, 1600, 1440))
    if bankSq:
        print('found the bank square ', bankSq)
        bezierMovement(bankSq.get('x') + 20, bankSq.get('x') + 35, bankSq.get('y') + 3, bankSq.get('y') + 10)
        randomSleep(0.3,0.5)
        agui.click()
        randomSleep(7.6, 9.8)
    print('at bank, dumping')
    dump = roughImgCompare('.\\screens\\dump.png', .8, (500, 500, 1000, 1000))
    bezierMovement(dump.get('x'), dump.get('x') + 10, dump.get('y'), dump.get('y') + 10)
    agui.click()
    randomSleep(0.3,0.7)
    print('returning to tree')
    bezierMovement(1892, 1919, 312, 336)
    agui.click()
    randomSleep(15.7,16.2)
    

while logsChopped < 3458:
    currentInv = ImageGrab.grab([2299,  1024, 2510,1324])
    currentInv.save('.\\screens\\currInv.png')
    amCutting  = roughImgCompare('.\\screens\\cuttingStatus.png', .9, (0, 0, 200, 200))
    if isInvFull(currentInv, fullInv):
        print('Inventory is full. Going to bank.')
        bankAndReturn()
        logsChopped = logsChopped + 28
    elif amCutting:
        print('currently wood cutting')
        randomSleep(5.2,6.9)
        continue 
    elif not amCutting:
        print(' no longer chopping, looking for a new tree')
        nextTreeCoords = None
        for tree in trees:
            nextTree = roughImgCompare(tree, .8, (0, 0, 1500, 1440))
            if nextTree:
                print(' found a new tree to chop ', nextTree)
                nextTreeCoords = [nextTree.get('x'), nextTree.get('x') + 25, nextTree.get('y'), nextTree.get('y') + 25]
                bezierMovement(nextTreeCoords[0], nextTreeCoords[1], nextTreeCoords[2], nextTreeCoords[3])
                randomSleep(0.1,0.3)
                agui.click()
                randomSleep(0.1,0.3)
                print('chopping new tree')
                bezierMovement(2700, 3700, 600, 800)
                randomSleep(0.1,0.3)
                agui.click()
                break
    randomSleep(5.2,6.9)

