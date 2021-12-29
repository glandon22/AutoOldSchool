import pyautogui
import time
import pyautogui
import pyscreenshot as ImageGrab


def quick_screenshot(name, add):
    print('ready in 3')
    time.sleep(3)
    x, y = pyautogui.position()
    print('sc box', x, y)
    im = ImageGrab.grab([x, y, x + add, y + add])
    # save image file
    im.save(r'screens\\' + name + '.png', 'png')


def get_pos():
    time.sleep(2)
    print(pyautogui.position())


def calculateClickbox():
    i = 0
    points = list()
    while i < 4:
        print('position mouse for click ', i, ' in 3 seconds')
        time.sleep(3)
        points.append(pyautogui.position())
        i = i + 1
    x1 = round((points[0].x + points[3].x) / 2)
    x2 = round((points[1].x + points[2].x) / 2)
    y1 = round((points[0].y + points[1].y) / 2)
    y2 = round((points[2].y + points[3].y) / 2)
    print([x1, x2, y1, y2])
    return [x1, x2, y1, y2]


def getInvCoords():
    fullCoords = []
    i = 0
    while i < 28:
        print('getting inv slot ', i + 1)
        fullCoords.append(calculateClickbox())
        print('full coords ', fullCoords)
        print(i + 1, ' completed. moving to next slot')
        i = i + 1


def captureScreenshot(name):
    screenshotBox = calculateClickbox()
    print('sc box', screenshotBox)
    im = ImageGrab.grab([screenshotBox[0], screenshotBox[2], screenshotBox[1], screenshotBox[3]])
    # save image file
    im.save(r'screens\\' + name + '.png', 'png')


def captureSpecificScreenCoords(screenshotBox, name):
    im = ImageGrab.grab([screenshotBox[0], screenshotBox[2], screenshotBox[1], screenshotBox[3]])
    # save image file
    im.save(r'screens\\' + name + '.png', 'png')
    return im


def captureUnderMouse(name):
    print('capturing hover bar')
    currentMouseX, currentMouseY = pyautogui.position()
    hover = ImageGrab.grab([currentMouseX + 1, currentMouseY + 31, currentMouseX + 140, currentMouseY + 49])
    hover.save(r'screens\\' + name + '.png', 'png')
    return hover
