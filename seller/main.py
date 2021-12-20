import random
import keyboard as kb
from general_utils import isInvFull, randomSleep, roughImgCompare
from bezier import bezierMovement
import pyautogui as agui
from PIL import Image, ImageGrab
import numpy
print(roughImgCompare('.\\screens\\target.png', .95, (0,0,2560, 1440)))
"""while True:
    loc = roughImgCompare('target', .75, (500,0,1800, 1440))"""