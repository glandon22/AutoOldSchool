import pyautogui
import time
import pyautogui
import pyscreenshot

inv_coords = [
    [2317, 2343, 1030, 1056], [2371, 2395, 1034, 1058], [2424, 2448, 1034, 1060], [2476, 2500, 1036, 1058],
    [2320, 2344, 1082, 1103], [2372, 2394, 1082, 1102], [2425, 2448, 1082, 1100], [2478, 2499, 1082, 1102],
    [2320, 2340, 1128, 1144], [2372, 2395, 1126, 1146], [2422, 2446, 1126, 1144], [2476, 2500, 1127, 1142],
    [2323, 2340, 1168, 1190], [2372, 2396, 1172, 1192], [2424, 2446, 1174, 1192], [2478, 2503, 1173, 1190],
    [2320, 2342, 1216, 1238], [2374, 2394, 1215, 1238], [2425, 2447, 1216, 1233], [2479, 2500, 1220, 1238],
    [2320, 2342, 1259, 1282], [2372, 2394, 1261, 1280], [2425, 2446, 1262, 1280], [2478, 2500, 1261, 1280],
    [2319, 2342, 1305, 1326], [2370, 2393, 1306, 1322], [2426, 2445, 1306, 1324], [2476, 2500, 1304, 1324]
]

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


def capture_empty_bag():
    for slot in range(len(inv_coords)):
        pyscreenshot.grab((inv_coords[slot][0], inv_coords[slot][2], inv_coords[slot][1], inv_coords[slot][3])).save('..\\screens\\empty_bag\\slot' + str(slot) + '.png')

#calculate_clickbox()