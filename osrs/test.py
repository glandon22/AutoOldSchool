import pywinctl as pwc
import pyautogui
import osrs

win = pwc.getWindowsWithTitle('utahdogs', condition=pwc.Re.CONTAINS)
win = win[0]
win.activate()
print('1')
pyautogui.click(500, 500)