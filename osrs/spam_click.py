import datetime
import random

import osrs
import pyautogui

run_time_in_seconds = 45

def main():
    start_time = datetime.datetime.now()
    curr_pos = pyautogui.position()
    while (datetime.datetime.now() - start_time).total_seconds() < run_time_in_seconds:
        x = random.randint(curr_pos.x - 2, curr_pos.x + 3)
        y = random.randint(curr_pos.y - 2, curr_pos.y + 3)
        for i in range(random.randint(5, 50)):
            pyautogui.click(x, y)

main()