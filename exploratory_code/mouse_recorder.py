import random
import time
from autoscape import general_utils
import pyautogui
import cv2
import pyscreenshot
import numpy as np
import pandas as pd
import plotly.express as px
import math

def main():
    import mouse
    import keyboard
    # Any duration less than this is rounded to 0.0 to instantly move the mouse.
    pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
    # Minimal number of seconds to sleep between mouse moves.
    pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
    # The number of seconds to pause after EVERY public function call.
    pyautogui.PAUSE = 0  # Default: 0.1aa
    events = []  # This is the list where all the events will be stored
    mouse.hook(events.append)  # starting the recording
    keyboard.wait("a")  # Waiting for 'a' to be pressed
    mouse.unhook(events.append)
    points = [[events[0][0], events[0][1]]]
    dest = [events[-1][0], events[-1][1]]
    timing = events[-1][2] - events[0][2]
    for i in range(len(events)):
        if events[i][0] == 'down':
            points.append('click')
        elif events[i][0] == 'up':
            continue
        elif i % 10 == 0:
            points.append([events[i][0], events[i][1]])
    points.append(dest)
    sleep_time = timing / len(points)
    file1 = open("data.csv", "a")
    dist = general_utils.point_dist(int(points[0][0]), int(points[0][1]), int(dest[0]), int(dest[1]))
    data1 = '{}, {}\n'.format(sleep_time, dist)
    file1.write(data1)
    file1.close()
    """time.sleep(2)
    for point in points:
        if point == 'click':
            pyautogui.click()
            continue
        pyautogui.moveTo(point)
        time.sleep(sleep_time / 10)"""
def kf(keys):
    #print('jjjj',type(keys))
    print(keys.astype(float).sort_values(ascending=False))
    return keys

def plot():
    import pandas as pd
    import plotly.express as px

    df = pd.read_csv('./data.csv')
    df =df.sort_values(by=['pixels'], key=kf)
    fig = px.scatter(df, x='time', y='pixels', title='average seconds between points')
    fig.show()

def create_window():
    while True:

        scr = np.array(pyscreenshot.grab())
        x = random.randint(0,1900)
        y = random.randint(0,1050)
        print(x, y)
        cv2.rectangle(scr, (x, y), (x + 20, y + 20), (0, 0, 0), 3)
        cv2.imshow("test", scr)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        import mouse
        import keyboard
        # Any duration less than this is rounded to 0.0 to instantly move the mouse.
        pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
        # Minimal number of seconds to sleep between mouse moves.
        pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
        # The number of seconds to pause after EVERY public function call.
        pyautogui.PAUSE = 0  # Default: 0.1aa
        events = []  # This is the list where all the events will be stored
        mouse.hook(events.append)  # starting the recording
        keyboard.wait("a")  # Waiting for 'a' to be pressed
        mouse.unhook(events.append)
        points = [[events[0][0], events[0][1]]]
        dest = [events[-1][0], events[-1][1]]
        timing = events[-1][2] - events[0][2]
        for i in range(len(events)):
            if events[i][0] == 'down':
                points.append('click')
            elif events[i][0] == 'up':
                continue
            elif i % 10 == 0:
                points.append([events[i][0], events[i][1]])
        points.append(dest)
        sleep_time = timing / len(points)
        file1 = open("data.csv", "a")
        dist = general_utils.point_dist(int(points[0][0]), int(points[0][1]), int(dest[0]), int(dest[1]))
        data1 = '{},{}\n'.format(sleep_time, dist)
        file1.write(data1)
        file1.close()
        print('here')
        return True


def get_points():
    while True:

        scr = np.array(pyscreenshot.grab())
        x = random.randint(0,1900)
        y = random.randint(0,1050)
        print(x, y)
        cv2.rectangle(scr, (x, y), (x + 20, y + 20), (0, 0, 0), 3)
        cv2.imshow("test", scr)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        import mouse
        import keyboard
        # Any duration less than this is rounded to 0.0 to instantly move the mouse.
        pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
        # Minimal number of seconds to sleep between mouse moves.
        pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
        # The number of seconds to pause after EVERY public function call.
        pyautogui.PAUSE = 0  # Default: 0.1aa
        events = []  # This is the list where all the events will be stored
        mouse.hook(events.append)  # starting the recording
        keyboard.wait("a")  # Waiting for 'a' to be pressed
        mouse.unhook(events.append)
        points = [[events[0][0], events[0][1]]]
        dest = [events[-1][0], events[-1][1]]
        timing = events[-1][2] - events[0][2]
        for i in range(len(events)):
            if i % 10 == 0:
                points.append([events[i][0], events[i][1]])
        points.append(dest)
        file1 = open("points.csv", "a")
        iter = random.randint(0, 100000)
        for point in points:
            data1 = '{},{}, {}\n'.format(iter, point[0], point[1])
            file1.write(data1)
        file1.close()
        print('here')
        return True

def plot_points():
    import pandas as pd
    import plotly.express as px

    df = pd.read_csv('./points.csv')
    fig = px.line(df, x='x', y='y', color='iter')
    fig.show()

def advanced_bezier(point, w, h):
    pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
    pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
    pyautogui.PAUSE = 0  # Default: 0.1
    x1, y1 = pyautogui.position()
    x2 = random.randint(point[0], point[0] + w)
    y2 = random.randint(point[1], point[1] + h)
    dist = math.floor(general_utils.point_dist(x1, y1, x2, y2))
    cp = math.floor(dist/10)
    # Distribute control points between start and destination evenly.
    x = np.linspace(x1, x2, num=cp, dtype='int')
    y = np.linspace(y1, y2, num=cp, dtype='int')
    # Randomise inner points a bit (+-RND at most).
    rnd = random.randint(3, 6)
    xr = [random.randint(-rnd, rnd) for _ in range(cp)]
    yr = [random.randint(-rnd, rnd) for _ in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr
    points = []
    for i in range(len(x)):
        points.append([x[i], y[i]])
    if random.randint(0, 5) == 1:
        print('going to overshoot')
        temp = points[-1]
        points[-1] = [points[-1][0] + random.randint(7, 20), points[-1][1] + random.randint(4, 16)]
        points.append(temp)
    for point in points:
        pyautogui.moveTo(point)
        general_utils.random_sleep(.0003, .0004)

def testing():
    import autoscape
    for i in range(28):
        slot = autoscape.show_inv_coords(i)
        autoscape.bezier_movement(slot[0], slot[1], slot[2], slot[3])
        time.sleep(1)

testing()