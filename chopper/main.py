from bezier import bezierMovement 
import pyautogui as agui
from util import randomSleep
from analyze import analyze_context
import keyboard as kb

status = 'Initializing'
gameContext = None
continueLoop = True
def chopTree():
    print('beginning to chop tree')
    bezierMovement(1279,1352,530,628)
    randomSleep(0.1,0.2)
    agui.click()
    bezierMovement(3100,3700,500,1000)
    randomSleep(0.1,0.2)
    agui.click()
    return 'Chopping'

def fletch(x1,x2,y1,y2):
    print('starting to fletch')
    #click knife
    bezierMovement(2315,2340,1028,1060)
    randomSleep(0.1,0.2)
    agui.click()
    randomSleep(0.2,0.4)
    #click log
    bezierMovement(x1,x2,y1,y2)
    randomSleep(0.1,0.2)
    agui.click()
    randomSleep(0.6,1.7)
    kb.send('3')
    randomSleep(0.6,0.9)
    #click away
    bezierMovement(3100,3700,500,1000)
    randomSleep(0.1,0.2)
    agui.click()
    return 'Currently fletching'
def sell():
    print('starting to sell')
    #go to cornpop square
    bezierMovement(1321,1380,368,412)
    randomSleep(0.1,0.2)
    agui.click()
    randomSleep(4.1,5.6)
    #go to well square
    bezierMovement(860,920,265,305)
    randomSleep(0.1,0.2)
    agui.click()
    randomSleep(4.1,5.6)
    #go to shop keeper
    bezierMovement(710,740,165,205)
    randomSleep(0.1,0.2)
    agui.click()
    randomSleep(4.1,5.6)
    #right click the bow
    clickCoords = bezierMovement(2420,2440,1030,1055)
    print('prev right click coords', clickCoords)
    randomSleep(0.1,0.2)
    agui.click(button='RIGHT')
    randomSleep(0.2,0.4)
    #sell all bows
    bezierMovement(2420,2440,clickCoords[1] + 100,clickCoords[1] + 108)
    randomSleep(0.1,0.2)
    agui.click()
    randomSleep(0.2,0.4)
    #return to well square
    bezierMovement(1900,1950,1360,1375)
    randomSleep(0.1,0.2)
    agui.click()
    randomSleep(6.1,7.6)
    #return to cornpop square
    bezierMovement(1805,1875,1290,1360)
    randomSleep(0.1,0.2)
    agui.click()
    randomSleep(5,5.6)
    #return to willow square
    bezierMovement(1160,1235,1200,1260)
    randomSleep(0.1,0.2)
    agui.click()
    randomSleep(5.1,5.9)
    #hop worlds
    kb.send('alt + shift + z')
    randomSleep(10.1,15.6)
    kb.send('esc')
    print('done selling')
    return 'Initializing'


#need to add check for WC level, when i level i need to click again
while continueLoop:
    randomSleep(1.9, 5.7)
    #being woodcutting on function init
    if status == 'Initializing':
        print('Initing function')
        status = chopTree()
        continue

    context = analyze_context(status)
    print('Current context: ', context)
    if context == 'no action':
        continue
    elif context == 'tree down, wait':
        status = 'Waiting for willow'
        print('status: ', status)
        continue
    elif context == 'Begin chopping':
        status = chopTree()
        print('status: ', status)
    elif context == 'start fletching':
        print('starting to fletch')
        status = fletch(2315,2340,1078,1101)
    elif context == 'start selling':
        status = sell()
    # TO DO
    # starting fletching again
    elif context == 'gained fletch level':
        print('restarting fletching after level gain, waiting for notification to dissappear')
        randomSleep(9.3,10.8)
        status = fletch(2470,2498,1312,1328)
    print('--------------------------------------')      


    
    
