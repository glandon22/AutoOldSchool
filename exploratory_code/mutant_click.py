import ctypes
import pyautogui
import time

MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_LEFTCLICK = MOUSEEVENTF_LEFTDOWN + MOUSEEVENTF_ABSOLUTE

def _size():
    """Returns the width and height of the screen as a two-integer tuple.
    Returns:
      (width, height) tuple of the screen size, in pixels.
    """
    return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)


def _send_mouse_event(ev, x, y, dw_data=0):
    width, height = _size()
    """x,y = pyautogui.position()
    print(x, y)"""
    ctypes.windll.user32.SetCursorPos(x, y)
    converted_x = 65536 * x // width + 1
    converted_y = 65536 * y // height + 1
    time.sleep(0.0001)
    ctypes.windll.user32.mouse_event(ev, ctypes.c_long(converted_x), ctypes.c_long(converted_y), dw_data, 0)

_send_mouse_event(MOUSEEVENTF_LEFTCLICK, 1150, 370)
"""while True:
    print(pyautogui.position())"""