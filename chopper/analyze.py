from PIL import Image
from PIL import ImageChops
import pyscreenshot as ImageGrab
import math,operator
from functools import reduce

fullInv = Image.open('.\\screens\\full_bag_unfletched.png')
fullInvFletched = Image.open('.\\screens\\full_bag_fletched.png')
treeUp = Image.open('.\\screens\\north_tree_up1.png')
fletchLevel = Image.open('.\\screens\\fletch_level.png')

def calcImgDiff(im1, im2):
    imageDifference = ImageChops.difference(im1,im2).histogram()
    diff = math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), imageDifference, range(256))
    ) / (float(im1.size[0]) * im2.size[1]))
    return diff

def isInvFull(currInv):
    diff = calcImgDiff(currInv, fullInv)
    print('bag diff', diff)
    if diff < 2: return True
    else: return False
def getTreeStatus(tree):
    diff = calcImgDiff(tree, treeUp)
    print('tree diff', diff)
    if diff < 10: return True
    else: return False
def isBagFletched(currInv):
    diff = calcImgDiff(currInv, fullInvFletched)
    print('bag diff (fletched)', diff)
    if diff < 2: return True
    else: return False
def gainedLevel(chatBox):
    diff = calcImgDiff(chatBox, fletchLevel)
    print('fletch level diff ', diff)
    if diff < 4: return True
    else: return False

def analyze_context(currStatus):
    treeStatus = ImageGrab.grab([1250,475,1405,660])
    treeStatus.save(r'screens\\last_tree_sighting.png', 'png')
    inventoryStatus = ImageGrab.grab([2300,1040,2525,1335])
    inventoryStatus.save(r'screens\\last_inv_sighting.png', 'png')
    chatStatus = ImageGrab.grab([2,1190,645,1350])
    if currStatus == 'Chopping':
        #inventory is full, time to fletch
        # TO DO
        if isInvFull(inventoryStatus):
            print('Inv is full')
            return 'start fletching'
        #inventory is not full, now should check if tree is up
        else:
            #im still chopping, do nothing
            if getTreeStatus(treeStatus):
                print('inv not full, still currently chopping')
                return 'no action'
            #tree is cut down without filling inv, wait for respawn then start cutting again
            else:
                print('inv is not full, tree down, currently waiting')
                return 'tree down, wait'
    elif currStatus == 'Waiting for willow':
        if getTreeStatus(treeStatus):
            print('waiting for willow, tree back up, going to start chopping')
            return 'Begin chopping'
        else:
            print('currently waiting for willow, tree is still down')
            return 'no action'
    elif currStatus == 'Currently fletching':
        if isBagFletched(inventoryStatus):
            #all logs fletched, time to sell
            return 'start selling'
        else:
            # TO DO
            #gained a fletch level, need to start fletching again
            if gainedLevel(chatStatus):
                return 'gained fletch level'
            else:
                return 'no action'

