import time

import pyautogui
import pywinctl as pwc
import osrs

windows = pwc.getWindowsWithTitle('RuneLite', condition=pwc.Re.CONTAINS)
window = windows[0]
window.activate()
osrs.clock.random_sleep(0.1, 0.11)
osrs.keeb.press_key('f5')

