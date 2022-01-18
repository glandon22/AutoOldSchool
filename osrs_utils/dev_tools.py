import pyautogui
import time
import pyautogui
import pyscreenshot


def quick_screenshot(name, add):
    print('ready in 3')
    time.sleep(3)
    x, y = pyautogui.position()
    print('sc box', x, y)
    im = pyscreenshot.grab([x, y, x + add, y + add])
    # save image file
    im.save(r'screens\\' + name + '.png', 'png')


def get_pos():
    time.sleep(2)
    print(pyautogui.position())


def calculate_clickbox():
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


def capture_screenshot(name):
    screenshot_box = calculate_clickbox()
    print('sc box', screenshot_box)
    time.sleep(1)
    im = pyscreenshot.grab([screenshot_box[0], screenshot_box[2], screenshot_box[1], screenshot_box[3]])
    # save image file
    im.save(r'..\\screens\\' + name + '.png', 'png')


def capture_specific_screen_coords(screenshot_box, name):
    im = pyscreenshot.grab([screenshot_box[0], screenshot_box[2], screenshot_box[1], screenshot_box[3]])
    # save image file
    im.save(name + '.png', 'png')
    return im


def capture_under_mouse(name):
    print('capturing hover bar')
    current_mouse_x, current_mouse_y = pyautogui.position()
    hover = pyscreenshot.grab([current_mouse_x + 1, current_mouse_y + 31, current_mouse_x + 140, current_mouse_y + 49])
    hover.save(r'screens\\' + name + '.png', 'png')
    return hover

#calculateClickbox()