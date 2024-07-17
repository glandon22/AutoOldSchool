import time

import pyautogui
import pywinctl as pwc

windows = pwc.getWindowsWithTitle('RuneLite')
window = windows[0]
window.activate()
pyautogui.click(827, 291, button='right')

